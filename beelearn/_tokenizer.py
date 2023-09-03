import re


def tokenize_word(input_string):
    # Split the input string using the %word% delimiter
    tokens = re.split(r"%word%", input_string)

    # Remove empty strings and leading/trailing whitespace
    cleaned_tokens = [token.strip() for token in tokens if token.strip()]

    return cleaned_tokens


input_string = """
%word% is an example of string
"""

tokens = tokenize_word(input_string)
print(tokens)
