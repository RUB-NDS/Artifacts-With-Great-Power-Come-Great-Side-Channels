import os
import sys
from tabulate import tabulate

tool_mapping = {
    "1a" : 'rtlf-alpha-lowest',
    "1b" : 'rtlf-alpha-0-9',
    "1c" : 'rtlf-alpha-9',
    "1d" : 'rtlf-alpha-18',
    "2" : 'dudect',
    "3" : 'mona',
    "4" : 't-test',
    "5a" : 'tlsfuzzer',
    "5b" : 'tlsfuzzer-bonferroni'
}

color_mapping = {
    "green" : "\033[32m",
    "red" : "\033[31m",
    "blue" : "\033[34m",
    "default" : "\033[0m" 
}

# map attack vector identifiers from the measuring tool to the abbreviations used in the figures
attack_vector_paper_mapping = {
    # Bleichenbacher (BB) Vectors
    "Wrong_second_byte_(0x02_set_to_0x17)vsCorrectly_formatted_PKCS#1_PMS_message": "B1B2",
    "Invalid_TLS_version_in_PMSvsCorrectly_formatted_PKCS#1_PMS_message": "B1B3",
    "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsCorrectly_formatted_PKCS#1_PMS_message": "B1B4",
    "No_0x00_in_messagevsCorrectly_formatted_PKCS#1_PMS_message": "B1B5",
    "Wrong_second_byte_(0x02_set_to_0x17)vsInvalid_TLS_version_in_PMS": "B2B3",
    "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsWrong_second_byte_(0x02_set_to_0x17)": "B2B4",
    "No_0x00_in_messagevsWrong_second_byte_(0x02_set_to_0x17)": "B2B5",
    "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsInvalid_TLS_version_in_PMS": "B3B4",
    "No_0x00_in_messagevsInvalid_TLS_version_in_PMS": "B3B5",
    "No_0x00_in_messagevs0x00_on_the_next_to_last_position_(|PMS|_=_1)": "B4B5",
    
    # Padding Oracle (PO) Vectors
    "InvPadValMac-[0]-0-59vsValPadInvMac-[0]-0-59": "P1P2",
    "InvPadValMac-[0]-0-59vsPlain_FF": "P1P3",
    "InvPadValMac-[0]-0-59vsPlain_XF_(0xXF=#padding_bytes)": "P1P4",
    "Plain_FFvsValPadInvMac-[0]-0-59": "P2P3",
    "ValPadInvMac-[0]-0-59vsPlain_XF_(0xXF=#padding_bytes)": "P2P4",
    "Plain_FFvsPlain_XF_(0xXF=#padding_bytes)": "P3P4",
    
    # Lucky Thirteen (L13) Vectors
    "NO_PADDINGvsLONG_PADDING": "L1L2",
}


def get_real_eval_mapping(filename):
    for prefix, mapping in attack_vector_paper_mapping.items():
        if filename.startswith(prefix):
            return mapping
    return None


def map_result_files(filename):
    mapping = get_real_eval_mapping(filename)
    if mapping != None :
        return mapping
    else:
        return filename

def process_all_directories(directory_paths, tool_index, options):
    suffix = tool_mapping.get(tool_index)
    # Iterate over all directories and files
    for directory in directory_paths:
        files_no_diff, files_diff = process_directory(suffix, directory)
        print_directory_result(options, directory, files_no_diff, files_diff)


def process_all_directories_all_tools(directory_paths, options):
    for directory in directory_paths:
        suffix_no_diff, suffix_diff = {}, {}
        for tool_index in tool_mapping.keys():
            files_no_diff, files_diff = process_directory(tool_mapping.get(tool_index), directory)
            if len(files_no_diff) > 0 or len(files_diff) > 0:
                suffix_no_diff[tool_index] = files_no_diff
                suffix_diff[tool_index] = files_diff
        print_directory_batch_result(options, directory, suffix_no_diff, suffix_diff)


def process_directory(suffix, directory):
    exit_code_no_diff, exit_code_diff = resolve_exit_code(suffix)
    files_no_diff, files_diff = [], []
    for filename in os.listdir(directory):
        # Check if file is a result file and read its result value
        if filename.endswith(suffix):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    content = file.read()
                    if exit_code_no_diff in content:
                        files_no_diff.append(filename)
                    if exit_code_diff in content:
                        files_diff.append(filename)
    return files_no_diff, files_diff


def resolve_exit_code(suffix):
    if "tlsfuzzer" in suffix:
        exit_code_no_diff = "0"
        exit_code_diff = "1"
    else:
        exit_code_no_diff = "10"
        exit_code_diff = "11"
    return exit_code_no_diff,exit_code_diff


def print_directory_batch_result(options, directory, suffix_no_diff, suffix_diff):
    print(f"{color_mapping.get('blue')}{directory}{color_mapping.get('default')}")
    headers = [tool_mapping.get(key) for key in suffix_diff.keys()]
    line_no_diff = ["No Diff:"]   
    line_diff = ["Diff:"]
    for key in suffix_diff.keys():
        if options == "-d":
            mapped_files_no_diff = [map_result_files(entry) for entry in suffix_no_diff[key]]
            mapped_files_diff = [map_result_files(entry) for entry in suffix_diff[key]]
            line_no_diff.append(f"{color_mapping.get('green')}{','.join(mapped_files_no_diff)}{color_mapping.get('default')}")
            line_diff.append(f"{color_mapping.get('red')}{','.join(mapped_files_diff)}{color_mapping.get('default')}")
        else:
            line_no_diff.append(f"{color_mapping.get('green')}{len(suffix_no_diff[key])}{color_mapping.get('default')}")
            line_diff.append(f"{color_mapping.get('red')}{len(suffix_diff[key])}{color_mapping.get('default')}")
    data = [line_no_diff, line_diff]
    print(tabulate(data, headers=headers, tablefmt="grid"))


def print_directory_result(options, directory, files_no_diff, files_diff):
    print(f"{color_mapping.get('blue')}{directory}")
    print(f"{color_mapping.get('green')}  No difference : {len(files_no_diff)}")
    if options == "-d":
        for file in files_no_diff:
                # attempt to map file name to vectors defined in paper for easier comparison
            mapping = get_real_eval_mapping(file)
            if mapping != None:
                print(f"{color_mapping.get('green')}   {mapping} ({file})")
            else:
                print(f"{color_mapping.get('green')}   {file}")
    print(f"{color_mapping.get('red')}  Difference    : {len(files_diff)}")
    if options == "-d":
        for file in files_diff:
                # attempt to map file name to vectors defined in paper for easier comparison
            mapping = get_real_eval_mapping(file)
            if mapping != None:
                print(f"{color_mapping.get('red')}   {mapping} ({file})")
            else:
                print(f"{color_mapping.get('red')}   {file}")


def main(directory_path, tool_index, options):
    # Collect all directories containing the specific result files
    matching_directories = []
    if tool_index == "all":
        for root, dirs, files in os.walk(directory_path):
            if any(".result-" in file for file in files):
                    matching_directories.append(root)
        process_all_directories_all_tools(matching_directories, options)
    else:
        for root, dirs, files in os.walk(directory_path):
            if any(file.endswith(".result-" + tool_mapping.get(tool_index)) for file in files):
                matching_directories.append(root)
        # Process all colledted directories
        process_all_directories(matching_directories, tool_index, options)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: <directory_path> <suffix_index> <options>")
        print("  <directory_path> : Path to the directory containing the result files.")
        print("  <suffix_index>   : Index of the suffix to use or 'all'.")
        print("                     1a : rtlf-alpha<<0.9%, 1b : rtlf-alpha<0.9%, 1c : rtlf-alpha<9%, 1d : rtlf-alpha<18%, 2: dudect, 3: mona, 4: t-test, 5a: tlsfuzzer, 5b: tlsfuzzer-bonferroni")
        print("  <options>        : Options.")
        print("                     n: Normal output, d: Detailed output")    
        sys.exit(1)

    print("Selected directory : " + sys.argv[1])
    if(sys.argv[2] == "all"):
        print("Selected suffix    : all")
    else:
        print("Selected suffix    : " + tool_mapping.get(sys.argv[2]))
    print("Selected options   : " + sys.argv[3])
    print("")
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    print("")
    print(f"{color_mapping.get('default')}Completed reporting.")