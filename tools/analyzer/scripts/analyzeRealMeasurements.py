import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

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

"""Call tool with the given file path and return its output."""
def call_tool(file_path, tool_index):
    if tool_index == "1a":
        file_path = "'" + file_path + "'"
        result_R_Data = file_path + ".result-" + tool_mapping.get(tool_index) + ".RDATA"
        result = subprocess.run("Rscript /analyzer/r-files/RTLF_alpha_lowest.R " + file_path + " " + result_R_Data + " && Rscript /analyzer/r-files/readRData.R " + result_R_Data, capture_output=True, text=True, shell=True)
        return result.returncode
    elif tool_index == "1b":
        file_path = "'" + file_path + "'"
        result_R_Data = file_path + ".result-" + tool_mapping.get(tool_index) + ".RDATA"
        result = subprocess.run("Rscript /analyzer/r-files/RTLF_alpha_0_9.R " + file_path + " " + result_R_Data + " && Rscript /analyzer/r-files/readRData.R " + result_R_Data, capture_output=True, text=True, shell=True)
        return result.returncode
    elif tool_index == "1c":
        file_path = "'" + file_path + "'"
        result_R_Data = file_path + ".result-" + tool_mapping.get(tool_index) + ".RDATA"
        result = subprocess.run("Rscript /analyzer/r-files/RTLF_alpha_9.R " + file_path + " " + result_R_Data + " && Rscript /analyzer/r-files/readRData.R " + result_R_Data, capture_output=True, text=True, shell=True)
        return result.returncode
    elif tool_index == "1d":
        file_path = "'" + file_path + "'"
        result_R_Data = file_path + ".result-" + tool_mapping.get(tool_index) + ".RDATA"
        result = subprocess.run("Rscript /analyzer/r-files/RTLF_alpha_18.R " + file_path + " " + result_R_Data + " && Rscript /analyzer/r-files/readRData.R " + result_R_Data, capture_output=True, text=True, shell=True)
        return result.returncode
    elif tool_index == "2":
        file_path = "'" + file_path + "'"
        result = subprocess.run("/analyzer/dudect/dudect_r_comparison_-O2 " + file_path, capture_output=True, text=True, shell=True)
        return result.returncode
    elif tool_index == "3":
        file_path = "'" + file_path + "'"
        command = "java -jar ReportingTool.jar -i " + file_path
        result = subprocess.run("cd /analyzer/mona-timing-report && " + command, capture_output=True, text=True, shell=True)
        return result.returncode
    elif tool_index == "4":
        result = subprocess.run(['Rscript', '/analyzer/r-files/t-test.R', file_path, "0.009"], capture_output=True, text=True)
        return result.returncode  
    elif tool_index == "5a":
            command = "PYTHONPATH=. python3 tlsfuzzer/analysis.py --no-ecdf-plot --no-scatter-plot --no-conf-interval-plot --alpha 0.009  -o " + file_path.replace("timing.csv", "")
            result_1 = subprocess.run("source /venv/bin/activate && cd /analyzer/tlsfuzzer && " + command, capture_output=True, text=True, shell=True)
            result_2 = subprocess.run("cd " + file_path.replace("timing.csv", "") + "&& rm legend.csv sample_stats.csv timing.bin* timing.csv report.* *.png", capture_output=True, text=True, shell=True)
            return result_1.returncode
    elif tool_index == "5b":
            command = "PYTHONPATH=. python3 tlsfuzzer/analysis_cmp1b.py --no-ecdf-plot --no-scatter-plot --no-conf-interval-plot --alpha 0.009  -o " + file_path.replace("timing.csv", "")
            result_1 = subprocess.run("source /venv/bin/activate && cd /analyzer/tlsfuzzer && " + command, capture_output=True, text=True, shell=True)
            result_2 = subprocess.run("cd " + file_path.replace("timing.csv", "") + "&& rm legend.csv sample_stats.csv timing.bin* timing.csv report.* *.png", capture_output=True, text=True, shell=True)
            return result_1.returncode
    return None

"""Write exit code to file."""
def write_res(new_filepath, exit_code):
    with open(new_filepath, 'w') as file:
        file.write(str(exit_code))

"""Process one file."""
def process_file(file_path, tool_index):
    exit_code = call_tool(file_path, tool_index)
    result_file_path = f"{file_path}.result-{tool_mapping.get(tool_index)}"
    write_res(result_file_path, exit_code)
    return exit_code

"""Process files in parallel."""
def process_files(file_paths, tool_index, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_file = {executor.submit(process_file, file, tool_index): file for file in file_paths}
        for future in as_completed(future_to_file):
           future.result()
    return

"""Collect all CSV files in the directory and subdirectories."""
def collect_files(directory_path, tool_index, file_type):
    file_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(file_type):
                file_paths.append(os.path.join(root, file))
    return file_paths

"""MAIN"""
def main(directory_path, tool_index, num_threads):
    if(tool_index in ["5a", "5b"]):
        subprocess.run(["python3", "combineVectorsBBForTlsfuzzer.py", directory_path], capture_output=True, text=True)
        subprocess.run(["python3", "combineVectorsPOForTlsfuzzer.py", directory_path], capture_output=True, text=True)
        file_paths = collect_files(directory_path, tool_index, "timing.csv")
    else:
        file_paths = collect_files(directory_path, tool_index, ".csv")
    process_files(file_paths, tool_index, num_threads)

"""MAIN"""
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: <directory_path> <tool_index> <num_threads>")
        print("  <directory_path> : Path to the directory containing CSV files.")
        print("  <tool_index>     : Index of the tool to use for analysis.")
        print("                     1a : rtlf-alpha<<0.9%, 1b : rtlf-alpha<0.9%, 1c : rtlf-alpha<9%, 1d : rtlf-alpha<18%, 2: dudect, 3: mona, 4: t-test, 5a: tlsfuzzer, 5b: tlsfuzzer-bonferroni")
        print("  <num_threads>    : Number of threads to use for parallel processing.")
        sys.exit(1)

    print("Selected directory : " + sys.argv[1])
    print("Selected tool      : " + tool_mapping.get(sys.argv[2]))
    print("Number of threads  : " + sys.argv[3])
    print("")
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print("")
    print("Completed processing.")