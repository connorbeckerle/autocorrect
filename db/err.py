'''Created on Mar 25, 2017

@author: conno
'''

class NoSuchChildError(Exception):
    '''
    '''


    def __init__(self, key):
        '''Constructor
        '''
        self.key = key
        
class InvalidArgError(Exception):
    '''
    '''
    
    
    def __init__(self, arg):
        '''Constructor
        '''
        self.arg = arg
