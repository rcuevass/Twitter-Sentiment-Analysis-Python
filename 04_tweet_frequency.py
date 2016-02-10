"""

	This script reads a file where tweets in JSON format are stored and
	prints to screen the frequency of each term in all of the tweets


	This script is excecuted as 

		python 04_tweet_frequency.py output.txt 

	where output.txt is the file containing the tweets that are going to be scored


"""


import sys
# Library to convert a JSON string into a Python data structure
import json 
# Library to handle regular expressions
import re

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))



def get_freq_tweets(tweet_file):
	
	"""
		This function reads a file containing tweets in JSON format 
		and prints to screen the pair (word,pct), where word is the term
		in tweets and pct is the fraction of that term in the whole corpus 
		of tweets

		Important -- tweet_file is given in JSON format

		Argument -- tweet_file

		Rerurn -- total count of terms in tweets (word_count)
			      dictionary of frequency terms (freq_dict)

	"""
	# We open tweet_file and store it
	tweetfile = open(tweet_file)
	
	# Initialize an empty dictionary where we will store 
	# the unique terms
	freq_dict = {} 

	# Initialize count of words in tweets
	word_count = 0

	# For every line in tweetfile...
	for line in tweetfile:

		# Since each line is in JSON format we convert it 
		# into a Python data structure
		parsed_json = json.loads(line)

		# Since we are only interested in tweets containing text in English
		# we check there is actually text in a given tweet and that is written in 
		# English
		if ('text' in parsed_json.keys()) and ('lang' in parsed_json.keys()) and (parsed_json['lang'] == 'en'):

			# Since the text in the parsed_json dictionary is unicoded ...
			unicode_string = parsed_json['text']

			# ... we encode it to a Python string
			encoded_string = unicode_string.encode('utf-8')

			# We do some extra cleaning by means of regular expressions
			# IMPORTANT .- We have not considered extra cleaning regarding 
			# URL's, hashtags and/or @ included in the tweets. This is something
			# that definetly can be refined in the future...
			encoded_string = re.sub(r'[^a-z0-9\s]', '', encoded_string.strip().lower()) 

			# For a particular tweet, we make a list out of it and loop over it...
			for word in encoded_string.split():

				# We check if the word is already in the dictionary.
				# If it is and is not related to a hyper-link....
				if ( word in freq_dict.keys() ) and ('https' not in word):
					# we increase the counter for that term...
					freq_dict[word] +=1
					# ... and increase the word counter
					word_count += 1
				# If the term is not in the dictionary...
				elif (word not in freq_dict.keys()) and ('https' not in word):
					# ... we add the term to it...
					freq_dict[word] = 1
					# ... and increase the word counter
					word_count += 1


	# Now that we have the dictionary, we loop over the 
	for word in freq_dict.keys():
		# We compute the percentage associated with this term
		pct = float(freq_dict[word])/word_count
		# And print to screen the pair.
		print "%s %.4f" % (word, pct)

	# We return word_count and dictionary of frequency in case we need it latter
	return word_count , freq_dict
 

def main():

	# Determine name of files from command line
    tweet_file = sys.argv[1] 
    
    # Feed the names of such files to the function that will print terms along scores
    get_freq_tweets(tweet_file)

if __name__ == '__main__':
    main()
