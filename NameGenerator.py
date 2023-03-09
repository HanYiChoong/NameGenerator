"""Credit Martin O'Leary https://mewo2.com/notes/naming-language/"""


from json import load
from random import Random
import argparse
from typing import TypedDict

DEFAULTORTHO = {
    "ʃ": "sh",
    "ʒ": "zh",
    "ʧ": "ch",
    "ʤ": "j",
    "ŋ": "ng",
    "j": "y",
    "x": "kh",
    "ɣ": "gh",
    "ʔ": "‘",
    "A": "á",
    "E": "é",
    "I": "í",
    "O": "ó",
    "U": "ú",
}


class Language(TypedDict):
    phonemes: dict[str, str]
    # weights: dict[str, list[int]]
    structure: str
    ortho: dict[str, str]
    minSyll: int
    maxSyll: int
    minChar: int
    maxChar: int
    dictionary: dict[str, str]


class WordGenerator:
    def __init__(self, languageFile: str) -> None:
        self.rng = Random()

        self.language = self.readLanguage(languageFile)

    def makeSyllable(self) -> str:
        syll = ""
        STRUCTURE = self.language["structure"]
        for i in range(len(STRUCTURE)):
            if STRUCTURE[i] == "?":
                if self.rng.random() < 0.5:
                    break
                else:
                    continue
            ptype = STRUCTURE[i]
            syll += self.rng.choice(self.language["phonemes"][ptype])
        return syll

    def makeWord(self, wordSeed=""):
        if "dictionary" in self.language.keys() and wordSeed.lower() in self.language["dictionary"].keys():
            return self.language["dictionary"][wordSeed.lower()]

        if wordSeed != "":
            self.rng.seed(wordSeed)
        nsylls = self.rng.randint(self.language["minSyll"], self.language["maxSyll"])
        word = ""
        while (
            len(word) < self.language["minChar"] or len(word) > self.language["maxChar"]
        ):
            word = ""
            for _ in range(nsylls):
                word += self.spell(self.makeSyllable())
        return word

    def spell(self, syll: str) -> str:
        s = ""
        for i in syll:
            if i in self.language["ortho"].keys():
                s += self.language["ortho"][i]
            elif i in DEFAULTORTHO.keys():
                s += DEFAULTORTHO[i]
            else:
                s += i

        return s

    def readLanguage(self, filename: str) -> Language:
        with open(filename, "r", encoding="utf-8") as fp:
            data = load(fp)
        return data


def aparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("lang", help="Language to use", type=str)
    parser.add_argument("--text", help="Text to use as base", type=str)

    return parser


if __name__ == "__main__":
    parser = aparse()
    args = parser.parse_args()
    TEXT = args.text
    LANG = args.lang
    wordGen = WordGenerator(LANG)
    words = list()
    if TEXT is not None:
        TEXTSPLIT = TEXT.split(" ")
        for i in TEXTSPLIT:
            words.append(wordGen.makeWord(i))
    else:
        words.append(wordGen.makeWord())

    print(" ".join(words))
