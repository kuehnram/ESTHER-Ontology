from enum import Enum


class Operation(Enum):
    ADDITION = "Addition"
    OMISSION = "Omission"
    REPETITION = "Repetition"
    CONVERSION = "Conversion"
    REPLACEMENT = "Replacement"
    QM = "?"


class LinguisticElement(Enum):
    LETTER = "Letter"
    VOWEL = "Vowel"
    CONSONANT = "Consonant"
    WORD = "Word"
    SENTENCE = "Sentence"
    PHRASE = "Phrase"
    VERSE = "Verse"
    PUNCTUATION = "Punctuation"
    QM = "?"


class LinguisticObject(Enum):
    SAME_FORM = "Same form"
    DIFFERENT_FORM = "Different form"
    SAME_MEANING = "Same meaning"
    DIFFERENT_MEANING = "Different meaning"
    OPPOSED_MEANING = "Opposed meaning"
    QM = "?"


class Position(Enum):
    BEGINNING = "Beginning"
    END = "End"
    MIDDLE = "Middle"
    BEGINNING_AND_END = "Beginning and end"
    WHOLE = "Whole"
    QM = "?"
