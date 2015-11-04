# Janani Kalyanam
# CREATED 8/8/2013

import numpy
import scipy, scipy.io
import math
import os, sys
import json
import glob
import numpy as np
import scipy.io
from datetime import date, timedelta
import scipy.sparse.csgraph
from scipy.sparse.csgraph import connected_components
import operator
# import clusterKeywords

match_no = 3;  # specify minimum number of word matches.
max_no_events = 4;  # max number of events for each hout
no_hours = 4;


def sort_cols_ascending(filename):
	fid = open(filename, 'r')
	lines = fid.readlines();
	lines = map(lambda x: x.strip(), lines);
	fid.close();

	fid = open('temp1.txt', 'w');

	first = 1;
	ii = 0;
	for line in lines:
		if (first == 1):
			fid.write(line + '\n');
			first = 0;
			continue;
		if (line == ''):
			continue
		line1 = line.split(' ');
		print ii
		ii = ii + 1
		print line1
		if (divmod(len(line1), 2)[1] != 0):
			print 'SOMETHING WRONG'
			sys.exit(1);

		col = line1[::2]
		vals = line1[1::2]

		col = map(lambda x: int(x), col);
		ind_col = sorted(enumerate(col), key=operator.itemgetter(1));
		my_str = ''
		for each in ind_col:
			my_str = my_str + str(each[1]) + ' ' + str(vals[each[0]]);

		print my_str
		fid.write(my_str + '\n');
	fid.close()


def produceComponents(filename):
	f = open(filename, 'r');
	myDict = eval(f.read())

	connected_components = {};
	keyword_pairs = {};

	myDates = myDict.keys();

	for each_date in myDates:
		theKey = each_date;
		theItem = [];
		theKeywordPairItem = [];

		for each_component in myDict[each_date]:
			m = each_component.keys()[0];
			list_of_pairs = each_component[m].keys();
			list_of_pairs = map(lambda x: x.split(' '), list_of_pairs);
			for each_pair in list_of_pairs:
				theKeywordPairItem.append(each_pair);

			theItem.append(list(m));

		connected_components[each_date] = theItem;
		keyword_pairs[each_date] = theKeywordPairItem;

	myTuple = (connected_components, keyword_pairs);

	return myTuple;


def produceComponents_ofSizeMoreThan2(filename):
	f = open(filename, 'r');
	myDict = eval(f.read())

	connected_components = {};
	keyword_pairs = {};
	no_keywords_per_component = {};

	myDates = myDict.keys();

	for each_date in myDates:
		theKey = each_date;
		theItem = [];
		theKeywordPairItem = [];
		noOfPairsItem = [];
		for each_component in myDict[each_date]:
			if (len(list(each_component.keys()[0])) > 2):
				m = each_component.keys()[0];  # this is the component itself.
				list_of_pairs = each_component[m].keys();  # these are the pairs
				len_of_constituents = 0;
				for each_pair in list_of_pairs:
					ii = 0;
					no_times = each_component[m][each_pair]
					len_of_constituents = len_of_constituents + no_times;
					my_pair = each_pair.split(' ');
					while (ii < no_times):
						theKeywordPairItem.append(my_pair);
						ii = ii + 1
				theItem.append(list(m));
				noOfPairsItem.append(len_of_constituents);

		if (len(theItem) > 1):
			connected_components[each_date] = theItem;
			keyword_pairs[each_date] = theKeywordPairItem;
			no_keywords_per_component[each_date] = noOfPairsItem;

	return (connected_components, keyword_pairs, no_keywords_per_component);


def searchAgain(timestamp_file, key1, key2=''):
	# Whether or not you should search for key1 and key2 again.
	# timestamp_file is the name of the keyword-score file that
	# will be found in mquezada/data/news/ and should be of the format
	# YYYY-MM-DD_hhmmss_keyword_scores.txt;
	# returns 0 for don't search, and 1 for search again.

	split_filename = timestamp_file.split('-');
	yyyy = split_filename[0];
	mm = split_filename[1];
	dd = split_filename[2].split('_')[0];


	#  get list of files with the same date
	list_of_files = glob.glob(
		'../../mquezada/data/news/' + timestamp_file.split('_')[
			0] + '*keywords*.txt');
	list_of_files = sorted(list_of_files);
	ind = list_of_files.index('../../mquezada/data/news/' + timestamp_file);
	if (ind + 1 + no_hours <= len(list_of_files) - 1):
		files_to_search = list_of_files[
						  ind + 1:ind + 1 + 4];  # all files are from the same day
	else:
		# need to grab files from the next day
		date_next_day = date(int(yyyy), int(mm), int(dd)) + timedelta(1);
		new_list_of_files = glob.glob(
			'../../mquezada/data/news/' + str(date_next_day.year) + '-' + str(
				date_next_day.month).zfill(2) +
			'-' + str(date_next_day.day).zfill(2) + '_' + '*keywords*.txt');
		files_to_search = list_of_files[ind + 1:];
		files_to_search = files_to_search + new_list_of_files[
											:(no_hours - len(files_to_search))];


	########################################################
	# files_to_search are the list of files that we need to search in.
	searchAgain_retval = 1;
	print files_to_search
	for file in files_to_search:
		groups_of_keywords = getKeywords(file);
		print groups_of_keywords;
		for each_group in groups_of_keywords:
			if ((key1 in each_group) or (key2 in each_group)):
				searchAgain_retval = 0;
				break;
		if not searchAgain_retval:
			break;

	return searchAgain_retval;


def mergeEvents(date_start, date_end):
	ret_val = getAdjacencyMatrix(date_start, date_end);
	A = ret_val['A'];
	vocab = ret_val['vocab'];
	list_of_keywords = ret_val['list_of_keywords'];
	if (len(list_of_keywords) == 0):
		return []
	keyword_components = getKeywordComponents(A, list_of_keywords);
	cardinalities = map(lambda x: len(x), keyword_components);

	count = 0;
	while (count > 0):
		count = count - 1;

		cardinalities = map(lambda x: len(x), keyword_components);
		ind_largest_component = np.argmax(cardinalities);
		largest_component = keyword_components[ind_largest_component];
		smaller_components = fragmentGraph(largest_component, A,
										   list_of_keywords);
		del keyword_components[ind_largest_component];
		for each_component in smaller_components:
			keyword_components.append(each_component);
	cardinalities = map(lambda x: len(x), keyword_components);

	fid = open('keyword_components.txt', 'w');
	for each_component in keyword_components:
		for each_key in each_component:
			fid.write(each_key + '\n');
		fid.write('\n\n')
	fid.close();

	return keyword_components


def getAdjacencyMatrix(date_start, date_end):
	# This function merges events between date_start and date_end.
	# date_start and date_end are string of the form 'yyyy-mm-dd'.
	# The function returns a list of keyword-groups, where each group
	# forms an "event". 

	ret_val = {};
	ret_val = getKeywordVocabulary(date_start, date_end);
	vocab = ret_val['vocab'];
	files = ret_val['files'];

	list_of_keywords = vocab.keys();
	A = np.zeros((len(list_of_keywords), len(list_of_keywords)), dtype=np.int);

	for each_file in files:
		groups_of_keywords = getKeywords(each_file);
		for each_group in groups_of_keywords:
			ind1 = list_of_keywords.index(each_group[0]);
			ind2 = list_of_keywords.index(each_group[1]);
			A[ind1, ind2] = A[ind1, ind2] + 1;
			A[ind2, ind1] = A[ind1, ind2];

	ret_val = {};
	ret_val['A'] = A;  # adjacenty matrix
	ret_val['vocab'] = vocab;  # dictionary of word counts.
	ret_val['list_of_keywords'] = list_of_keywords;  # list of keywords
	return ret_val;


def fragmentGraph(keyword_component, A, list_of_keywords):
	# returns the final merged group of keywords
	keyword_component = list(keyword_component);
	indices = [];
	for each_key in keyword_component:
		indices.append(list_of_keywords.index(each_key));

	A_fragment = A[indices, :];
	A_fragment = A_fragment[:, indices];
	deg = np.sum(A_fragment, 1);
	node_with_max_edge = np.argmax(np.sum(A_fragment, 1));
	A_fragment = scipy.delete(A_fragment, node_with_max_edge, axis=0)
	A_fragment = scipy.delete(A_fragment, node_with_max_edge, axis=1)
	max_edge_keyword = keyword_component[node_with_max_edge];
	del keyword_component[node_with_max_edge];

	new_components = getKeywordComponents(A_fragment, keyword_component);

	for each_component in new_components:
		each_component.append(max_edge_keyword)
	return new_components


def getKeywordComponents(A, list_of_keywords):
	# A	= scipy.delete(A,node_max_deg,0);
	# A	= scipy.delete(A,0,node_max_deg);
	# del vocab[list_of_keywords[node_max_deg]];
	no_components, assignment = connected_components(A);
	assignment = np.array(assignment);

	keyword_components = [[] for i in range(no_components)];
	for i in range(no_components):
		indices = np.where(assignment == i)[0];
		for each in indices:
			keyword_components[i].append(list_of_keywords[each]);

	return keyword_components;


def getKeywordVocabulary(date_start, date_end):
	# calliing this function forms a vocabulary of keywords used for searches
	# between date_start and date_end.  date_start and date_end are strings of
	# the form 'yyyy-mm-dd'.  It extracts keywords 
	# from /mquezada/data/news/<yyyy-mm-dd>_timestamp_keywords.txt using getKeywords()
	# function.  And then forms a vocabulary of all the keywords, and returns a dictionary.
	# First element of the dictionary is a list of keywords, and the second element is a
	# list of files between date_start and date_end.

	mm_start = int(date_start.split('-')[1]);
	dd_start = int(date_start.split('-')[2]);
	yy_start = int(date_start.split('-')[0]);
	mm_end = int(date_end.split('-')[1]);
	dd_end = int(date_end.split('-')[2]);
	yy_end = int(date_end.split('-')[0]);

	vocab = {};
	ret_val = {};


	# start_date	= date(int(yy_start),int(mm_start),int(dd_start)) + timedelta(1);
	start_date = date(int(yy_start), int(mm_start), int(dd_start));
	end_date = date(int(yy_end), int(mm_end), int(dd_end)) + timedelta(1);

	final_list_of_files = [];
	d = start_date;
	while (1):
		if (d == end_date):
			break;

		temp_date = str(d.year).zfill(4) + '-' + str(d.month).zfill(
			2) + '-' + str(d.day).zfill(2);
		list_of_files = glob.glob(
			'../../mquezada/data/news/' + temp_date + '*scores*');

		for file_name in list_of_files:
			groups_of_keywords = getKeywords(file_name);
			final_list_of_files.append(file_name);
			for each_keyword_group in groups_of_keywords:
				for keyword in each_keyword_group:
					if keyword not in vocab.keys():
						vocab[keyword] = 1;
					else:
						vocab[keyword] = vocab[keyword] + 1;
		d = d + timedelta(1);

	ret_val['vocab'] = vocab;
	ret_val['files'] = final_list_of_files;

	return ret_val;


def calculatePerplexity(likelihood, nWords):
	# likelihood is a vector of likelihoods for each doc.
	# nWords is the number of words in each doc.
	# len(likelihood) = len(nWords) = numDocs
	# calculates perplexity as:
	# exp{-\frac{sum(likelihood)}{sum(nWords)}}

	if (len(likelihood) != len(nWords)):
		sys.exit('ERROR: likelihood and nWords need to be of the same length');

	likelihood_sum = sum(likelihood);
	nWords_sum = sum(nWords);

	perplexity = math.exp(-likelihood_sum / nWords_sum);

	return perplexity


def parseFile_likelihood_ldaInput(likelihood_file, lda_input_file):
	# Parser for the *lda-likelihood file (to form a vector
	# of likelihoods,) and lda-input file (to form a vector
	# of document lengths).



	fid_likelihood = open(likelihood_file, 'r');

	likelihood = fid_likelihood.readlines();
	likelihood = map(lambda x: float(x.strip()), likelihood);

	fid_lda_input_file = open(lda_input_file, 'r');
	nWords = fid_lda_input_file.readlines();
	nWords = map(lambda x: float(x.strip().split(' ')[0]), nWords);

	if (len(likelihood) != len(nWords)):
		sys.exit('ERROR: likelihood and nWords need to be of the same length');

	return {'likelihood': likelihood, 'nWords': nWords}


def similarity(sentence1, sentence2):
	words1 = sentence1.split(' ');
	words2 = sentence2.split(' ');

	words1 = set(words1);
	words2 = set(words2);

	common = words1.intersection(words2);
	total = words1.union(words2);

	similarity_struct = {};
	similarity_struct['sim'] = len(common) / float(len(total));
	similarity_struct['no_common_words'] = len(common);
	similarity_struct['common_words'] = common;

	return similarity_struct;


def collect_keywords(groups_of_keywords, new_keywords):
	check_flag = 0;

	if (len(groups_of_keywords) == 0):
		a = {};
		for each in new_keywords:
			a[each] = 1;
		groups_of_keywords.append(a);
		return groups_of_keywords;

	intersection_length = [];
	for group in groups_of_keywords:
		orig_keywords = set(group.keys());
		common_keywords = orig_keywords.intersection(new_keywords);
		intersection_length.append(len(common_keywords))

	max_score_ind = intersection_length.index(max(intersection_length));

	if (intersection_length[max_score_ind] >= match_no):
		check_flag = 1;
		for each in new_keywords:
			if each in groups_of_keywords[max_score_ind].keys():
				groups_of_keywords[max_score_ind][each] = \
					groups_of_keywords[max_score_ind][each] + 1;
			else:
				groups_of_keywords[max_score_ind][each] = 1;

	if (check_flag == 0):
		a = {};
		for each in new_keywords:
			a[each] = 1;
		groups_of_keywords.append(a);

	return groups_of_keywords;


def getKeywords_fromHeadlines(headlines, outFile):
	# INPUT: inFile is a file of headlines (stop words removed
	# and everything lower case).  OUTPUT:  Sets of keywords will
	# be written in outFile.

	groups_of_keywords = [];  # is a list

	# fin		= open(inFile, 'r');
	# headlines	= fin.readlines();
	headlines = map(lambda x: x.strip(), headlines);
	# fin.close();

	for i in range(len(headlines)):
		for j in range(len(headlines))[i + 1:]:
			if (i == j):
				continue;
			struct = similarity(headlines[i], headlines[j]);
			if (struct['no_common_words'] < match_no):
				continue;
			groups_of_keywords = collect_keywords(groups_of_keywords,
												  struct['common_words']);

	fout = open(outFile, 'w');

	scores = [];
	i = 0;
	for group in groups_of_keywords:
		# print i
		avg = 0;
		for each_key in group.keys():
			avg = avg + group[each_key];
		scores.append(float(avg) / len(group.keys()));
		i = i + 1;

	sorted_indices = numpy.argsort(scores);
	sorted_indices = sorted_indices[::-1];  # highest value first

	for i in range(len(sorted_indices)):
		index = sorted_indices[i]
		fout.write(str(scores[index]) + '\n');
		for each_key in groups_of_keywords[index].keys():
			string = each_key + ' ' + str(
				groups_of_keywords[index][each_key]) + '\n';
			fout.write(string);
		fout.write('\n\n');

	fout.close()
	return groups_of_keywords;


def parseHeadlinesByHour(filename, date):
	# filename is the name of json file
	# data is string of the format 'yyyy-mm-dd'

	fid = open(filename);
	data = json.load(fid);
	fid.close();

	date_time = date + ' 00:41:30';
	keys_of = data.keys();

	hour = 0;
	while (date_time in keys_of):
		headlines = data[date_time];
		hh = date_time.split(' ')[-1].split(':')[0];
		mm = date_time.split(' ')[-1].split(':')[1];
		ss = date_time.split(' ')[-1].split(':')[2];

		headlines_file = date + '_' + str(hh) + str(mm) + str(ss) + '.txt';
		hour = hour + 1;
		fid = open(headlines_file, 'w');
		for each in headlines:
			fid.write(each + '\n');

		fid.close();
		next_hour = str(int(date_time.split(' ')[-1].split(':')[0]) + 1).zfill(
			2);
		date_time = date + ' ' + next_hour + ':41:30';


def getKeywords(inFile):
	# inFile is a text file containing the keywords.

	fid = open(inFile, 'r');
	lines = fid.readlines();
	lines = map(lambda x: x.strip(), lines);
	lines = map(lambda x: x.split(' '), lines);
	fid.close();

	no_events = 1;
	line_no = 0;

	list_of_keywords = [];

	while (1):
		if (no_events > max_no_events):
			break;
		if (line_no > len(lines) - 1):
			break;

		if (lines[line_no][0] == ''):
			no_events = no_events + 1;
			line_no = line_no + 2;
			continue;

		if (len(lines[line_no]) == 1 and lines[line_no][0] != ''):
			line_no = line_no + 1;
			continue;

		if (len(lines[line_no]) == 2):
			scores = [];
			words = [];
			while (lines[line_no][0] != ''):
				scores.append(float(lines[line_no][1]));
				words.append(lines[line_no][0]);
				line_no = line_no + 1;
			sorted_indices = numpy.argsort(scores);
			sorted_indices = sorted_indices[::-1];
			list_of_keywords.append(
				[words[sorted_indices[0]], words[sorted_indices[1]]])

	return list_of_keywords


def preprocess_headlines(filename, filename_out):
	# Convert everything to lower case
	# remove stop words
	# filename is

	fid = open(filename)
	data = json.load(fid);

	fid_stopwords = open('stopwords.txt', 'r');
	stopwords = fid_stopwords.readlines();
	stopwords = map(lambda x: x.strip(), stopwords);
	fid_stopwords.close()


	# filename_out	= filename.split('.json')+'.txt';
	fid_out = open(filename_out, 'w')

	for item in data:
		line = item['text'];
		# print line
		line = line.split(' ');
		line = map(lambda x: x.lower(), line);
		toRemove = [];
		index = 0;
		for word in line:
			if word in stopwords:
				toRemove.append(index);
			index = index + 1;

		new_line = [];
		for i in range(len(line)):
			if i not in toRemove:
				new_line.append(line[i]);

		for word in new_line:
			if (word == 'killing' or word == 'killed' or word == 'kills'):
				word = 'kill';

		string = '';
		for word in new_line:
			string = string + word + ' ';
		string = string + '\n';
		fid_out.write(string);


if __name__ == '__main__':
	sort_cols_ascending('temp.txt')

	'''
	timestamp_file = '2013-09-02_183456_keywords_scores.txt';
	timestamp_file = '2013-09-02_131233_keywords_scores.txt';
	searchAgain(timestamp_file)	
	############################################
	no_days = 5;
	begin	= date(2013,9,6);
	keywords_across_days	= {};
	while(no_days > 0):
		no_days	= no_days - 1;
		date_start	= str(begin.year).zfill(4)+'-'+str(begin.month).zfill(2)+'-'+str(begin.day).zfill(2);
		next		= begin+timedelta(1);
		date_end	= str(next.year).zfill(4)+'-'+str(next.month).zfill(2)+'-'+str(next.day).zfill(2);
		print date_start + ' ' + date_end + '\n'
		l	= mergeEvents(date_start,date_end);
		if(len(l) == 0):
			begin = next
			continue;
		keyword_components	=	l;
		keywords_across_days[date_start] = keyword_components;
		
		filename	= 'keywords_'+date_start+'_'+date_end+'.txt';
		fid	= open(filename,'w');
		for each_component in keyword_components:
			for each_keyword in each_component:
				fid.write(each_keyword+'\n');
			fid.write('\n')
		begin = next

	merged_list	= clusterKeywords.clusterKeywords(keywords_across_days)
	print	type(merged_list)
	fid	= open('merged_list.txt','w');
	for each_component in merged_list:
		fid.write(str(each_component.score)+'\n');
		for each_keyword in each_component.keyword_list:
			fid.write(each_keyword+'\n');
		fid.write('\n')
	# preprocess_headlines('../../mquezada/code/twitter/headlines/2013-08-20_173933.json','temp.txt')

	inFile		= '../data/2013-08-16_034130_keywords.txt';
	myList		= getKeywords(inFile);
	
	for ii in range(len(myList)):
		print ii
		for jj in range(len(myList[ii])):
			print myList[ii][jj]
		
	#####################################
	### USAGE FOR getKeywords_fromHeadlines();
	### filenames is a list of filenames with headlines. (Remove stop words from headlines).
	for each_filename in filenames:

		in_filename	= each_filename;
		out_filename	= each_filename.split('.txt')[0]+'_keywords.txt';
	
		groups_of_keywords	=	getKeywords_fromHeadlines(in_filename, out_filename);
		#print stats(groups_of_keywords[:10],in_filename);
	'''

