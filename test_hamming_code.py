#!/usr/bin/env python3
import pytest
from hamming_code import HammingCode, HCResult

class TestHammingCode:
    def test_instance(self):
        """ Essential: Test class instantiation """
        hc = HammingCode()
        assert isinstance(hc, HammingCode)

    def test_decode_valid(self):
        """ Test decode() with VALID input """
        hc = HammingCode()
        codewords = [
            (0,0,1,0,1,1,1,1,1,1,0),
            (0,0,0,0,0,0,0,0,0,0,1),
            (1,0,1,1,0,1,1,1,1,0,1)
        ]
        expected_decoded = [
            (0,1,1,0,1,1),
            (0,0,0,0,0,0),
            (1,0,1,1,0,1)
        ]
        for cw, expected in zip(codewords, expected_decoded):
            decoded, result = hc.decode(cw)
            assert decoded == expected
            assert result == HCResult.VALID

    def test_decode_corrected(self):
        """ Test decode() with CORRECTED input """
        hc = HammingCode()
        # Single-bit error in data bits
        codeword = list(hc.encode((0,1,1,0,1,1)))
        codeword[2] ^= 1
        decoded, result = hc.decode(tuple(codeword))
        assert decoded == (0,1,1,0,1,1)
        assert result == HCResult.CORRECTED

        # Single-bit error in SEC-DED parity bit
        codeword = list(hc.encode((1,0,1,1,0,1)))
        codeword[-1] ^= 1
        decoded, result = hc.decode(tuple(codeword))
        assert decoded == (1,0,1,1,0,1)
        assert result == HCResult.CORRECTED

    def test_decode_uncorrectable(self):
        """ Test decode() with UNCORRECTABLE input """
        hc = HammingCode()
        # Double-bit error
        codeword = list(hc.encode((1,1,1,1,1,0)))
        codeword[1] ^= 1
        codeword[4] ^= 1
        decoded, result = hc.decode(tuple(codeword))
        assert decoded is None
        assert result == HCResult.UNCORRECTABLE

    def test_encode(self):
        """ Test encode() """
        hc = HammingCode()
        test_words = [
            (0,1,1,0,1,1),
            (0,0,0,0,0,0),
            (1,0,1,1,0,1),
            (1,1,1,1,1,0)
        ]
        for word in test_words:
            codeword = hc.encode(word)
            assert len(codeword) == hc.total_bits + 1  # SEC-DED parity
            assert isinstance(codeword, tuple)
