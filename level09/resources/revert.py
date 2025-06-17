#!/usr/bin/env python3

def revert(buf: bytes) -> str:
    return "".join([chr((b - i) % 256) for i, b in enumerate(buf)])

if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as f:
        data = f.read()

    reverted = revert(data[:-1]) # remove \n
    print(reverted)
