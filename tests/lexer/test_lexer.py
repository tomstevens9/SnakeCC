import pytest
import io
import itertools


from snakecc.lexer.lexer import PeekableReader


EXAMPLE_TEXT = "example text"


@pytest.fixture
def example_reader() -> PeekableReader:
    return PeekableReader(io.StringIO(EXAMPLE_TEXT))


def test_peekable_reader_reads_correctly(example_reader: PeekableReader) -> None:
    for c in EXAMPLE_TEXT:
        assert example_reader.read() == c
    with pytest.raises(PeekableReader.EOF):
        assert example_reader.read()


def test_peekable_reader_peak_does_not_move_cursor(
    example_reader: PeekableReader,
) -> None:
    for c in EXAMPLE_TEXT:
        assert example_reader.peek() == c
        assert example_reader.read() == c


def test_peekable_reader_peak_only_looks_ahead_one_char(
    example_reader: PeekableReader,
) -> None:
    assert example_reader.peek() == "e"
    assert example_reader.peek() == "e"
    assert example_reader.read() == "e"


def test_peekable_reader_iterates_correctly(example_reader: PeekableReader) -> None:
    assert "".join(example_reader) == EXAMPLE_TEXT


def test_peekable_reader_peeking_works_during_iteration(
    example_reader: PeekableReader,
) -> None:
    for c in example_reader:
        if c == " ":
            assert example_reader.peek() == "t"
