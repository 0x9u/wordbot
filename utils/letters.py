from confusables import confusable_characters

LETTER_N = "".join(set(['Ņ', 'ⓝ', '⒩', '几', '𝐍', 'ɳ', '𝓷', '𝖓', 'ክ', 'ꋊ', 'n', 'π', '🇳', '🄽', 'u', 'ภ', 'ɲ'] + confusable_characters('n')))
LETTER_I = "".join(set(['i', '𝓲', '1', '!', 'l', 'î', r'\|', 'ⓘ', '⒤', '𝖎', 'ጎ', '丨', 'ꂑ', '𝒾', '🇮', '🄸', 'ı'] + confusable_characters('i')))
LETTER_G = "".join(set(['9', '7', 'g', 'ġ', 'ğ', '𝕘', 'ⓖ', '⒢', 'ɠ', 'Ꮆ', '𝓰', '𝖌', '𝐠', 'ኗ', 'ꁅ', 'q','🇬', '🄶', 'ƃ', 'ﻮ','Ᏽ'] + confusable_characters('g')))
LETTER_R = "".join(set(['ⓡ', '𝐫', 'r', '𝓻', 'ꌅ', '⒭', '૨', '尺', 'Ր', '𝖗', 'ዪ', 'я', '🇷', 'ɹ', 'г'] + confusable_characters('r')))
LETTER_A = "".join(set(['a', '@', 'ã', 'æ', 'Ⓐ', '⒜', '4', '𝖆', '𝓪', '🇦', '🄰', 'Ꮬ'] + confusable_characters('a')))
LETTER_E = "".join(set(['e', 'ቿ', 'ⓔ', '⒠', '𝖊', '𝓮', '乇', 'ꈼ', '𝐞', 'ε', '🇪', 'ǝ', 'є', '𝝚'] + confusable_characters('e')))
LETTER_O = "".join(set(['o', 'σ'] + confusable_characters('o')))
LETTER_Y = "".join(set(['y', 'Ⓨ', '⒴'] + confusable_characters('y')))
LETTER_J = "".join(set(['j', '⒥', 'ⓙ', '𝖏', '𝓳', 'ꃅ', '𝐣', 'ጂ', 'ɉ'] + confusable_characters('j')))