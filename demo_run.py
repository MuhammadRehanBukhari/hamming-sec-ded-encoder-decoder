#!/usr/bin/env python3
from hamming_code import HammingCode, HCResult

def print_section(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

def main():
    hc = HammingCode()

    # ---------------------------------------------------------
    # Encoding examples
    # ---------------------------------------------------------
    print_section("ENCODING EXAMPLES")

    test_words = [
        (0,1,1,0,1,1),
        (0,0,0,0,0,0),
        (1,0,1,1,0,1),
        (1,1,1,1,1,0)
    ]

    for word in test_words:
        encoded = hc.encode(word)
        print(f"Input: {word}  ->  Encoded: {encoded}")

    # ---------------------------------------------------------
    # Decoding valid codewords
    # ---------------------------------------------------------
    print_section("DECODING VALID CODES")

    valid_codewords = [
        (0,0,1,0,1,1,1,1,1,1,0),
        (0,0,0,0,0,0,0,0,0,0,1),
        (1,0,1,1,0,1,1,1,1,0,1),
        (1,1,1,1,1,0,1,0,1,1,1)
    ]

    for cw in valid_codewords:
        decoded, result = hc.decode(cw)
        print(f"Codeword: {cw}  ->  Decoded: {decoded}, Result: {result.value}")

    # ---------------------------------------------------------
    # Correctable error example
    # ---------------------------------------------------------
    print_section("SINGLE-BIT ERROR CORRECTION")

    word = (0,1,1,0,1,1)
    encoded = list(hc.encode(word))

    # introduce a single error
    encoded[3] ^= 1
    corrupted = tuple(encoded)

    decoded, result = hc.decode(corrupted)
    print(f"Corrupted: {corrupted}  ->  Decoded: {decoded}, Result: {result.value}")

    # ---------------------------------------------------------
    # Uncorrectable error example
    # ---------------------------------------------------------
    print_section("UNCORRECTABLE ERROR (DOUBLE-BIT ERROR)")

    word = (1,1,1,1,1,0)
    encoded = list(hc.encode(word))

    encoded[1] ^= 1
    encoded[4] ^= 1
    corrupted2 = tuple(encoded)

    decoded2, result2 = hc.decode(corrupted2)
    print(f"Corrupted: {corrupted2}  ->  Decoded: {decoded2}, Result: {result2.value}")

if __name__ == "__main__":
    main()
