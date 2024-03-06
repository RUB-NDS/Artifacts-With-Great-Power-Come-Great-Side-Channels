import os
import sys

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

def process_directories(directory_paths, tool_index, options):
    suffix = tool_mapping.get(tool_index)
    # Set counter check values
    if tool_index in ["5a", "5b"]:
        counter_10_check = "0"
        counter_11_check = "1"
    else:
        counter_10_check = "10"
        counter_11_check = "11"
    # Iterate over all directories and files
    for directory in directory_paths:
        counter_10, counter_11 = 0, 0
        files_10, files_11 = [], []
        for filename in os.listdir(directory):
            # Check if file is a result file and read its result value
            if filename.endswith(suffix):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as file:
                        content = file.read()
                        if counter_10_check in content:
                            counter_10 += 1
                            files_10.append(filename)
                        if counter_11_check in content:
                            counter_11 += 1
                            files_11.append(filename)
        # Print results
        print(f"{color_mapping.get('blue')}{directory}")
        print(f"{color_mapping.get('green')}  No difference : {counter_10}")
        if options == "-d":
            for file in files_10:
                print(f"   {file}")
        print(f"{color_mapping.get('red')}  Difference    : {counter_11}")
        if options == "-d":
            for file in files_11:
                print(f"{color_mapping.get('default')}   {file}")

def main(directory_path, tool_index, options):
    # Collect all directories containing the specific result files
    matching_directories = []
    for root, dirs, files in os.walk(directory_path):
        if any(file.endswith(".result-" + tool_mapping.get(tool_index)) for file in files):
            matching_directories.append(root)
    # Process all colledted directories
    process_directories(matching_directories, tool_index, options)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: <directory_path> <suffix_index> <options>")
        print("  <directory_path> : Path to the directory containing the result files.")
        print("  <suffix_index>   : Index of the suffix to use.")
        print("                     1a : rtlf-alpha<<0.9%, 1b : rtlf-alpha<0.9%, 1c : rtlf-alpha<9%, 1d : rtlf-alpha<18%, 2: dudect, 3: mona, 4: t-test, 5a: tlsfuzzer, 5b: tlsfuzzer-bonferroni")
        print("  <options>        : Options.")
        print("                     n: Normal output, d: Detailed output")    
        sys.exit(1)

    print("Selected directory : " + sys.argv[1])
    print("Selected suffix    : " + tool_mapping.get(sys.argv[2]))
    print("Selected options   : " + sys.argv[3])
    print("")
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    print("")
    print(f"{color_mapping.get('default')}Completed reporting.")