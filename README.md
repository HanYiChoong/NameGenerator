# NameGenerator
A generic fast conlang word generator for worldbuilding purposes.

# How to use
No additional python packages needed. Tested on Python > 3.9.

To use out of the box, you simply specify a language file and then optionally a seed word so you can get the same word consistently, as well as querying the dictionary.
```shell
python NameGenerator.py path/to/language/file [--text text-to-use-as-seed]
```

## Using without seed word
```shell
python NameGenerator.py .\languages\latin.json
> kulheiph
python NameGenerator.py .\languages\latin.json
> byshavug
python NameGenerator.py .\languages\latin.json
> weuz
```

## Using seed word
```shell
python NameGenerator.py .\languages\latin.json --text hello
> veimav
python NameGenerator.py .\languages\latin.json --text hello
> veimav
python NameGenerator.py .\languages\latin.json --text Hello
> ngiw
python NameGenerator.py .\languages\latin.json --text hElLo
> waelhago
```

## Using seed sentence
```shell
python NameGenerator.py .\languages\latin.json --text "hello there my friend"
> veimav fui bebihreu koegbad
```

## Using seed word with dictionary
If you have defined a word in the `latin.json` dictionary, the generator will ignore seed word casing.

`latin.json`
```json
"dictionary": {
    ...
    "hello": "waelha"
}
```
```shell
python NameGenerator.py .\languages\latin.json --text hello
> waelha
python NameGenerator.py .\languages\latin.json --text Hello
> waelha
python NameGenerator.py .\languages\latin.json --text hElLo
> waelha
python NameGenerator.py .\languages\latin.json --text "hello there my friend"
> waelha fui bebihreu koegbad
```

# Creating a new language
Generating a new language involves defining a .json file according to `language.schema`. Here are the following elements to include:
- `"phonemes"`: Types of phonemes in the language. Most have vowels and consonents, but your conlang might have something more (or less). Used to define syllable structure.
- `"structure"`: The structure of each syllable in your language. Commonly uses `CVC`. Using a `?` character, you can have the syllable receive a 50% chance of terminating at that phoneme. `CV?C` has a 50% chance of generating `CVC` and a 50% chance of `CV`.
- `"ortho"`: The orthography (spelling) of special phonemes in your language. Used to add in multi-letter phonemes to your language. Not necessary to use IPA notation. If you want, you can simply denote special phonemes using capital letters instead of small.
- `"maxChar"`: The longest word the generator will construct for your language.
- `"minChar"`: The shortest word the generator will construct for your language.
- `"minSyll"`: The minimum number of syllables a word has in your language.
- `"dictionary"`: Optional. A database of words in your language so you get more consistent generations.

# Credits
Based upon the advanced Javascript conlang generator created by Martin O'Leary for his fantasy map generator.

https://mewo2.com/notes/naming-language/