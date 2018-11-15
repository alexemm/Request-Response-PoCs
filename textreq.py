from urllib import request

import time
import json

# Representation of URL    
class URL_word():
    def __init__(self, word):
        self.url = 'https://www.openthesaurus.de/synonyme/search?q=%s&format=application/json' % word
    
    # String Representation for URL, returns URL for accessing
    def __str__(self):
       return self.url

# Class for handling the Response in JSON from the Web-API       
class Response():
    def __init__(self, url, waiting_time = 1.1):
        
        # 60 Requests/min
        time.sleep(waiting_time)
        self.response = request.urlopen(str(url)).read().decode('UTF-8')
    
    # Dictionary view for Response in JSON
    def as_dictionary(self):
        return json.loads(self.response)
    
    # Accessing like in a dict
    def __getitem__(self, key):
        return self.as_dictionary()[key]
    
    # String Representation of the Response
    def __str__(self):
        return self.response


# Container class for valid words in the German language         
class Valid_List():
    
    # Creating list as container and number of letters, given as n
    def __init__(self, n = 2):
        self.container = []
        self.n = n
    
    # Magic function for handling list like dict    
    def __getitem__(self, key):
        return self.container[key]
    
    # Magic function for appending valid words with a '+'    
    def __add__(self, obj):
        self.container.append(obj)
    
    # Method for putting all the valid words in a list    
    def count_words(self):
        if self.n == 0:
            pass
        return self.__count_words_rek(self.n,"",self.container)
    
    # Helper method for recursion, may be private as it is a helper function
    def count_words_rek(self,n,word, valid_list):
        if n == 0:
            if  self.valid_word(word) and word not in self.container:
                self = self + word            
            return
        
        for i in range(97,123):
            word = word + chr(i)
            self.__count_words_rek(n-1,word,valid_list)
            word = word[0:len(word)-1]
    
    # Returns length
    def __len__(self):
        return len(self.container)
    
    # Returns String representation of list
    def __str__(self):
        return str(self.container)
    
    # Returns whether this word is valid or not
    def valid_word(self,word):
        url = URL_word(word)
        response = Response(url)
        return len(response['synsets']) != 0
        
    __count_words_rek = count_words_rek #private


n = 3        
valid_list = Valid_List(n)
valid_list.count_words()
print("%d/%d"%(len(valid_list),26**n))
print(valid_list)