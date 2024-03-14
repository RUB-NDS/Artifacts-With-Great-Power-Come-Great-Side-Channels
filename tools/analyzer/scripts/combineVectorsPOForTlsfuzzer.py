import csv
import os
import sys

def isBasline(line):
    return line[0].strip() == "BASELINE"

def isModified(line):
    return line[0].strip() == "MODIFIED"

"""Get all BASELINE vectors from a file."""
def getBaselineAsList(input_file):
    lines_baseline = []
    with open(input_file, "r", newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line_read in csv_reader:
            if isBasline(line_read):
                lines_baseline.append(line_read[1])
    return lines_baseline

""""Get all MODIFIED vectors from a file."""
def getModifiedAsList(eingabe_datei):
    lines_modified = []
    with open(eingabe_datei, "r", newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line_read in csv_reader:
            if isModified(line_read):
                lines_modified.append(line_read[1])
    return lines_modified

"""Merge the measurements for specific folder."""
def merge_for_folder(folder_path):
    # Files to merge
    basline =   getBaselineAsList(folder_path + "/" + "InvPadValMac-[0]-0-59vsPlain_FF.csv")
    modified1 = getModifiedAsList(folder_path + "/" + "InvPadValMac-[0]-0-59vsPlain_FF.csv")
    modified2 = getModifiedAsList(folder_path + "/" + "InvPadValMac-[0]-0-59vsPlain_XF_(0xXF=#padding_bytes).csv")
    modified3 = getModifiedAsList(folder_path + "/" + "InvPadValMac-[0]-0-59vsValPadInvMac-[0]-0-59.csv")

    result_file = "timing.csv"
    with open(folder_path + "/" + result_file, "w", newline="") as csv_datei:
        csv_writer = csv.writer(csv_datei)
        csv_writer.writerow(["InvPadValMac-[0]-0-59", "Plain_FF", "Plain_XF_(0xXF=#padding_bytes)", "ValPadInvMac-[0]-0-59.csv"])
    
        max_length = 500000
        if len(basline) < max_length:
            max_length = len(basline)
            print(f"CSV only contained {max_length} lines. Limiting output accordingly")
        for i in range(max_length):
            csv_writer.writerow([basline[i], modified1[i], modified2[i], modified3[i]])

"""Find all Padding Oracle folders and merge the measurements inside them."""
def find_padding_oracle_folders(root_path):
    ctr = 0
    for root, _, _ in os.walk(root_path):
        if "PaddingOracle" in os.path.basename(root):
            merge_for_folder(root)
            ctr = ctr + 1
            print(f"Done preparing {ctr} files.")

"""MAIN"""
def main():
    if len(sys.argv) != 2:
        print("Usage: python combineVectorsPOForTlsfuzzer.py <path>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"Path '{path}' does not exist.")
        sys.exit(1)

    find_padding_oracle_folders(path)

"""MAIN"""
if __name__ == "__main__":
    main()