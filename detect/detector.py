from unidecode import unidecode
import unicodedata
import re

import detect.letters as letters

def detect_word(text: str) -> bool:
    """
    Detects if a given text contains a racial slur.

    This function will detect if a given text contains a racial slur, regardless of
    whether it is written with ASCII characters or characters with diacritics.

    Parameters
    ----------
    text : str
        The text to check

    Returns
    -------
    bool
        True if the text contains a racial slur, False otherwise
    """
    
    # decoded used to remove diacritics
    text = text.replace("\n", "").replace("\r", "")
    
    decoded = unidecode(text)
    # normalised used to cover chinese/other characters
    # that look similar to letters
    normalised = unicodedata.normalize("NFD", text)
    normalised = re.sub(r'[\u0300-\u036f]', '', "".join([char for char in normalised if unicodedata.category(char) != "Mn"]))

    regex = fr'.*?(?:(br|[{letters.LETTER_N}{letters.LETTER_J}]+)[\W\s]*?)+(?:[/\\\(\){letters.LETTER_I}]+[\W\s]*?)+(?:[{letters.LETTER_G}{letters.LETTER_R}]+[\W\s]*?)+(?:[{letters.LETTER_A}{letters.LETTER_Y}{letters.LETTER_O}]+[\W\s]*?|(?:[{letters.LETTER_E}]+[\W\s]*?[{letters.LETTER_R}]+[\W\s]*?))'
  
    
    return re.match(regex, decoded, re.IGNORECASE | re.UNICODE) or re.match(regex, normalised, re.IGNORECASE | re.UNICODE)