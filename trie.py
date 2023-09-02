class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

    # finds words that start with prefix
    def search_all(self, prefix):
        node = self.root
        suggestions = []  # pass by reference
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        self.find_words(node, prefix, suggestions)
        return suggestions

    # recursive helper function for search_all
    def find_words(self, node, prefix, suggestions):
        if node.is_word:
            suggestions.append(prefix)
        for char in node.children:
            self.find_words(node.children[char], prefix + char, suggestions)
