"""

	This script reads a file where tweets in JSON format are stored and
	prints to screen the state with the highest average sentiment (happiest state)


	This script is excecuted as 

		python 05_state_highest_avg_sentiment.py AFINN-111.txt output.txt 

	where AFINN-111.txt is the reference file containing the scores of terms
	and output.txt is the file containing the tweets that are going to be scored


"""

import sys
# Library to convert a JSON string into a Python data structure
import json 
# Library to handle regular expressions
import re
# Library to handle intrinsic opeators of Python. In this code is used in
# particular to sort a dictionary
import operator

def hw():
	print 'Hello, world!'

def lines(fp):
	print str(len(fp.readlines()))


def US_states_dict():

	"""
		This function returns a dictionary of abbreviations of US states
		and the corresponding state's names 

	"""

	states = {
		'AK': 'Alaska',
		'AL': 'Alabama',
		'AR': 'Arkansas',
		'AS': 'American Samoa',
		'AZ': 'Arizona',
		'CA': 'California',
		'CO': 'Colorado',
		'CT': 'Connecticut',
		'DC': 'District of Columbia',
		'DE': 'Delaware',
		'FL': 'Florida',
		'GA': 'Georgia',
		'GU': 'Guam',
		'HI': 'Hawaii',
		'IA': 'Iowa',
		'ID': 'Idaho',
		'IL': 'Illinois',
		'IN': 'Indiana',
		'KS': 'Kansas',
		'KY': 'Kentucky',
		'LA': 'Louisiana',
		'MA': 'Massachusetts',
		'MD': 'Maryland',
		'ME': 'Maine',
		'MI': 'Michigan',
		'MN': 'Minnesota',
		'MO': 'Missouri',
		'MP': 'Northern Mariana Islands',
		'MS': 'Mississippi',
		'MT': 'Montana',
		'NA': 'National',
		'NC': 'North Carolina',
		'ND': 'North Dakota',
		'NE': 'Nebraska',
		'NH': 'New Hampshire',
		'NJ': 'New Jersey',
		'NM': 'New Mexico',
		'NV': 'Nevada',
		'NY': 'New York',
		'OH': 'Ohio',
		'OK': 'Oklahoma',
		'OR': 'Oregon',
		'PA': 'Pennsylvania',
		'PR': 'Puerto Rico',
		'RI': 'Rhode Island',
		'SC': 'South Carolina',
		'SD': 'South Dakota',
		'TN': 'Tennessee',
		'TX': 'Texas',
		'UT': 'Utah',
		'VA': 'Virginia',
		'VI': 'Virgin Islands',
		'VT': 'Vermont',
		'WA': 'Washington',
		'WI': 'Wisconsin',
		'WV': 'West Virginia',
		'WY': 'Wyoming'}

	# Lowered case dictionary
	states = {k.lower(): v.lower() for k, v in states.items()}

	return states


def US_states2timezone_dict():

	"""
		This function returns a dictionary of abbreviations of US states
		and the corresponding time zones

	"""

	state2timezone = { 'AK': 'US/Alaska', 'AL': 'US/Central', 'AR': 'US/Central', 'AS': 'US/Samoa', \
						'AZ': 'US/Mountain', 'CA': 'US/Pacific', 'CO': 'US/Mountain', 'CT': 'US/Eastern', \
						'DC': 'US/Eastern', 'DE': 'US/Eastern', 'FL': 'US/Eastern', 'GA': 'US/Eastern', \
						'GU': 'Pacific/Guam', 'HI': 'US/Hawaii', 'IA': 'US/Central', 'ID': 'US/Mountain', \
						'IL': 'US/Central', 'IN': 'US/Eastern', 'KS': 'US/Central', 'KY': 'US/Eastern', \
						'LA': 'US/Central', 'MA': 'US/Eastern', 'MD': 'US/Eastern', 'ME': 'US/Eastern', \
						'MI': 'US/Eastern', 'MN': 'US/Central', 'MO': 'US/Central', 'MP': 'Pacific/Guam', \
						'MS': 'US/Central', 'MT': 'US/Mountain', 'NC': 'US/Eastern', 'ND': 'US/Central', \
						'NE': 'US/Central', 'NH': 'US/Eastern', 'NJ': 'US/Eastern', 'NM': 'US/Mountain', \
						'NV': 'US/Pacific', 'NY': 'US/Eastern', 'OH': 'US/Eastern', 'OK': 'US/Central', \
						'OR': 'US/Pacific', 'PA': 'US/Eastern', 'PR': 'America/Puerto_Rico', \
						'RI': 'US/Eastern', 'SC': 'US/Eastern', 'SD': 'US/Central', 'TN': 'US/Central', \
						'TX': 'US/Central', 'UT': 'US/Mountain', 'VA': 'US/Eastern', 'VI': 'America/Virgin', \
						'VT': 'US/Eastern', 'WA': 'US/Pacific', 'WI': 'US/Central', 'WV': 'US/Eastern', \
						'WY': 'US/Mountain', '' : 'US/Pacific', '--': 'US/Pacific' }
	return state2timezone


def inverse_dictionary(direct_dictionary):

	"""
		This function reverses a dictionary: turns keys into values and 
		values into keys.

	"""

	inv_dict = {v: k for k, v in direct_dictionary.items()}

	return inv_dict


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


def tweets_sentiment_avg(tweet_file,afinn_dict):
	
	"""
		This function, based  on a sentiment dictionary afinn_dict,  
		assigns a sentiment value to every tweet in a collection of 
		tweets contained in a file tweet_file

		Important -- tweet_file is given in JSON format

		Arguments -- File containing tweets in JSON format, tweet_file
					 File containing bank of sentiment values of words, afinn_dict

		Returns -- Dictionary of US states abbreviations and its corresponding
				   average sentiment value

	"""

	# Dictionary of US states
	US_states = US_states_dict()

	# Inverse US dictionary 
	US_inv_states = inverse_dictionary(US_states)

	# We create an empty dictionary where we will collect the 
	# average of sentiments: to each state we will assign 
	# an average of sentiments associated with that state
	dict_avg = {}

	dict_freq = {}

	dict_states = {}


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
		
		if ('text' in parsed_json.keys()) and ('lang' in parsed_json.keys()) and \
			(parsed_json['lang'] == 'en') and ('user' in parsed_json.keys()):
			
			# Since the text in the parsed_json dictionary is unicoded ...
			unicode_string = parsed_json['text']

			# ... we encode it to a Python string
			encoded_string = unicode_string.encode('utf-8')

			# We do some extra cleaning by means of regular expressions
			# IMPORTANT .- We have not considered extra cleaning regarding 
			# URL's, hashtags and/or @ included in the tweets. This is something
			# that definetly can be refined in the future...
			encoded_string = re.sub(r'[^a-z0-9\s]', '', encoded_string.strip().lower()) 

			# We assign sentiment value based invoking the 
			# tweet_sentiment_value function ... 
			sentiment_value = tweet_sentiment_value(encoded_string,afinn_dict)

			# ... and turn it into a float value (remember we are interested
			# in taking the average of sentiment)
			sentiment_float = float(sentiment_value)

			# We create an auxiliary dictionary out of the 'user' field 
			# from the parsed_json object

			aux_dict = parsed_json['user']

			# We check such a dictionary has 'location' field and that is
			# NOT empty. If this is the case...

			if ('location' in aux_dict.keys() ) and (aux_dict['location'] is not None) :

				# ...we get the location...
				aux_text = aux_dict['location']

				# ... encode it...
				aux_text = aux_text.encode('utf-8')

				# ... clean it up with a regex, srip it and turn it to a 
				# lower case string.
				aux_text = re.sub(r'[^a-z0-9\s]', '', aux_text.strip().lower())

				# We now breake the text appart and split it to turn it into
				# a list
				aux_text = aux_text.replace(',','').split()

				# Here we ASSUME that the list COULD be related with a US state
				# if it has two strings. For instance: Washington, DC , 
				# Durham, NC , etc.
				# If it is lentgh 2 we then ASSUME the second entry is
				# related with the state.
				# If this is the case...
				if (len(aux_text) == 2) and (aux_text[1] in US_states.keys() ):

					# ... we collect it
					state_ = aux_text[1]
						
					# We check whether the state being processed is already in 
					# the dictionary collecting the averages.

					# If the state is NOT in dictionary...
					if state_ not in dict_avg.keys():

						# ... we add it with its corresponding sentiment value 
						# computed...
						dict_avg[state_] = sentiment_float

						# ... and initialize to 1 the frequency such a state has appeared
						dict_freq[state_] = 1.
								

					# If the state is already in the dictionary...
					elif state_ in dict_avg.keys():

						# We update the average...
						dict_avg[state_] = (dict_freq[state_]*dict_avg[state_]) + sentiment_float
						dict_avg[state_] = dict_avg[state_] / ( dict_freq[state_] + 1.)
						# ... and the freqency of such a state
						dict_freq[state_] += 1.

	# Return the desired dictionary...
	return dict_avg


def print_top_n(dict_,n):

	"""
		This function prints the top-n keys in a dictionary along it corresponding
		values

		Arguments -- dictionary, dict_
					 n, integer indicating the top-n we wish to print

		Returns -- Prints to screen the top-n elements described 
	"""


	# Making use of itemgetter from the operator library, https://docs.python.org/2/library/operator.html
	# we sort the dictionary in incrasing order.
	sorted_dict = sorted(dict_.items(), key=operator.itemgetter(1))
	# Then we re-sort it in decreasing order...
	sorted_dict = sorted_dict[::-1]

	# ... and print the top-n keys along with their values
	for term_ in sorted_dict[:n]:
		
		# We make sure the abbreviated string is shown only with two letters
		# along with its corresponding value
		abbv = term_[0].strip('\n').strip('\t').upper()
		abbv = abbv[0:2]
		print abbv , term_[1]
 

def main():

	# Read name of files containing bank of words with sentiment values
	# and tweets
	sent_file , tweet_file = sys.argv[1] , sys.argv[2]
	
	# Set an empty dictionary...
	dict_scores = {}
	# ...where scores of words will be stored
	dict_scores = return_parsed_afinn(sent_file)

	# We feed the recently created dictionary and file of tweets
	# to the function tweets_sentiment_avg that will determine
	# the sentiment average per state
	dict_avg = tweets_sentiment_avg(tweet_file,dict_scores)

	# Print the state with highest average by invoking function
	# print_top_n
	print_top_n(dict_avg,1)


if __name__ == '__main__':
	main()
