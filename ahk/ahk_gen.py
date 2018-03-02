'''Builds ahk commands to make the ahk module

Created on Mar 24, 2017

@author: conno
'''

import trie, trienode
import sys
import debug

# get to this dir:
#TODO:
# backspace!
def genEndChar():
    d = {
        'Space': ' ',
        '-': '-', 
        '+;': ':', 
        "'": "'", 
        "+'": '""', 
        '/': '/', 
        '\\': '\\', 
        '.': '.', 
        ',': ',', 
        '+/': '?', 
        '+1': '!', 
        'Enter': '`n'}
    for char, char_to_send in d.iteritems():
        print '$'+char+'::'
        print '\tbuilder.execute("'+char_to_send+'")'
        print '\treturn'
        
def genCancelChar():
    l = ['LButton', 'RButton', 'Up', 'Down', 'Left', 'Right', 'Home',
         'End', '!Tab']
    for char in l:
        print '~'+char+'::'
        print '\tbuilder.wipe()'
        print '\treturn'

genEndChar()
genCancelChar()

        
def genUpper():
    for i in range(97, 123):
        print '~+'+chr(i)+'::'
        print '\tbuilder.tempDisable()'
        print '\treturn'

def genLower():
    for i in range(97, 123):
        print '~'+chr(i)+'::'
        print '\tbuilder.addLetter("'+chr(i)+'")'
        print '\treturn'

genLower()
genUpper()
