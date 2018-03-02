'''Contains helper debugging objects

Created on Mar 30, 2017

@author: conno
'''

from __future__ import print_function

class DebugObj(object):
    '''Helper class for debugging.
    '''


    def __init__(self, prev_dbo=None, addition=''):
        '''Constructor
        '''
        
        if prev_dbo:
            self.str=prev_dbo.str + addition
        else:
            self.str= ''
    
    @classmethod
    def newdbo(self, prev_dbo=None, addition=''):
        if prev_dbo:
            return DebugObj(prev_dbo, addition)
        else:
            return None
        
class ScrDots(object):
    '''Prints dots to the screen to display progress of some process as it chugs along.
    '''

    def __init__(self, dot_interval=1000, num_interval=10000):
        self.count = 0
        self.num_count = 0
        self.dot_interval = dot_interval
        self.num_interval = num_interval
        self.PRINT_WIDTH = 80
        self.newline_interval = dot_interval * self.PRINT_WIDTH
        
    def ping(self):
        self.count += 1
        if self.count % self.newline_interval == 0:
            print('')
        if self.count % self.num_interval == 0:
            self.num_count += 1
            print(self.num_count, end='')
        elif self.count % self.dot_interval == 0:
            print('.', end='')
