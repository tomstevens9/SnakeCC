from dataclasses import dataclass
from enum import StrEnum, auto
from io import TextIOBase
from typing import Generator


# TODO fill in missing keywords
KEYWORDS = {
    "int",  # TODO Add other types
    "short",
    "long",
    "float",
    "double",
    "signed",
    "unsigned",
    "return",
    "if",
    "else",
    "while",
    "for",
    "break",
    "continue",
    "switch",
    "case",
    "default",
    "void",
    "static",
    "extern",
    "const",
    "typedef",
    "struct",
    "union",
    "enum",
    "sizeof",
}


class TokenType(StrEnum):
    IDENTIFIER = auto()
    PUNCTUATION = auto()
    KEYWORD = auto()
    NUMERIC_CONSTANT = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str


class PeekableReader:
    class EOF(Exception):
        pass

    def __init__(self, input_stream: TextIOBase) -> None:
        self.input_stream = input_stream
        self.peeked = ""

    def peek(self) -> str:
        # Only allow peaking next character
        if not self.peeked:
            self.peeked = self.input_stream.read(1)
        return self.peeked

    def read(self) -> str:
        if self.peeked:
            result = self.peeked
            self.peeked = ""
        else:
            result = self.input_stream.read(1)
        if result:
            return result
        else:
            raise self.EOF

    def __iter__(self) -> "PeekableReader":
        return self

    def __next__(self) -> str:
        try:
            return self.read()
        except self.EOF:
            raise StopIteration


def get_tokens(input_stream: TextIOBase) -> Generator[Token, None, None]:
    reader = PeekableReader(input_stream)
    while True:
        try:
            char = reader.read()
        except PeekableReader.EOF:
            return None
        if char in ("{}()[],;"):
            yield Token(type=TokenType.PUNCTUATION, value=char)
        if char.isalpha():  # identifier or keyword
            token_value = char
            while (new_char := reader.read()).isalnum():  # TODO Hard to read?
                token_value += new_char
            token_type = (
                TokenType.KEYWORD if token_value in KEYWORDS else TokenType.IDENTIFIER
            )
            yield Token(type=token_type, value=token_value)
