import unicodedata
import re
from detoxify import Detoxify
import confusables

import utils.letters as letters

REGEX = fr'.*?(br|[{letters.LETTER_N}{letters.LETTER_J}]+)([\W\s]*[{letters.LETTER_I}{letters.LETTER_E}])+([\W\s]*[{letters.LETTER_G}]{{1,2}}[{letters.LETTER_R}]?)+([\W\s]*[{letters.LETTER_A}{letters.LETTER_Y}{letters.LETTER_O}]|[\W\s]*[{letters.LETTER_E}]+[\W\s]*[{letters.LETTER_R}])+'

detect = re.compile(REGEX, re.IGNORECASE | re.UNICODE)

model = Detoxify('original')

def detect_toxicity(text: str) -> float:
    """
    Returns a dictionary of toxicity scores for the given text.

    The dictionary contains the following scores as floats between 0.0 and 1.0:
    - severe_toxicity
    - obscene
    - threat
    - insult
    - identity_attack
    - toxicity

    The scores are calculated by the Detoxify model.
    """
    scores = model.predict(text)
    return scores

def multiplier(text: str) -> float:
    """
    Returns a multiplier for the given text based on how toxic it is.

    The multiplier is a float between 1.0 and 2.0, where a higher value indicates a more toxic message.
    The value is determined by the 'severe_toxicity' score of the given text, which is calculated by the Detoxify model.
    """
    toxicity = detect_toxicity(confusables.normalize(text))
    toxicity = toxicity['severe_toxicity'] + toxicity['threat']
    print(f"Detected toxicity: {toxicity}")
    return 1.0 + toxicity

def detect_word(text: str) -> int:
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
    stripped = text.replace("\n", "").replace("\r", "")
    
    #decoded = unidecode(text)
    # normalised used to cover chinese/other characters
    # that look similar to letters
    
    normalised = unicodedata.normalize("NFD", stripped)
    normalised = re.sub(r'[\u0300-\u036f]', '', "".join([char for char in normalised if unicodedata.category(char) != "Mn"]))
    
    return len(set(detect.findall(normalised)))