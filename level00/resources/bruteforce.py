import string

def rotate(s: str, r: int):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[r:] + alphabet[:r]
    table = str.maketrans(alphabet, shifted_alphabet)

    return s.translate(table)

if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2, "invalid usage"

    s = sys.argv[1]

    for i in range(1, 26):
        print(f"{i:>2} -> {rotate(s, i)}")
