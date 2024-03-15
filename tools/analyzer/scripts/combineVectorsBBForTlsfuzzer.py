import csv
import os
import sys

def isBasline(line):
    return line[0].strip() == "BASELINE"

def isModified(line):
    return line[0].strip() == "MODIFIED"

"""Get all BASELINE vectors from a file."""
def getBaselineAsList(eingabe_datei):
    lines_baseline = []
    with open(eingabe_datei, "r", newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line_read in csv_reader:
            if isBasline(line_read):
                lines_baseline.append(line_read[1])
    return lines_baseline

""""Get all MODIFIED vectors from a file."""
def getModifiedAsList(input_file):
    lines_modified = []
    with open(input_file, "r", newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line_read in csv_reader:
            if isModified(line_read):
                lines_modified.append(line_read[1])
    return lines_modified

"""Merge the measurements for specific folder."""
def merge_for_folder(folder_path):
    # Files to merge
    basline =   getBaselineAsList(folder_path + "/" + "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsCorrectly_formatted_PKCS#1_PMS_message.csv")
    modified1 = getModifiedAsList(folder_path + "/" + "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsCorrectly_formatted_PKCS#1_PMS_message.csv")
    modified2 = getModifiedAsList(folder_path + "/" + "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsInvalid_TLS_version_in_PMS.csv")
    modified3 = getModifiedAsList(folder_path + "/" + "0x00_on_the_next_to_last_position_(|PMS|_=_1)vsWrong_second_byte_(0x02_set_to_0x17).csv")
    modified4 = getBaselineAsList(folder_path + "/" + "No_0x00_in_messagevs0x00_on_the_next_to_last_position_(|PMS|_=_1).csv")

    result_file = "timing.csv"
    with open(folder_path + "/" + result_file, "w", newline="") as csv_datei:
        csv_writer = csv.writer(csv_datei)
        csv_writer.writerow(["0x00_on_the_next_to_last_position_(|PMS|_=_1)", "Correctly_formatted_PKCS#1_PMS_message.csv", "Invalid_TLS_version_in_PMS.csv", "Wrong_second_byte_(0x02_set_to_0x17).csv", "No_0x00_in_message"])
    
        max_length = 500000
        if len(basline) < max_length:
            max_length = len(basline)
            print(f"CSV only contained {max_length} lines. Limiting output accordingly")
        for i in range(max_length):
            csv_writer.writerow([basline[i], modified1[i], modified2[i], modified3[i], modified4[i]])

"""Find all Bleichenbacher folders and merge the measurements inside them."""
def find_bleichenbacher_folders(root_path):
    ctr = 0
    for root, _, _ in os.walk(root_path.rstrip("/")):
        if "Bleichenbacher" in os.path.basename(root):
            merge_for_folder(root)
            ctr = ctr + 1
            print(f"Done preparing {ctr} files.")

"""MAIN"""
def main():
    if len(sys.argv) != 2:
        print("Usage: python combineVectorsBBForTlsfuzzer.py <path>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"Path '{path}' does not exist.")
        sys.exit(1)

    find_bleichenbacher_folders(path)

"""MAIN"""
if __name__ == "__main__":
    main()