"""

	This script reads a file where tweets in JSON format are stored and
	prints to screen the sentiment value assigned to each tweet.

	The sentiment value is computed by adding up the score of each term 
	in the tweet. The score of each term is obtained from a file that
	has a number of terms with corresponding scores. If a term in the 
	tweet is not in the reference file then that score in the tweet 
	gets assigned a value of zero.

	This script is excecuted as 

		python 02_tweet_sentiment_scores.py AFINN-111.txt output.txt 

	where AFINN-111.txt is the reference file containing the scores of terms
	and output.txt is the file containing the tweets that are going to be scored


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



def return_parsed_afinn(sent_file):

	""" 
		This function parses the sentiment file (AFINN-111.txt in this case)
		and gets a dictionary from it. 

		Arguments -- file containing sentiments
		Returns -- dictiionary

		dictionary keys -- words in file
		dictionary value -- sentiment value assigned to a given word

	"""
	
	# We open file
	afinnfile = open(sent_file)

	# initialize an empty dictionary
	scores = {} 

	# For every line in file...
	for line in afinnfile:
		 # The file is tab-delimited. "\t" means "tab character"
		 # So we split lines in tab
		term, score  = line.split("\t") 
		# Convert the score to an integer and assign value to key in dictionary
  		scores[term] = int(score)  

  	# return dictionary
	return scores 


def tweet_sentiment_value(tweet_text,sent_dictionary):

	"""
		This function assigns a sentiment value sent_value to a 
		tweeter text, tweet_text, based on a given dictionary sent_dictionary

		Arguments -- tweet_text , sent_dictionary
		Returns -- sent_value

	"""

	# Initialize sentiment value to zero
	sent_value = 0

	# We split the tweeter text to get a list out of it
	# and iterate over the resulting list.
	# For every word in the resulting list...
	for word in tweet_text.split():
		# ... we check if the word is in the set of the
		# given dictionary list...
		if word in sent_dictionary.keys():
			# If so, we update the sentiment value by the
			# value given to the word found
			sent_value += sent_dictionary[word]
	
	# Return resulting sentiment value
	return sent_value




def process_tweets(tweet_file,afinn_dict):
	
	"""
		This function, based  on a sentiment dictionary afinn_dict,  
		assigns a sentiment value to every tweet in a collection of 
		tweets contained in a file tweet_file

		Important -- tweet_file is given in JSON format

	"""
	# We open tweet_file and store it
	tweetfile = open(tweet_file)
	
	# Initialize an empty dictionary
	scores = {} 

	# Initialize counter of tweets to be processed
	count_tweet = 0

	# For every line in tweetfile...
	for line in tweetfile:

		# Since each line is in JSON format we convert it 
		# into a Python data structure
		parsed_json = json.loads(line)

		# Initialize sentiment value
		sentiment_value = 0


		# Since we are only interested in tweets containing text in English
		# we check there is actually text in a given tweet and that is written in 
		# English
		if ('text' in parsed_json.keys()) and ('lang' in parsed_json.keys()) and (parsed_json['lang'] == 'en'):

			# If so, we update the number of tweet to be processed
			#count_tweet += 1

			# Since the text in the parsed_json dictionary is unicoded ...
			unicode_string = parsed_json['text']
			# ... we encode it to a Python string
			encoded_string = unicode_string.encode('utf-8')

			# We do some extra cleaning by means of regular expressions
			# IMPORTANT .- We have not considered extra cleaning regarding 
			# URL's, hashtags and/or @ included in the tweets. This is something
			# that definetly can be refined in the future...
			encoded_string = re.sub(r'[^a-z0-9\s]', '', encoded_string.strip().lower()) 

			# We assign sentiment value based invoking the tweet_sentiment_value function
			sentiment_value = tweet_sentiment_value(encoded_string,afinn_dict)
 
			# Finally print tweet along its sentiment value
			#print encoded_string , sentiment_value
			print sentiment_value

		else:

			print sentiment_value
		
def main():

    sent_file , tweet_file = sys.argv[1] , sys.argv[2]
    
    #parse_afinn()
    dict_scores = {}
    dict_scores = return_parsed_afinn(sent_file)
    #print dict_scores.items()
    process_tweets(tweet_file,dict_scores)

if __name__ == '__main__':
    main()
