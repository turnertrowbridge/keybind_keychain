class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_word = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_word

    # finds words that start with prefix
    def search_all(self, prefix):
        found_words = []
        node = self.root
        for c in prefix:
            if c not in node.children:  # pass by reference
                return []
            node = node.children[c]
        self.search_all_dfs(node, prefix, found_words)
        return found_words

    # recursive helper function for search_all
    def search_all_dfs(self, node, prefix, found_words):
        if node.is_word:
            found_words.append(prefix)
        for c in node.children:
            self.search_all_dfs(node.children[c], prefix + c, found_words)


