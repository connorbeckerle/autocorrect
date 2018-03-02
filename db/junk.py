
# fss_4 - before removal of dbo stuff
    def fss_4(self, node, word, pos, result, result_list, k, alrdy_trans=False):
        '''recursive function to do search work
        '''
        #DEBUG:
        if dbo:
        
        if node.data[pos:] == word:
            # we found a match! Also we must be on a leaf, so nowhere to go
            result.data += node.data[pos:-1]
            result.metadata = node.metadata
            result_list.add(result)
            if dbo: 
                self.dbp('ADDED: ' + result.data, dbo)
                self.dbp('errs:', dbo)
                for err in result.errors:
                    self.dbp('\t' + err, dbo)
                self.dbp('', dbo)
            return
            
        # need to add current char to result
        result.data += node.data[pos]
        
        # two cases depending on if at end of current node or not
        if pos >= (len(node.data)-1): # if at end of node
            for next_char, next_node in node.child_nodes.iteritems():
                if k > 0:
                    # DELETION:
                    if dbo: self.dbp('deletion-', dbo)
                    new_result = results.Result(result, 'deletion')
                    self.fss_4(next_node, word, 0, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))                
                    # SUBSTITUTION:
                    if len(word) > 0 and node.data[pos] != word[0]:
                        if dbo: self.dbp('substitution-', dbo)
                        new_result = results.Result(result, 'substitution')
                        self.fss_4(next_node, word[1:], 0, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))
                # CORRECT:
                if len(word) > 0 and node.data[pos] == word[0]:
                    if dbo: self.dbp('continue-', dbo)
                    new_result = results.Result(result, 'continue')
                    self.fss_4(next_node, word[1:], 0, new_result, result_list, k, dbo=debug.DebugObj.newdbo(dbo, '  '))
        else: # if not at end of node
            if k > 0:
                # DELETION:
                if dbo: self.dbp('deletion-', dbo)
                new_result = results.Result(result, 'deletion')
                self.fss_4(node, word, pos+1, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))                
                # SUBSTITUTION:
                if  len(word) > 0 and node.data[pos] != word[0]:
                    if dbo: self.dbp('substitution-', dbo)
                    new_result = results.Result(result, 'substitution')
                    self.fss_4(node, word[1:], pos+1, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))
            # CORRECT:
            if len(word) > 0 and node.data[pos] == word[0]:
                if dbo: self.dbp('continue-', dbo)
                new_result = results.Result(result, 'continue')
                self.fss_4(node, word[1:], pos+1, new_result, result_list, k, dbo=debug.DebugObj.newdbo(dbo, '  '))
        if k > 0:
            # INSERTION - doesn't step forward so doesn't matter which if 
            #     we are at the end of a node or not
            if dbo: self.dbp('insertion-', dbo)
            new_result = results.Result(result, 'insertion')
            new_result.data = new_result.data[:-1]
            self.fss_4(node, word[1:], pos, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))
            # TRANSPOSITION - same:
            if not alrdy_trans and len(word) >= 2:
                if dbo: self.dbp('transposition-', dbo)
                new_word = word[1] + word[0] + word[2:]
                new_result = results.Result(result, 'transposition')
                new_result.data = new_result.data[:-1]
                self.fss_4(node, new_word, pos, new_result, result_list, k-1, alrdy_trans=True, dbo=debug.DebugObj.newdbo(dbo, '  '))
    


            
    # fss_3 - was replaced by fss_4
    def fss_3(self, node, word, pos, result, result_list, k, alrdy_trans=False, dbo=None):
        '''(fuzzy_search_simple_3) - DEPRECATED
        '''
        
        #DEBUG:
        if dbo:
            self.dbp('k = ' + str(k), dbo)
            self.dbp('node: ' + node.data[pos:], dbo)
            self.dbp('word: ' + word, dbo)
            self.dbp('result so far: ' + result.data, dbo)
            self.dbp('', dbo)
            
        # if at end of word, done:
        if len(node.data) > 0 and node.data[pos] == self.chr0:
            if len(word) == 1 and word[0] == self.chr0:
                result.metadata = node.metadata
                if dbo: 
                    self.dbp('ADDED: ' + result.data, dbo)
                    self.dbp('errs:', dbo)
                    for err in result.errors:
                        self.dbp('\t' + err, dbo)
                    self.dbp('', dbo)
                result_list.add(result)
                return
        # need to add to result
        if len(node.data) > 0: 
            result.data += node.data[pos]
        
        # two cases depending on if at end of current node or not
        if pos >= (len(node.data)-1): # if at end of node
            for next_char in node.child_nodes:
                if k > 0:
                    # DELETION:
                    if dbo: self.dbp('deletion-', dbo)
                    new_result = results.Result(result, 'deletion')
                    self.fss_3(node.get_child(next_char), word, 0, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))                
                    # SUBSTITUTION:
                    if len(node.data) > 0 and len(word) > 0 and node.data[pos] != word[0]:
                        if dbo: self.dbp('substitution-', dbo)
                        new_result = results.Result(result, 'substitution')
                        self.fss_3(node.get_child(next_char), word[1:], 0, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))
                # CORRECT:
                if len(node.data) > 0 and len(word) > 0 and node.data[pos] == word[0]:
                    if dbo: self.dbp('continue-', dbo)
                    new_result = results.Result(result, 'continue')
                    self.fss_3(node.get_child(next_char), word[1:], 0, new_result, result_list, k, dbo=debug.DebugObj.newdbo(dbo, '  '))
        else: # if not at end of node
            if k > 0:
                # DELETION:
                if dbo: self.dbp('deletion-', dbo)
                new_result = results.Result(result, 'deletion')
                self.fss_3(node, word, pos+1, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))                
                # SUBSTITUTION:
                if len(node.data) > 0 and len(word) > 0 and node.data[pos] != word[0]:
                    if dbo: self.dbp('substitution-', dbo)
                    new_result = results.Result(result, 'substitution')
                    self.fss_3(node, word[1:], pos+1, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))
            # CORRECT:
            if len(node.data) > 0 and len(word) > 0 and node.data[pos] == word[0]:
                if dbo: self.dbp('continue-', dbo)
                new_result = results.Result(result, 'continue')
                self.fss_3(node, word[1:], pos+1, new_result, result_list, k, dbo=debug.DebugObj.newdbo(dbo, '  '))
        if k > 0:
            # INSERTION - doesn't step forward so doesn't matter which case:
            if dbo: self.dbp('insertion-', dbo)
            new_result = results.Result(result, 'insertion')
            new_result.data = new_result.data[:-1]
            self.fss_3(node, word[1:], pos, new_result, result_list, k-1, dbo=debug.DebugObj.newdbo(dbo, '  '))
            # TRANSPOSITION - same:
            if not alrdy_trans and len(word) >= 2:
                if dbo: self.dbp('transposition-', dbo)
                new_word = word[1] + word[0] + word[2:]
                new_result = results.Result(result, 'transposition')
                new_result.data = new_result.data[:-1]
                self.fss_3(node, new_word, pos, new_result, result_list, k-1, alrdy_trans=True, dbo=debug.DebugObj.newdbo(dbo, '  '))
            
        
