"""
https://www.jeffcarp.com/posts/2019/markov-chain-python/
"""
import argparse
from typing import Optional, TypedDict
import numpy as np
from collections import defaultdict
from json import load


class MarkovLanguage(TypedDict):
    minChar: int
    maxChar: int
    dictionary: Optional[dict[str, str]]
    text: str


class MarkovNameGen:
    def _walk_graph(self, graph, distance=5, start_node=None) -> list[str]:
        """Returns a list of words from a randomly weighted walk."""
        if distance <= 0:
            return []

        # If not given, pick a start node at random.
        if not start_node:
            start_node = self.rng.choice(list(graph.keys()))

        weights = np.array(
            list(self.markov_graph[start_node].values()), dtype=np.float64
        )
        # Normalize word counts to sum to 1.
        weights /= weights.sum()

        # Pick a destination using weighted distribution.
        choices = list(self.markov_graph[start_node].keys())
        chosen_word = self.rng.choice(choices, None, p=weights)

        return [chosen_word] + self._walk_graph(
            graph, distance=distance - 1, start_node=chosen_word
        )

    def generate_graph(self, filename: str):
        # Read text from file and tokenize.
        with open(filename) as fp:
            self.language: MarkovLanguage = load(fp)
        tokenized_text = [letter for letter in self.language["text"]]

        # Create graph.
        self.markov_graph = defaultdict(lambda: defaultdict(int))

        last_letter = tokenized_text[0].lower()
        for letter in tokenized_text[1:]:
            if letter == " ":
                continue
            letter = letter.lower()
            self.markov_graph[last_letter][letter] += 1
            last_letter = letter

    def convert_to_number(self, string: str) -> int:
        return int.from_bytes(string.encode(), "little")

    def generate_word(self, seed: str = None):
        if "dictionary" in self.language.keys():
            if seed.lower() in self.language["dictionary"]:
                return self.language["dictionary"][seed.lower()]

        if seed is not None:
            self.rng = np.random.default_rng(self.convert_to_number(seed))
        minChar = self.language["minChar"]
        maxChar = self.language["maxChar"]
        distance = int((maxChar - minChar) * self.rng.random() + minChar)
        return "".join(self._walk_graph(self.markov_graph, distance=distance))


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
