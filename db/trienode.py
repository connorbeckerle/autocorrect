'''Created on Mar 24, 2017

@author: conno
'''

from err import NoSuchChildError, InvalidArgError

class TrieNode(object):
    '''One node of the prefix trie.

    ATTRs:
        child_nodes: dict containing {first letter of each child's data, each child}
        data: data string in this node
        metadata: optional metadata. Metadata is only for terminal nodes
    '''


    def __init__(self, data, metadata=None):
        '''Instantiate TrieNode with blank child_nodes dict

        :param data: data string in this node
        :param metadata: optional metadata. Metadata is only for terminal nodes
        '''
        self.child_nodes = {}
        self.data = data # string data in this node
        self.metadata = metadata # word.WordData obj, only if terminal
 
    def set_child(self, child_node):
        '''Set a new child node for this node.

        The first char of the child node's data is the its key.
        :param child_node: child node to set.
        '''
        if not isinstance(child_node, TrieNode):
            raise InvalidArgError(child_node)
        key = child_node.data[:1]
        self.child_nodes[key] = child_node
                
    def get_key(self):
        '''Get this node's key.

        :returns the key of this node - the first char of its data.
        '''
        return self.data[:1]
        
    def is_terminal(self):
        '''Check if this node is terminal.

        :returns True if terminal (last char is ascii char 0, False if not.
        '''
        return self.data[-1] == chr(0)
    
    def has_child_suffix(self, suffix):
        '''Check if this node has a child node corresponding to the given suffix.

        :param suffix: suffix to check for.
        :returns True or False
        '''
        return self.child_nodes.has_key(suffix[:1])
        
    def get_child(self, suffix):
        '''Get the child node for a given suffix.

        :param suffix: suffix of node to get.
        '''
        if not self.has_child_suffix(suffix):
            raise NoSuchChildError(suffix[:1])
        else:
            return self.child_nodes.get(suffix[:1])
    
    
    
