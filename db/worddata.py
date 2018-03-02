'''
Created on Mar 24, 2017

@author: conno
'''

class WordData(object):
    '''Represents data associated with word (e.g., usage)

    Currently is just the word.
    '''

    #TODO - consider alternative measure for recursive trie functions
    # currently build string iteratively. Why not just track an index
    # of the string in here?
    

    def __init__(self, count=None):
        '''
        Constructor
        '''
        self.count = count
                
    def print_data(self):
        return '^' + str(self.count)
    
    
def create_from_string(data_str):
    data_list = data_str.split('^')
    data_list.pop(0)
    return WordData(*data_list)
