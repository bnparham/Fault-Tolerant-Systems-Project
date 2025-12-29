# CRC-16 Visual Error Detection Simulator

## Overview

This project is a **visual and educational simulation of CRC-16 error detection**
designed to demonstrate how cyclic redundancy checks work at the bit level.

The application generates random binary data, computes a CRC-16 checksum using
polynomial division, simulates transmission errors, and visually shows how CRC
detects corrupted data.

---

## How the Project Works

### 1. Data Generation

- A random **64-bit binary data word** is generated for each run.
- The data is treated as a polynomial in binary form.

### 2. CRC-16 Computation

- A standard **CRC-16-CCITT generator polynomial** is used: x^16 + x^12 + x^5 + 1
- Sixteen zero bits are appended to the data.
- Modulo-2 polynomial division is performed.
- The **16-bit remainder** becomes the CRC checksum.

### 3. Frame Transmission

- The transmitted frame is formed as: [64-bit data] + [16-bit CRC]

### 4. Channel Simulation

The simulator supports three transmission scenarios:

- **No Error:** Perfect transmission with no bit changes
- **Independent Errors:** Random bit flips at arbitrary positions
- **Burst Errors:** Contiguous sequences of flipped bits

### 5. Visual Error Highlighting

- The received frame is compared bit-by-bit with the transmitted frame.
- Correct bits are displayed in **green**.
- Corrupted bits are displayed in **red** for easy identification.

### 6. Receiver Verification

- The receiver recomputes the CRC over the received frame.
- If the remainder is non-zero, an error is detected.
- The result is clearly reported in the terminal output.

---

## Purpose

This project is intended for:

- Learning CRC fundamentals
- Understanding polynomial division in error detection
- Visualizing the effect of random and burst errors
- Demonstrating why CRC is effective in real communication systems

---

## Execution

Run the simulator using Python:

```bash
python crc16_visual_simulator.py
```