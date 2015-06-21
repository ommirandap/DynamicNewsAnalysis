import json
import os


DATA_ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(DATA_ROOT_DIR, "data-headlines")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROC_DATA_DIR = os.path.join(DATA_DIR, "processed")


def processFile(filename):

    inputfile_path = os.path.join(RAW_DATA_DIR, filename)
    outputfile_path = os.path.join(PROC_DATA_DIR, "processed_" + filename)

    with open(outputfile_path, 'w') as outputfile:
        with open(inputfile_path, 'r') as inputfile:
            for line in inputfile:
                tweet = json.loads(line)
                output_line = tweet["created_at"] + '\t' + tweet["id_str"] + '\t' + tweet["text"] + '\n'
                output_line = output_line.encode("utf-8")
                outputfile.write(output_line)


def main():
    filesPath = map(lambda x: os.path.join(RAW_DATA_DIR, x), os.listdir(RAW_DATA_DIR))

    for singleFile_path in filesPath:
        singleFile_name = singleFile_path.split("/")[-1]
        print("Processing the " + singleFile_name + " data file")
        processFile(singleFile_name)


if __name__ == "__main__":
    main()