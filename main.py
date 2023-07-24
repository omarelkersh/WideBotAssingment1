class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class SpellChecker:
    def __init__(self, dictionary_file):
        self.root = TrieNode()
        self.load_dictionary(dictionary_file)


    def load_dictionary(self, dictionary_file):
        try:
            with open(dictionary_file, 'r', encoding='utf-8-sig') as file:
                words = file.read().splitlines()
        except UnicodeDecodeError:
            with open(dictionary_file, 'r', encoding='latin-1') as file:
                words = file.read().splitlines()

        for word in words:
            self.add_word(word)

    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def find_nearest_words(self, word):
        def dfs(node, current_word, distance):
            if node.is_end_of_word and current_word != word:
                candidates.append((current_word, distance))
            if not node.children:
                return
            for char in node.children:
                dfs(node.children[char], current_word + char, distance + 1)

        def lexicographic_sort(word_list):
            return sorted(word_list, key=lambda x: (x[1], x[0]))[:4]

        node = self.root
        candidates = []
        for char in word:
            if char not in node.children:
                # Handle the case when the input word is not present in the dictionary
                dfs(node, word, 0)
                return lexicographic_sort(candidates)
            node = node.children[char]
        if node.is_end_of_word  and word != "":
            candidates.append((word, 0))
        dfs(node, word, 0)

        # Handle the case when no similar words are found in the dictionary
        if not candidates:
            dfs(self.root, '', 0)
            return lexicographic_sort(candidates)

        return lexicographic_sort(candidates)

    def add_to_dictionary(self, word):
        self.add_word(word)

# Example usage:
if __name__ == "__main__":
    dictionary_file = "dictionary.txt"
    spell_checker = SpellChecker(dictionary_file)

    # Find nearest 4 words for a given input word
    input_word = "apple"
    nearest_words = spell_checker.find_nearest_words(input_word)
    print(f"Nearest words to '{input_word}': {nearest_words}")

    input_word = "wrod"
    nearest_words = spell_checker.find_nearest_words(input_word)
    print(f"Nearest words to '{input_word}': {nearest_words}")

    # Add a word to the dictionary
    new_word = "example"
    spell_checker.add_to_dictionary(new_word)
    print(f"'{new_word}' added to the dictionary.")

