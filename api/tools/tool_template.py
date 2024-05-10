from langchain.tools import StructuredTool
from langchain_core.tools import ToolException

name = "pig_latin"
description = "Useful to translate a sentence to Pig Latin"


def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during {name} tool execution:" + error.args[0]


def get_answer(input: str):
    def sentence_to_pig_latin(sentence):
        sentence = sentence.lower()
        words = sentence.split()
        pig_latin_words = [pig_latin(word) for word in words]
        pig_latin_sentence = ' '.join(pig_latin_words)
        return pig_latin_sentence.capitalize()

    def pig_latin(word):
        vowels = 'aeiou'
        if word[0] in vowels:
            return word + 'way'
        else:
            consonants = ''
            for letter in word:
                if letter not in vowels:
                    consonants += letter
                else:
                    break
            return word[len(consonants):] + consonants + 'ay'

    try:
        return sentence_to_pig_latin(input)
    except Exception as e:
        raise ToolException(f"The following errors occurred during {name} tool execution: {type(e)=}")


def load_tool():
    return StructuredTool.from_function(
        name=name,
        description=description,
        func=get_answer,
        handle_tool_error=_handle_error,
    )
