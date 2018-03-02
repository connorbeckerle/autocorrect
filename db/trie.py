'''Created on Mar 24, 2017

@author: conno
'''

import pdb

import sys
import string
#from __builtin__ import None

import trienode
import worddata
import results


class Trie(object):
    '''A prefix trie representing one dictionary of correct words.

    This class is just a pointer to the root node with methods for operating on it.

    USEFUL PUBLIC METHODS:
        build_from_dict()
        build_from_trie()
        print_structure()
        contains()
        get_best_correction()
        get_potential_words()

    ATTRs:
        rootnode: root node of trie. is blank.
    '''
    
    # limitations:
    # can not figure out transpositions combined with another error (e.g. with a char inserted
    # in the middle, like trans >> tazrns)
    
    chr0 = chr(0)
    def get_best_correction(self, word):
        '''Return the best correction matching given input.

        Uses k=2.
        '''
        result_list = get_potential_words(word, k=2)
        best = result_list.get_best()
        if best:
            return best.data
        else:
            return ''
        
    def get_potential_words(self, word, k):
        '''Return a list of potential words matching input as a ResultList.

        :param word: input to find matches for
        :param k: maximum error numbers to search against (recommend 2 max)
        '''
        result_list = results.ResultList()
        startnode = self.rootNode
        word = word + self.chr0
        for key, next_node in startnode.child_nodes.iteritems():
            result = results.Result()
            self._fuzzy_search_r(next_node, word, 0, result, result_list, k)
        
        return result_list
    
    def dbp_state(self, k, node, word, pos, result):
        self.dbp('k = ' + str(k))
        self.dbp('node: ' + node.data[pos:])
        self.dbp('word: ' + word)
        self.dbp('result so far: ' + result.data)
        self.dbp('')

    def _fuzzy_search_r(self, node, word, pos, result, result_list, k, alrdy_trans=False):
        '''recursive function to do search work

        explanation:
            this performs a fuzzy search for correct words that match the given word input

        :param node: current trienode
        :param word: remainder of current word. ends in chr0
        :param pos: position in trienode data
        :param result: current built-up result (i.e. correct word)
        :param result_list: pointer to list of results
        :param k: allowed edits (total remaining)
        :param alrdy_trans: only allow one transposition
        '''
        pdb.set_trace()
        if node.data[pos:] == word:
            # we found a match! Also we must be on a leaf, so nowhere else to go
            result.data += node.data[pos:-1]
            result.metadata = node.metadata
            result_list.add(result)
            return
            
        # need to add current char to result
        result.data += node.data[pos]
        
        # for edits that advance along the trie, two cases depending on 
        # if at end of current node or not:
        if pos >= (len(node.data)-1): # if at end of node
            for next_char, next_node in node.child_nodes.iteritems():
                if k > 0:
                    # DELETION:
                    new_result = results.Result(result, 'deletion')
                    self._fuzzy_search_r(next_node, word, 0, new_result, result_list, k-1)
                    # SUBSTITUTION:
                    if len(word) > 0 and node.data[pos] != word[0]:
                        new_result = results.Result(result, 'substitution')
                        self._fuzzy_search_r(next_node, word[1:], 0, new_result, result_list, k-1)
                # CORRECT:
                if len(word) > 0 and node.data[pos] == word[0]:
                    new_result = results.Result(result, 'continue')
                    self._fuzzy_search_r(next_node, word[1:], 0, new_result, result_list, k)
        else: # if not at end of node
            if k > 0:
                # DELETION:
                new_result = results.Result(result, 'deletion')
                self._fuzzy_search_r(node, word, pos+1, new_result, result_list, k-1)
                # SUBSTITUTION:
                if  len(word) > 0 and node.data[pos] != word[0]:
                    new_result = results.Result(result, 'substitution')
                    self._fuzzy_search_r(node, word[1:], pos+1, new_result, result_list, k-1)
            # CORRECT:
            if len(word) > 0 and node.data[pos] == word[0]:
                new_result = results.Result(result, 'continue')
                self._fuzzy_search_r(node, word[1:], pos+1, new_result, result_list, k)
        if k > 0:
            # INSERTION - doesn't step forward so doesn't matter which if 
            #     we are at the end of a node or not
            new_result = results.Result(result, 'insertion')
            new_result.data = new_result.data[:-1]
            self._fuzzy_search_r(node, word[1:], pos, new_result, result_list, k-1)
            # TRANSPOSITION - same:
            if not alrdy_trans and len(word) >= 2:
                #TODO: why only allow one?
                new_word = word[1] + word[0] + word[2:]
                new_result = results.Result(result, 'transposition')
                new_result.data = new_result.data[:-1]
                self._fuzzy_search_r(node, new_word, pos, new_result, result_list, k-1, alrdy_trans=True)
    
    def _build_from_trie_recursive(self, data, metadata, node):
        '''Recursive helper for build_from_trie

        :param data: list of data strings
        :param metadata: metadata for this word
        :param node: current node
        '''
        curr_data = data[0]
        # base case - terminal node. If triefile has no dups, don't need to check if exists
        #TODO - check for dups and handle
        if len(data) == 1:
            node.set_child(trienode.TrieNode(curr_data, metadata))
        else:
            # if no appropriate child node, need to make one
            if not node.has_child_suffix(curr_data):
                node.set_child(trienode.TrieNode(curr_data))
            # recursive case: step into child node
            self._build_from_trie_recursive(data[1:], metadata, node.get_child(curr_data))
    
    def build_from_trie(self, trie_file):
        '''Build a trie from a trie file.

        Trie file specs:
            Each line represents a word.
            Words are tab-delimited (representing new nodes)
            Word text ends in a chr(0)
            After the chr(0) is a ^-delimited metadata list, beginning in a ^
            There should be no duplicates
        :param trie_file: file location
        '''
        #TODO: add a filetype validation line at the top?

        f = open(trie_file, 'r')
        
        for ln in f:
            ln_split = ln.split(chr(0))
            metadata = worddata.create_from_string(ln_split[1])
            data = ln_split[0] + chr(0)
            data_list = data.lstrip().split('\t')
            self._build_from_trie_recursive(data_list, metadata, self.rootNode)

    def build_from_dict(self, dict_file):
        '''Build the trie from a dict (newline-delimited list of words). 
        
        Extra data is optional.
        :param dict_file:
        '''
        
        f = open(dict_file, 'r')
        
        for ln in f:
            if '\t' in ln:
                split_ln = string.split(ln,'\t')
                #DEBUG:
                wd = split_ln[0]
                test_val = self.contains('pro')
                if wd == 'products': #or wd == 'product':
                    pass
                if wd == 'product':
                    pass
                self.insert(self.rootNode, split_ln[0], worddata.WordData(int(split_ln[1])))
            else:
                self.insert(self.rootNode, split_ln[0], worddata.WordData())
    
    def _print_recursive(self, f, word, node):
        '''Recursive print helper function.

        :param f:
        :param :
        :param node:
        '''        
        new_word = word + '\t' + node.data
        if node.is_terminal():
            f.write(new_word + node.metadata.print_data() + '\n')
        for key in sorted(node.child_nodes):
            self._print_recursive(f, new_word, node.child_nodes[key])

    def print_structure(self, outPath=''):
        '''Print the trie in trie file format, which is easy to read and to import.

        :param outPath: Optional file to print to. If empty, prints to console
        '''
        if outPath:
            f = open(outPath, 'w')
            
        else:
            f = sys.stdout
        
        for key in sorted(self.rootNode.child_nodes.keys()):
            self._print_recursive(f, '', self.rootNode.child_nodes[key])
    
    def insert(self, node, word, metadata):
        '''Insert word into existing trie.

        :param word: word to insert.
        :param metadata: metadata associated with word
        :param node: current node. call with self.rootNode.
        '''
        # first non-recursive call
        if node == self.rootNode:
            word = word + chr(0) # append termination char
            
        # base case - this has already been inserted, and this node exists
        if word == node.data:
            return
                
        # compare word, data in node letter-by-letter
        i = 0
        for char_w, char_d in zip(word, node.data):
            # base case - word differs from node.data
            # if different, need to split this node and set children. then done.
            # because of endchar, no complete path can be a subset of another;
            # so this will always be hit if they are not identical and/or one 
            # terminates.
            if char_w != char_d:
                # split current node
                new_split_node = trienode.TrieNode(node.data[i:], node.metadata)
                new_split_node.child_nodes = node.child_nodes
                node.child_nodes = {}
                node.set_child(new_split_node)
                node.data = node.data[:i]
                node.metadata = None
                # add new node
                node.set_child(trienode.TrieNode(word[i:], metadata))
                return
            i += 1
            
        # base case - has child(s) but no matching one
        if not node.has_child_suffix(word[i:]):
            #DEBUG:
            str_debug = word[i:]
            node.set_child(trienode.TrieNode(word[i:], metadata))
        # recursive case - child has node to follow through
        else:
            self.insert(node.get_child(word[i:]), word[i:], metadata)
        
    def _search_exact(self, node, word):
        '''Exact search recursive function.

        :param word: word to check
        :param node: current node. call with self.rootNode.
        :returns True or False
        '''
        # initial call
        if node == self.rootNode:
            word = word + chr(0)
            
        # base case - the word exists in this node
        if word == node.data:
            return True
            
        # compare word, node.data char-by-char
        i = 0
        for char_w, char_d in zip(word, node.data):
            # base case - they differ, word is not in dict
            if char_w != char_d:
                return False
            i += 1
            
        # now we are at end of node data but there is still some word left
        # base case - has child(s) but not matching one
        if not node.has_child_suffix(word[i:]):
            return False
        else:
            return self._search_exact(node.get_child(word[i:]), word[i:])
    
    def contains(self, word):
        '''Identify if trie contains word or not

        :param word: word to check
        :returns True or False
        '''
        return self._search_exact(self.rootNode, word)
    
    def dbp(self, text):
        '''debug print function
        '''
        print text 
        
    def __init__(self):
        '''Instantiate
        '''
        self.rootNode = trienode.TrieNode('')
    
        
