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
    def generate_graph(self, filename: str):
        # Read text from file and tokenize.
        with open(filename, "r") as fp:
            self.language: MarkovLanguage = load(fp)

        corpus = list()
        for word in self.language["text"].lower().split(" "):
            corpus.append([x for x in word])

        self.generator = markovify.Text(None, parsed_sentences=corpus,
                                        state_size=3)

    def generate_word(self, seed: str = None):
        if "dictionary" in self.language.keys():
            if seed.lower() in self.language["dictionary"]:
                return self.language["dictionary"][seed.lower()]

        if seed is not None:
            random.seed(seed)
        word = None
        while word is None:
            word = self.generator.make_sentence()

        return word.replace(" ", "")


def aparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("lang", help="Language file to use", type=str)
    parser.add_argument("--text", help="Text to use as base", type=str)

    return parser


if __name__ == "__main__":
    markov = MarkovNameGen()
    parser = aparse()
    args = parser.parse_args()
    TEXT = args.text
    LANG = args.lang
    markov.generate_graph(LANG)

    words = list()
    if TEXT is not None:
        TEXTSPLIT = TEXT.split(" ")
        for i in TEXTSPLIT:
            words.append(markov.generate_word(i))
    else:
        words.append(markov.generate_word())

    print(" ".join(words))
