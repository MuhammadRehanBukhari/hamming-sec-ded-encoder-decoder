#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r

        # Predefined non-systematic generator matrix G'
        self.gns = [
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        ]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(self.gns)
        self.h = self.__derive_h(self.g)

        

    def __convert_to_g(self, gns: List[List[int]]) -> List[List[int]]:
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """
        G = [row[:] for row in gns]

        def xor_rows(a, b):
          return [x ^ y for x, y in zip(a, b)]

        # Step 1
        G[2] = xor_rows(G[2], G[0])
        G[4] = xor_rows(G[4], G[0])
        G[5] = xor_rows(G[5], G[0])
        # Step 2
        G[0] = xor_rows(G[0], G[1])
        G[2] = xor_rows(G[2], G[1])
        G[5] = xor_rows(G[5], G[1])
        # Step 3
        G[0] = xor_rows(G[0], G[2])
        G[4] = xor_rows(G[4], G[2])
        G[5] = xor_rows(G[5], G[2])
        # Step 4
        G[0] = xor_rows(G[0], G[3])
        G[2] = xor_rows(G[2], G[3])
        # Step 5
        G[1] = xor_rows(G[1], G[4])
        G[2] = xor_rows(G[2], G[4])
        # Step 6
        G[0] = xor_rows(G[0], G[5])
        G[1] = xor_rows(G[1], G[5])
        G[4] = xor_rows(G[4], G[5])

        return G


    def __derive_h(self, g: List[List[int]]) -> List[List[int]]:
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """
        k = len(g)        # number of data bits
        n = len(g[0])     # total bits
        r = n - k         # number of parity bits

        # Extract parity part P (last r columns)
        P = [row[k:] for row in g]

        # Transpose P to get P^T
        P_T = [[P[row][col] for row in range(k)] for col in range(r)]

        # Append identity I_r to P^T to form H
        H = []
        for i in range(r):
            identity_row = [1 if j == i else 0 for j in range(r)]
            H.append(P_T[i] + identity_row)

        return H


    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """Encodes the given word and returns the codeword as a tuple."""
        if len(source_word) != self.data_bits:
            raise ValueError(f"Source word must have length {self.data_bits}")

        # Initialize codeword
        codeword = [0] * self.total_bits

        # Multiply source_word with systematic generator matrix G (mod 2)
        for i in range(self.data_bits):
            if source_word[i] == 1:
                for j in range(self.total_bits):
                    codeword[j] ^= self.g[i][j]

        # Compute additional parity bit p5 (even parity)
        parity_bit = sum(codeword) % 2
        codeword.append(parity_bit)  # append SEC-DED bit

        return tuple(codeword)

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """Decodes the codeword, correcting single-bit errors and detecting double-bit errors."""
        if len(encoded_word) != self.total_bits + 1:
            raise ValueError(f"Encoded word must have length {self.total_bits + 1}")

        codeword = list(encoded_word[:-1])
        p5_received = encoded_word[-1]

        # Compute syndrome
        syndrome = []
        for row in self.h:
            s = sum(c * h for c, h in zip(codeword, row)) % 2
            syndrome.append(s)

        # Compute overall parity including p5
        total_parity = (sum(codeword) + p5_received) % 2

        if total_parity == 0 and all(s == 0 for s in syndrome):
            return tuple(codeword[:self.data_bits]), HCResult.VALID
        elif total_parity == 1 and any(s != 0 for s in syndrome):
            # Single-bit error: correct
            error_position = 0
            for i, bit in enumerate(syndrome):
                error_position += bit << i
            error_position -= 1

            if 0 <= error_position < self.total_bits:
                codeword[error_position] ^= 1
                return tuple(codeword[:self.data_bits]), HCResult.CORRECTED
            else:
                return None, HCResult.UNCORRECTABLE
        elif total_parity == 1 and all(s == 0 for s in syndrome):
            # Error only in p5
            return tuple(codeword[:self.data_bits]), HCResult.CORRECTED
        else:
            return None, HCResult.UNCORRECTABLE
