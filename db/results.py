'''Created on Mar 30, 2017

@author: conno
'''

import operator

class ResultList(object):
    '''Dict of result dictionary words for a query.'''

    def __init__(self):
        '''Constructor'''
        self.result_dict = {}
        
    def _keep_best(self, first, second):
        '''Return result with lowest k value.

        :param first:
        :param second:
        '''
        if len(first.errors) <= len(second.errors):
            return first
        else:
            return second
        
    def add(self, new_result):
        '''Add a new result to the list, replacing a duplicate if necessary.'''
        if new_result.data in self.result_dict:
            old_result = self.result_dict[new_result.data]
            self.result_dict[new_result.data] = self._keep_best(old_result, new_result)
        else:
            self.result_dict[new_result.data] = new_result
            
    def contains(self, word):
        return word in self.result_dict

    def sort_results(self):
        '''Return a sorted list of Results
        '''
        d = self.result_dict.itervalues()
        results = sorted(d, key=operator.attrgetter('error_count'))
        return results

    
    def get_best(self):
        #TODO:
        # this should use sqrt(score) for edit distance = 2, not just score
        if self.result_dict:
            best_score = 0
            best_result = None
            for key, result in self.result_dict.iteritems():
                if result.metadata is not None:
                    if result.metadata.count > best_score:
                        best_result = result
                        best_score = best_result.metadata.count
            if best_result is not None:
                return best_result
            else:
                #TODO:
                # this is a terrible way to handle the issue that sometimes 
                # metadata is none.
                # Instead, I should just enforce having metadata wtih default 0
                # or something.
                for key, result in self.result_dict.iteritems():
                    return result
        else:
            return None
        
class Result(object):    
    '''Stores the result for one potential correct word.
    
    ATTRs:
        data: string data (the dict word this result represents)
            - built recursively with append()
        errors: list of consecutive error types
            - built recursively
        error_count: number of non-'continue' errors
        metadata: word metadata object.
            - added at end
    '''
    def __init__(self, prev_result=None, err_type=None):
        '''Create a new result, either from scratch or building an old one.

        :param prev_result: previous result to concatenate onto
        :param err_type: type of error causing this result
            should be one of: 'deletion', 'substitution', 'transposition', 'continue'
        '''
        #TODO: expand to have # of each type
        #TODO: make err_type required
        if prev_result == None:
            self.data = ''
            self.errors = []
            self.error_count = 0
        else:
            self.errors = list(prev_result.errors)
            self.data = prev_result.data
            self.error_count = prev_result.error_count
            if err_type:
                self.errors.append(err_type)
            if err_type != 'continue':
                self.error_count += 1
            
        
    def add_node(self, node):
        '''Appends the string in this node, and if node is terminal, adds its
        metadata.

        :param node: node appending
        '''
        self.data += node.data
        if node.is_terminal():
            self.metadata = node.metadata
