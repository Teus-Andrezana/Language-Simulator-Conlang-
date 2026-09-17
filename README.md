# Language-Simulator-Conlang

A Python project for generating artificial languages (conlangs), exploring phonetic patterns, and developing language families from a base language. The central idea is to simulate how a language can arise, evolve, and branch into dialects by creating sounds, syllable structure, stress rules, vocabulary, and phonological change over time.

## Author note

This project was created by a curious enthusiast rather than a professional linguist. The goal is to explore, experiment, and learn in a practical way how languages can be modeled computationally. Suggestions, feedback, and ideas are very welcome.

## Central theme of the project

The project combines three main ideas:

- Generation of an initial proto-language
- Definition of phonetic and structural rules
- Evolution of that language into dialects and language families

In other words, it works like a computational linguistics lab: from a set of sounds and meanings, the system creates a language with internal properties and can then derive different variants as if they were branches in an evolutionary tree.

## What the project does

- Creates initial vowels and consonants for a base language
- Defines word order, syllable structure, and stress patterns
- Generates basic words and concepts
- Applies phonetic rules and sound changes
- Creates dialects from a mother language
- Maintains a base of meanings and grammatical categories
- Allows investigation into how a language can vary over generations

## Project structure

- [proto.py](proto.py): contains the `ProtoLingua` class, responsible for generating the initial language, including sounds, grammar, stress, and basic vocabulary.
- [familia.py](familia.py): contains the `FamiliaLinguistica` class, which creates dialects and language families from the original language, simulating evolution and branching.
- [tools.py](tools.py): contains helper functions for phonetic analysis, sound changes, vowel/consonant classification, lenition, harmony, and word adjustment.
- [conlang.ipynb](conlang.ipynb): interactive notebook for experiments, testing, and visual exploration of the generator.
- [biblioteca/fonetica.json](biblioteca/fonetica.json): phonetic rules and sound classification database.
- [biblioteca/significados.json](biblioteca/significados.json): dictionary of meanings and concepts used as the basis for lexical generation.
- [readMe](readMe): project documentation.

## How it works

The logic of the project follows the idea of a language evolving in layers:

1. The `ProtoLingua` class builds an initial base containing:
   - sound inventory
   - syllable structure
   - grammatical order
   - stress pattern
   - initial words

2. The `FamiliaLinguistica` class receives this base and generates variants as if they were dialects of the same ancestral branch.

3. Functions in `tools.py` apply phonetic changes and standardization to make the evolution more realistic.

4. JSON files act as data libraries: phonetic rules and term meanings.

## Example usage

```python
from proto import ProtoLingua
from familia import FamiliaLinguistica

lingua_base = ProtoLingua(150)
print(lingua_base.proto_lingua["sons"])

familia = FamiliaLinguistica(4, lingua_base.proto_lingua, "lingua_mae", 0)
print(familia.dialetos_criados.keys())
```

This type of execution generates a base language and a family with derived dialects.

## Requirements

- Python 3.9+
- Standard Python libraries
- JSON files present in the `biblioteca/` folder

## Dependencies

The project uses native Python structures such as:

- `random`
- `json`
- `copy`
- optional notebook libraries such as `pandas` in some contexts

## Future improvements

- Better documentation of the word-generation flow
- Visual examples of language families
- Exploration of more phonological and morphological rules
- Improved organization of documentation by module
- Language contact effects and their influence on speech
- Broader experimentation with lexical and grammatical evolution

## Conclusion

This project is a simulation of linguistic creation and evolution, with a focus on phonetics, lexicon, and the branching of languages. It works as a useful foundation for experimentation and study of how artificial languages can emerge and differentiate over time.
