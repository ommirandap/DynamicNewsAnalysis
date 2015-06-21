import json, sys, os, codecs

DATA_ROOT_DIR = sys.argv[1]
DATA_TSV_DIR = os.path.join(DATA_ROOT_DIR, "tsv")


def readAccountID(filename):
	accounts = []
	with codecs.open(filename, "r", "utf-8") as f:
		
		for line in f:
			data = line.split('\t')
			largo = len(data)
			if(largo != 4):
				print("Error in file: " + filename)
				print("Largo = : " + str(largo) + "\tLinea:\t" + line)
				return None
			accounts.append(data[1])
		
		accounts.sort()
		return accounts


def main():

	folderDate = os.listdir(DATA_TSV_DIR)
	# folder Date = ['2014-11', '2014-12', '2015-01', ...]

	for folder in folderDate:

		folderPath = os.path.join(DATA_TSV_DIR, folder)
		files = os.listdir(folderPath)
		filePathInFolder = 	[os.path.join(folderPath, filename) for filename in files]
		
		# Process File
		for i in filePathInFolder:
			#print("Processing " + i)

			acc_ids = readAccountID(i)
			if acc_ids == None:
				print("Check errors! Exiting...")
				sys.exit()
			
			else:
				for j in acc_ids:
					#print(filePathInFolder + " : " + j)
					print j



if __name__ == '__main__':
	main()