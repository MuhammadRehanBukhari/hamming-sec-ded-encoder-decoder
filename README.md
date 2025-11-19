
```markdown
A complete Python implementation of the **(10,6) Hamming SEC-DED code** (Single-Error Correction, Double-Error Detection).  
This project includes:

- Generator matrix (G) derivation  
- Parity-check matrix (H) derivation  
- Encoding of 6-bit data words  
- Decoding with:
  - `VALID` — no error  
  - `CORRECTED` — single-bit error fixed  
  - `UNCORRECTABLE` — double-bit error detected  
- Full pytest-based unit test suite  
- Demo script for viewing outputs

---


````

Install dependencies:

```bash
pip3 install -r requirements.txt
```

---

## ▶️ How to Run the Demo

```bash
python3 demo_run.py
```

This prints:

* Encoded codewords
* Valid decodes
* Single-bit error correction
* Double-bit error detection

---

## 🧪 Running Tests

```bash
pytest
```


---

## 📘 Example Output

```
Encoding examples:
Input: (0, 1, 1, 0, 1, 1)
Encoded: (0,0,1,0,1,1,1,1,1,1,0)

Decoding:
Decoded: (0,1,1,0,1,1), Result: VALID

Single-bit error corrected:
Decoded: (0,1,1,0,1,1), Result: CORRECTED

Double-bit error detected:
Decoded: None, Result: UNCORRECTABLE
```

---

## 🛠 Technologies Used

* Python 3
* PyTest
* Linear algebra over GF(2)
* Hamming SEC-DED coding theory

---


---

## 👤 Author

Muhammad Rehan Bukhari

```


