import sys


def main() -> int:
    assert len(sys.argv) == 2
    input_file_path = sys.argv[1]
    print(input_file_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
