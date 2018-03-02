'''Provides a COM server setup to interact with ahk.

Created on Apr 2, 2017

@author: conno
'''

#import time
#import pythoncom
import win32com.server.register
from win32com.server.exception import COMException
import admin
import trie
import traceback

# MISC NOTES
# likely have to cast received strings with str()

#TODO:
# alt-tab should wipe in the AHK script
class COMServer:

    # note - these are comma-delimited
    # list of all method names exposed to COM
    _public_methods_ = ['ping', 'query', 'dumb_query', 'debug_mode']
    
    # list of all attribute names exposed to COM
    _public_attrs_ = []
    
    # list of all read-only exposed attributes
    _readonly_attrs_ = ['count']        
    
    # this server's CLS ID
    _reg_clsid_ = '{E88C95B9-B6BA-4365-BC3E-42C07E33B944}'
    
    # this server's (user-friendly) program ID
    _reg_progid_ = 'Python.AutoCorrectServer'
    
    # optional description
    _reg_desc_ = 'Autocorrection server!'
    
    def __init__(self):
        triefile = '../data/Word Frequency Dictionary - Full - trieform.txt'
        self.ac_trie = trie.Trie()
        self.ac_trie.build_from_trie(triefile)
        self.debug_mode_flag = False
        
    def ping(self):
        return "I'm alive!"
    
    def dumb_query(self, word):
        word = str(word)
        if self.debug_mode_flag:
            try:
                return word + word
            except Exception as e:
                with open('../error_log.txt', 'w') as f:
                    f.truncate()
                    f.write(traceback.format_exc())
                raise COMException(desc=repr(e))
        else:
            return word + word
    
    def debug_mode(self):
        #TODO:
        # this should not be a toggle.
        if self.debug_mode_flag:
            self.debug_mode_flag = False
            return 'Debugging disabled.'
        else:
            self.debug_mode_flag = True
            return 'Debugging enabled.'

    def query(self, word):
        word = str(word)
        if self.ac_trie.contains(word):
            return ''
        
        if self.debug_mode_flag:
            try:
                new_word = self.ac_trie.get_best_correction(word)
            except Exception as e:
                #TODO: this is dumb.
                with open('../error_log.txt', 'w') as f:
                    f.truncate()
                    f.write(traceback.format_exc())
                raise COMException(desc=repr(e))
        else:
            new_word = self.ac_trie.get_best_correction(word)
            
        if new_word == word:
            return ''
        else:
            return new_word
        
    @staticmethod
    def reg():
        win32com.server.register.UseCommandLine(COMServer)
        
    @staticmethod
    def unreg():
        if not admin.isUserAdmin():
            admin.runAsAdmin()
        win32com.server.register.UnregisterServer(COMServer._reg_clsid_, COMServer._reg_progid_)

            
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'Error: need to supply arg ("--register" or "--unregister")'
        sys.exit(1)
    elif sys.argv[1] == '--register':
        COMServer.reg()
    elif sys.argv[1] == '--unregister':
        print 'Starting to unregister...'    
        COMServer.unreg()
        print 'Unregistered COM server.'
    else:
        print 'Error: arg not recognized'
    
