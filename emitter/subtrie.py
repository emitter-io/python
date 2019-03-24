class SubTrieNode:
    def __init__(self, parent, word, handler):
        self.parent = parent
        self.word = word
        self.children = {}
        self.handler = handler

class SubTrie:
    def __init__(self):
        self.root = SubTrieNode(None, None, None)

    def _getWords(self, topic):
        return filter(None, topic.split("/"))
    
    def insert(self, topic, handler):
        curNode = self.root
        for word in self._getWords(topic):
            if word not in curNode.children:
                curNode.children[word] = SubTrieNode(curNode, word, None)
            curNode = curNode.children[word]
        curNode.handler = handler

    def _lookup(self, route, children):
        handlers = []

        if len(route) == 0:
            return handlers

        if route[0] in children:
            if children[route[0]].handler != None:
                handlers.append(children[route[0]].handler)
            handlers = handlers + self._lookup(route[1:], children[route[0]].children)
        
        if "+" in children:
            if children["+"].handler != None:
                handlers.append(children["+"].handler)
            handlers = handlers + self._lookup(route[1:], children["+"].children)
        
        return handlers

    def lookup(self, topic):
        route = list(self._getWords(topic))
        return self._lookup(route, self.root.children)
    
    def delete(self, topic):
        curNode = self.root
        for word in self._getWords(topic):
            if word not in curNode.children:
                return
            curNode = curNode.children[word]

        curNode.handler = None
        
        while curNode.handler == None and len(curNode.children) == 0:
            del curNode.parent.children[curNode.word]
            curNode = curNode.parent

        return


t = SubTrie()
t.insert("a/", lambda: print("Handler a"))
t.insert("a/b/c/", lambda: print("Handler a/b/c"))
t.insert("a/+/c/", lambda: print("Handler a/+/c"))

results = t.lookup("a/b/c")
print(len(results))

for r in results:
    r()