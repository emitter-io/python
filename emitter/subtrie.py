class SubTrieNode:
    def __init__(self, parent, word, handler):
        self.parent = parent
        self.word = word
        self.children = {}
        self.handler = handler

class SubTrie:
    def __init__(self):
        self.root = SubTrieNode(None, None, None)

    @staticmethod
    def _get_words(topic):
        return filter(None, topic.split("/"))
    
    def insert(self, topic, handler):
        cur_node = self.root
        for word in self._get_words(topic):
            if word not in cur_node.children:
                cur_node.children[word] = SubTrieNode(cur_node, word, None)
            cur_node = cur_node.children[word]
        cur_node.handler = handler

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
        route = list(self._get_words(topic))
        return self._lookup(route, self.root.children)
    
    def delete(self, topic):
        cur_node = self.root
        for word in self._get_words(topic):
            if word not in cur_node.children:
                return
            cur_node = cur_node.children[word]

        cur_node.handler = None
        
        while cur_node != self.root and cur_node.handler == None and len(cur_node.children) == 0:
            del cur_node.parent.children[cur_node.word]
            cur_node = cur_node.parent

        return