import json, sys, os, codecs



DATA_ROOT_DIR = sys.argv[1]
DATA_TSV_DIR = os.path.join(DATA_ROOT_DIR, "tsv")
ACC_ID = sys.argv[2]
TXT = sys.argv[3]


def extractTweetsFromAcc(ID, filename):

	tweets = []
	with codecs.open(filename, "r", "utf-8") as f:
		
		for line in f:
			data = line.split('\t')
			if (data[1] == ACC_ID):
				tweets.append(line)
			else:
				pass
		
		return tweets

def extractONLYTEXTFromAcc(ID, filename):

	tweets = []
	with codecs.open(filename, "r", "utf-8") as f:
		
		for line in f:
			data = line.split('\t')
			if (data[1] == ACC_ID):
				tweets.append(data[3])
			else:
				pass
		
		return tweets



def main():

	folderDate = os.listdir(DATA_TSV_DIR)
	# folder Date = ['2014-11', '2014-12', '2015-01', ...]

	for folder in folderDate:

		folderPath = os.path.join(DATA_TSV_DIR, folder)
		files = os.listdir(folderPath)
		filePathInFolder = 	[os.path.join(folderPath, filename) for filename in files]
		print("Processing " + folder)
		
		outname = "All_Tweets_" + ACC_ID + ".tsv"
		with codecs.open(outname, "w", "utf-8") as outf: 
			# Process File
			for i in filePathInFolder:
				#print("Processing " + i)
				if(TXT == 1):
					TweetsLines = extractTweetsFromAcc(ACC_ID, i)
					for line in TweetsLines:
						outf.write(line)
				else:
					TextLines = extractONLYTEXTFromAcc(ACC_ID, i)
					for line in TextLines:
						outf.write(line)

if __name__ == '__main__':
	main()