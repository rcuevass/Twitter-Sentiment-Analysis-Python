"""

	This script reads a file where tweets in JSON format are stored and
	prints to screen the top-ten most popular hashtags in the collection of tweets


	This script is excecuted as 

		python 06_top_ten_hashtags.py output.txt 

	where output.txt is the file containing the tweets that are going to be scored


"""

import sys
# Library to convert a JSON string into a Python data structure
import json 
# Library to handle regular expressions
import re
# Library to handle intrinsic opeators of Python. In this code is used in
# particular to sort a dictionary
import operator


def process_hashtags_tweets(tweet_file):
	
	"""
		This function reads a file containing tweets in JSON format 
		and returns a dictionary containin all unique hashtags in tweets
		along with its frequency

		Important -- tweet_file is given in JSON format

		Argument -- tweet_file

		Rerurn -- hashtag_dict, dictionary mentioned in the description
								of this function

	"""
	# We open tweet_file and store it
	tweetfile = open(tweet_file)
	
	# Initialize an empty dictionary where we will store 
	# the unique hashtags
	hashtag_dict = {} 

	# Initialize count of words in tweets
	word_count = 0

	# For every line in tweetfile...
	for line in tweetfile:

		# Since each line is in JSON format we convert it 
		# into a Python data structure
		parsed_json = json.loads(line)


		# We check 'entities' , which is related to the hashtags, is in the 
		# JSON dictionary and that the tweet is in English
		if ('entities' in parsed_json) and ('lang' in parsed_json.keys()) \
			and (parsed_json['lang'] == 'en') :

			# If so, we extract the list containing all hashtags associated with a
			# tweet
			aux_list = parsed_json['entities']['hashtags']
			
			# We check the list is not empty. This statment is equivalent
			# to if len(aux_list) != 0:
			if aux_list:

				# If not empty, we loop over all elements of the list...
				for term_ in (aux_list):
					# ... extract hashtag's text ...
					hash_text =  term_['text']

					# ... encode it ...
					hash_text_processed = hash_text.encode("utf-8").strip()

					# ... check if there is 'chomp' in text
					if '\n' in hash_text_processed:

						# ...if there is, we remove it...
						hash_text_processed = hash_text_processed.strip('\n')

					# Now that the hashtag has been parsed and cleaned we check if it is
					# in the dictionary's keys and has no 'https' associated with it...
					if ( hash_text_processed in hashtag_dict.keys() ) \
						and ('https' not in hash_text_processed):
						# If so, we update counter of hashtag...
						hashtag_dict[hash_text_processed] += 1
					elif ( hash_text_processed not in hashtag_dict.keys() ) \
						and ('https' not in hash_text_processed):
						# ... otherwise we add it to the dictionary
						hashtag_dict[hash_text_processed] = 1

	# Return dictionary...
	return hashtag_dict



def print_top_n(hashtag_dict,n):

	"""
		This function prints the top-n keys in a dictionary along it corresponding
		values

		Arguments -- dictionary, hashtag_dict
					 n, integer indicating the top-n we wish to print

		Returns -- Prints to screen the top-n elements described 
	"""

	# Making use of itemgetter from the operator library, https://docs.python.org/2/library/operator.html
	# we sort the dictionary in incrasing order.
	sorted_dict = sorted(hashtag_dict.items(), key=operator.itemgetter(1))
	# Then we re-sort it in decreasing order...
	sorted_dict = sorted_dict[::-1]

	# ... and print the top-n keys along with their values
	for term_ in sorted_dict[:n]:
		print term_[0] , int(term_[1])
 

def main():

	# Determine name of files from command line
    tweet_file = sys.argv[1] 

    # Get a dictionary of hashtags associated with the tweets in file
    hashtag_dict = process_hashtags_tweets(tweet_file)
    
    # Feed the recently obtained dictionary to the function that will print 
    # the top-n hashtags
    print_top_n(hashtag_dict,10)

if __name__ == '__main__':
    main()
