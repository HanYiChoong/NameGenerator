"""
https://www.jeffcarp.com/posts/2019/markov-chain-python/
"""
import argparse
import random
from typing import Optional, TypedDict
from json import load
import markovify


class MarkovLanguage(TypedDict):
    minChar: int
    maxChar: int
    dictionary: Optional[dict[str, str]]
    text: str


class MarkovNameGen:
    def __init__(self, filename: str):
        # Read text from file and tokenize.
        with open(filename, "r") as fp:
            self.language: MarkovLanguage = load(fp)

        corpus = list()
        for word in self.language["text"].lower().split(" "):
            corpus.append([x for x in word])

        self.generator = markovify.Text(None, parsed_sentences=corpus,
                                        state_size=3)

    def generate_word(self, seed: str | None = None):
        if seed and self.language["dictionary"] and seed.lower() in self.language["dictionary"]:
            return self.language["dictionary"][seed.lower()]

        if seed is not None:
            random.seed(seed)
        word = None
        while word is None:
            word = self.generator.make_sentence()

        return word.replace(" ", "")
    
class MarkovAddWord:
    def __init__(self, filename: str):
        with open(filename, "r") as fp:
            self.language: MarkovLanguage = load(fp)
    
    def add_word(self, text: str, word: str) -> int:
        """Adds a word to the dictionary.

        Args:
            text (str): English text to base the word around.
            word (str): Word to add.

        Returns:
            int: Provides error codes. 0: Added without issue. 1: No dictionary present. 2: English text already exists. 3: More than one word provided.
        """
        if not self.language["dictionary"]:
            return 1
        word_counts = len(text.split(" "))
        if (word_counts != 1):
            return 3
        if text in self.language["dictionary"]:
            return 2
        self.language["dictionary"][text] = word
        return 0
    

def aparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("lang", help="Language file to use.", type=str)
    parser.add_argument("--text", help="Text to use as base.", type=str)
    parser.add_argument("--add", help="Con-word to add using text provided. Only 1 word allowed.", type=str)

    return parser


if __name__ == "__main__":
    parser = aparse()
    args = parser.parse_args()
    TEXT = args.text
    LANG = args.lang
    ADD_WORD = args.add

    if ADD_WORD:
        add_gen = MarkovAddWord(LANG)
        success_rate = add_gen.add_word(TEXT, ADD_WORD)
        if (success_rate == 0):
            print("{}: {} added successfully!".format(TEXT, ADD_WORD))
        if (success_rate == 1):
            print("Provided language file has no dictionary!")
        if (success_rate == 2):
            print("Provided English text already exists!")
        if (success_rate == 3):
            print("More than one word provided!")
    else:
        markov = MarkovNameGen(LANG)

        words = list()
        if TEXT is not None:
            TEXTSPLIT = TEXT.split(" ")
            for i in TEXTSPLIT:
                words.append(markov.generate_word(i))
        else:
            words.append(markov.generate_word())

        print(" ".join(words))
