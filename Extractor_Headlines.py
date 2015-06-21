import json, os, sys

DATA_ROOT_DIR = sys.argv[1]
DATA_DIR = os.path.join(DATA_ROOT_DIR, "data-headlines")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROC_DATA_DIR = os.path.join(DATA_DIR, "processed")
TSV_DATA_DIR = os.path.join(DATA_DIR, "tsv")


def cleantext(text):
	return text.replace("\n","").replace("\t", "").replace("\r", "")


def json_to_tsvfile(folder, filename):

	new_filename = filename.replace("json", "tsv")
	inputfile_path = os.path.join(PROC_DATA_DIR, folder, filename)
	outputfile_path = os.path.join(TSV_DATA_DIR, folder, new_filename)

	with open(outputfile_path, 'w') as outputfile:
		with open(inputfile_path, 'r') as inputfile:

			for line in inputfile:
				tweet = json.loads(line)
				outline_list = []
				outline_list.append(tweet["created_at"])
				outline_list.append(tweet["user"]["id_str"])
				outline_list.append(tweet["id_str"])
				outline_list.append(cleantext(tweet["text"]))
				outline = '\t'.join(outline_list) + '\n'
				outline = outline.encode("utf-8")
				outputfile.write(outline)


def processFile(folder, filename):

	inputfile_path = os.path.join(RAW_DATA_DIR, folder, filename)
	outputfile_path = os.path.join(PROC_DATA_DIR, folder, "processed_" + filename)

	with open(outputfile_path, 'w') as outputfile:
		with open(inputfile_path, 'r') as inputfile:

			inputfile_json = json.load(inputfile)
			
			for tweet_json in inputfile_json:
				outputfile.write(json.dumps(tweet_json) + '\n')

'''
This file, process a directory of the form data_root_dir/data-headlines/raw/XXX.json
which has a json array with many tweets and transform it into a data_root_dir/data-headlines/processed/processed_XXX.json
which has the same tweets, but 1 json object (1 tweet) per line
'''

def main():
	
	foldersDateName = os.listdir(PROC_DATA_DIR)

	for folder in foldersDateName:
		print("Processing the data folder: " + folder)
		folderDateFullPath = os.path.join(PROC_DATA_DIR, folder)
		filesInDateFolder = [ filename for filename in os.listdir(folderDateFullPath) if os.path.isfile(os.path.join(folderDateFullPath, filename)) and os.access(os.path.join(folderDateFullPath, filename), os.R_OK) and filename.endswith(".json") ]

		for json_file in filesInDateFolder:
			#processFile(folder, json_file)
			json_to_tsvfile(folder, json_file)


if __name__ == '__main__':
	main()