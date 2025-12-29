import random

# Terminal UI helpers
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def banner(title):
    print(f"\n{BOLD}{CYAN}{'='*70}")
    print(f"{title.center(70)}")
    print(f"{'='*70}{RESET}")

# ------------------------------------------------
# CRC-16 core logic
# ------------------------------------------------

def polynomial_to_binary(poly_terms, degree):
    """
    Convert polynomial terms to binary generator string.

    Example:
    poly_terms = [16, 12, 5, 0]
    degree = 16
    Output: '10001000000100001'
    """
    bits = ['0'] * (degree + 1)

    for term in poly_terms:
        bits[degree - term] = '1'

    return ''.join(bits)

CRC_GENERATORS = {
    "CRC-16-CCITT": {
        "degree": 16,
        "terms": [16, 12, 5, 0]
    },
    "CRC-16-ALT-1": {
        "degree": 16,
        "terms": [16, 15, 11, 9, 8, 7, 5, 4, 2, 1, 0]
    },
    "CRC-16-ALT-2": {
        "degree": 16,
        "terms": [16, 10, 8, 7, 3, 0]
    },
    # --- CUSTOM CRC ---
    "CRC-16-CUSTOM-1": {
        "degree": 16,
        "terms": [16, 15, 11, 9, 8, 7, 5, 4, 2, 1, 0]
    },
    "CRC-16-CUSTOM-2": {
        "degree": 16,
        "terms": [16, 10, 8, 7, 3, 0]
    },
    "CRC-16-CUSTOM-3": {
        "degree": 16,
        "terms": [16, 14, 13, 11, 9, 6, 5, 3, 0]
    }
}

def get_crc_generator(name):
    gen = CRC_GENERATORS[name]
    return polynomial_to_binary(gen["terms"], gen["degree"])

def list_generators():
    print(f"{BOLD}Available CRC Generators:{RESET}")
    for name in CRC_GENERATORS:
        binary = get_crc_generator(name)
        print(f"- {name}")
        print(f"  Polynomial bits: {YELLOW}{binary}{RESET}\n")

list_generators()
CRC_POLY = get_crc_generator("CRC-16-ALT-1")

def crc_division(data, poly):
    data = list(data)
    poly_len = len(poly)

    for i in range(len(data) - poly_len + 1):
        if data[i] == '1':
            for j in range(poly_len):
                data[i + j] = '0' if data[i + j] == poly[j] else '1'

    return ''.join(data[-(poly_len - 1):])

# ------------------------------------------------
# Data generation
# ------------------------------------------------
def random_bits(n):
    return ''.join(random.choice('01') for _ in range(n))

# ------------------------------------------------
# Error injection
# ------------------------------------------------

def independent_error(frame, num_errors=None, max_errors=5):
    """
    Independent bit errors.
    
    - num_errors = integer -> user-controlled number of errors
    - num_errors = None    -> computer randomly chooses (1 to max_errors)
    """
    frame = list(frame)
    length = len(frame)

    if num_errors is None:
        num_errors = random.randint(1, max_errors)

    num_errors = min(num_errors, length)
    positions = random.sample(range(length), num_errors)

    for p in positions:
        frame[p] = '0' if frame[p] == '1' else '1'

    return ''.join(frame), positions


def burst_error(frame, burst_length=None, max_burst=10):
    """
    Burst (contiguous) errors.
    
    - burst_length = integer -> user-controlled burst size
    - burst_length = None    -> computer randomly chooses size
    """
    frame = list(frame)
    length = len(frame)

    if burst_length is None:
        burst_length = random.randint(2, max_burst)

    burst_length = min(burst_length, length)
    start = random.randint(0, length - burst_length)

    for i in range(start, start + burst_length):
        frame[i] = '0' if frame[i] == '1' else '1'

    return ''.join(frame), (start, start + burst_length - 1)


# ------------------------------------------------
# Highlight corrupted bits
# ------------------------------------------------
def highlight_errors(original, received):
    out = []
    for o, r in zip(original, received):
        if o == r:
            out.append(GREEN + r + RESET)
        else:
            out.append(RED + r + RESET)
    return ''.join(out)

# ------------------------------------------------
# Full educational demo (UPDATED)
# ------------------------------------------------
def crc_demo(error_type="none", burst_size=None):
    banner(f"CRC-16 DEMO — MODE: {error_type.upper()}")

    # 1. Generate data
    data = random_bits(64)
    print(f"{BOLD}Original 64-bit Data:{RESET}")
    print(GREEN + data + RESET)

    # 2. Append zeros
    appended = data + "0" * 16
    print(f"\n{BOLD}Append 16 zeros:{RESET}")
    print(appended)

    # 3. Generator
    print(f"\n{BOLD}Generator Polynomial:{RESET}")
    print(YELLOW + CRC_POLY + RESET)

    remainder = crc_division(appended, CRC_POLY)
    print(f"\n{BOLD}CRC Remainder:{RESET}")
    print(CYAN + remainder + RESET)

    # 4. Transmitted frame
    tx = data + remainder
    print(f"\n{BOLD}Transmitted Frame:{RESET}")
    print(GREEN + tx + RESET)

    # 5. Channel behavior
    if error_type == "none":
        rx = tx
        print(f"\n{GREEN}✔ No error introduced in channel{RESET}")

    elif error_type == "independent":
        rx, pos = independent_error(tx)
        print(f"\n{RED}Independent bit errors at positions:{RESET} {pos}")

    elif error_type == "burst":
        rx, rng = burst_error(tx, burst_length=burst_size)

        if burst_size is None:
            print(f"\n{RED}Burst error (random size) from bit {rng[0]} to {rng[1]}{RESET}")
        else:
            print(f"\n{RED}Burst error (size = {burst_size}) from bit {rng[0]} to {rng[1]}{RESET}")

    else:
        raise ValueError("Invalid error_type. Use: none, independent, or burst.")

    # 6. Show received frame with highlights
    print(f"\n{BOLD}Received Frame (errors highlighted):{RESET}")
    print(highlight_errors(tx, rx))

    # 7. Receiver CRC check
    check = crc_division(rx, CRC_POLY)
    print(f"\n{BOLD}Receiver CRC Remainder:{RESET}")
    print(CYAN + check + RESET)

    # 8. Decision
    if int(check, 2) == 0:
        print(f"\n{GREEN}{BOLD}✔ NO ERROR DETECTED{RESET}")
    else:
        print(f"\n{RED}{BOLD}✖ ERROR DETECTED BY CRC{RESET}")


crc_demo("none")
crc_demo("independent")
crc_demo("burst")

crc_demo("burst", burst_size=3)
crc_demo("burst", burst_size=8)
