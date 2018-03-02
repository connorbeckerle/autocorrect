'''Created on Mar 24, 2017

@author: conno
'''
import timeit
import random
import time

from triesearch import trie
from triesearch import trienode
from triesearch import worddata
from triesearch import debug

def test_best_corr():
    atrie = trie.Trie()
    atrie.build_from_trie('../data/Word Frequency Dictionary - Full - trieform.txt')
    print atrie.get_best_correction('str')
    
#test_best_corr()

def _get_random_letter():
    return chr(random.randint(97, 122))

def fuzzy_search_thorough_test():
    TEST_WORD_COUNT = 100
    WORD_ERR_COUNT_EA_TYPE = 5
    MAX_K = 2
    dictfile = '../data/Word Dictionary.txt'
    this_trie = trie.Trie()
    word_list = []
    dict = {}
    dot = debug.ScrDots(1, 10)
    
    with open(dictfile , 'r') as f:
        for ln in f:
            word_list.append(ln.strip())
            
    for word in word_list:
        this_trie.insert(this_trie.rootNode, word, None)
        
    word_list = word_list[:TEST_WORD_COUNT]
    
    # confusing structure:
    # dict contains all the words as keys.
    # each entry is a dict with key 1 - MAX_K
    # each of those dict entries is a list of err_words with that many errors in them
    for word in word_list:
        dot.ping()
        dict[word] = {} # list of error lists
        dict[word][1] = []
        for i in range(WORD_ERR_COUNT_EA_TYPE):
            # insertion
            pos = random.randint(0, len(word))
            dict[word][1].append(word[:pos] + _get_random_letter() + word[pos:])
            # deletion
            pos = random.randint(0, len(word) - 1)
            dict[word][1].append(word[:pos] + word[pos+1:])
            # substitution
            pos = random.randint(0, len(word) - 1)
            dict[word][1].append(word[:pos] + _get_random_letter() + word[pos+1:])
            # transposition
            if len(word) >= 2:
                pos = random.randint(0, len(word) - 2)
                dict[word][1].append(word[:pos] + word[pos+1] + word[pos] + word[pos+2:])
                
        for k in range(2, MAX_K+1):
            dict[word][k] = []
            for i in range(WORD_ERR_COUNT_EA_TYPE):
                # insertion
                err_word = dict[word][k-1][random.randint(0, len(dict[word][k-1])-1)]
                pos = random.randint(0, len(err_word))
                dict[word][k].append(err_word[:pos] + _get_random_letter() + err_word[pos:])
                # deletion
                err_word = dict[word][k-1][random.randint(0, len(dict[word][k-1])-1)]
                if len(err_word) >= 1:
                    pos = random.randint(0, len(err_word) - 1)
                    dict[word][k].append(err_word[:pos] + err_word[pos+1:])
                # substitution
                err_word = dict[word][k-1][random.randint(0, len(dict[word][k-1])-1)]
                if len(err_word) >= 1:
                    pos = random.randint(0, len(err_word) - 1)
                    dict[word][k].append(err_word[:pos] + _get_random_letter() + err_word[pos+1:])
                # transposition
                err_word = dict[word][k-1][random.randint(0, len(dict[word][k-1])-1)]
                if len(err_word) >= 2:
                    pos = random.randint(0, len(err_word) - 2)
                    dict[word][k].append(err_word[:pos] + err_word[pos+1] + err_word[pos] + err_word[pos+2:])
        
    count = 0
    err_count = 0
    start_time = time.time()
    orig_time = start_time
    count_start = 0
    for word in dict.keys():
        for k in dict[word].keys():
            for err_word in dict[word][k]:
                count += 1
                result_list = this_trie.get_fss_results(err_word, k, None)
                if not result_list.contains(word):
                    print 'ERROR:'
                    print '\terr_word: ' + err_word
                    print '\tword: ' + word
                    print '\tk: ' + str(k)
                    err_count += 1
        count_amt = count-count_start
        time_amt = time.time()-start_time
        print '\n\n' + str(count_amt) + ' words in ' + str(time_amt) + ' seconds (' + str(time_amt/count_amt) + ' sec/word)'
        count_start = count
        start_time = time.time()
        
    print str(err_count) + ' errors in ' + str(count) + ' tests.'
    print 'avg: ' + str((time.time()-orig_time)/count) + ' sec/word'
    
#fuzzy_search_thorough_test()


def test_import_trie():
    triefile = '../data/Word Frequency Dictionary - Full - trieform.txt'
    trie_trie = trie.Trie()
    trie_trie.build_from_trie(triefile)
    
def test_import_dict():
    dictfile = '../data/Word Frequency Dictionary.txt'
    dict_trie = trie.Trie()
    dict_trie.build_from_dict(dictfile)
    
def test_time():
    
    a = timeit.Timer('testmisc2.test_import_trie()', 'import testmisc2\ngc.enable()')
    
    print a.timeit(1)
    
    b = timeit.Timer('testmisc2.test_import_dict()', 'import testmisc2\ngc.enable()')
    
    print b.timeit(1)
    
#test_time()
    
def interactive_exactsearch_test():
    
    this_trie = trie.Trie()
    print 'starting...'
    while True:
        input = raw_input()
        if input == '': continue
        insplit = input.split()
        if input == '-disp':
            this_trie.print_structure()
        elif insplit[0] == 'cont':
            print this_trie.contains(insplit[1], this_trie.rootNode)
        elif insplit[0] == 'add':
            this_trie.insert(insplit[1], worddata.WordData(), this_trie.rootNode)
            print 'added'
        else:
            print 'unrecognized input'
        

def check_file_equiv(f1, f2):
    import filecmp
    print filecmp.cmp(f1, f2, shallow=False)
    
def test_string_iteration():
    
    str = 'abcZdefgh'
    str2 = 'abcdefgh'
    
    # compare word, data in node letter-by-letter
    for i, (char_w, char_d) in enumerate(zip(str, str2)):
        
        # if different, need to split this node
        if char_w != char_d:
            print str2[:i] + " - " + str2[i:]
            return

def test_print():
        
    testcls = trie.Trie()
    
    testcls.print_structure()
    
    outfile = '../output/out.txt'
    
    testcls.print_structure(outfile)
    
#node = trienode.TrieNode("str")

# val = node.get_child("something")
# print val
# print "yay"
# print "uh"



    
    
#test_string_iteration()
#test_trie_insert()
#test_trie_insert2()
#interactive_exactsearch_test()

