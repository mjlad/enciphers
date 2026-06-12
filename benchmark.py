"""
encipher benchmark vs competitors
Requirements: pip install encipher cryptography itsdangerous rfernet orjson
"""

import os
import time
import tracemalloc
import orjson

os.environ.setdefault("CIPHER_KEY", "42")

from enciphers import Encipher
from cryptography.fernet import Fernet
from itsdangerous import URLSafeTimedSerializer
from rfernet import Fernet as rFernet


# ────────────────────────────────────────
# Settings
# ────────────────────────────────────────

ITERATIONS : int  = 1000
STEP       : int  = 7
DATA       : dict = {
    "id"      : "1",
    "name"    : "mejlad",
    "username": "mejlad",
    "picture" : "pic.jpg",
}

# ────────────────────────────────────────
# Initialize
# ────────────────────────────────────────

cipher     = Encipher(step=STEP, key=42)
fernet_key = Fernet.generate_key()
f          = Fernet(fernet_key)
rf         = rFernet(rFernet.generate_new_key())
s          = URLSafeTimedSerializer("secret_key_42")
text       = orjson.dumps(DATA)
text_str   = text.decode("utf-8")


# ────────────────────────────────────────
# Benchmark function
# ────────────────────────────────────────

def bench(fn, *args) -> tuple[float, int]:
    t = time.perf_counter()
    for _ in range(ITERATIONS):
        r = fn(*args)
    ms = (time.perf_counter() - t) * 1000

    tracemalloc.start()
    r = fn(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return ms, peak, r


# ────────────────────────────────────────
# Encrypt
# ────────────────────────────────────────

enc_ms,  enc_mem,  enc_token  = bench(cipher.encrypt, text)
fer_ms,  fer_mem,  fer_token  = bench(f.encrypt,      text)
rfe_ms,  rfe_mem,  rfe_token  = bench(rf.encrypt,     text)
its_ms,  its_mem,  its_token  = bench(s.dumps,        {"data": text_str})

# ────────────────────────────────────────
# Decrypt
# ────────────────────────────────────────

dec_ms,  dec_mem,  _  = bench(cipher.decrypt, enc_token)
fdec_ms, fdec_mem, _  = bench(f.decrypt,      fer_token)
rdec_ms, rdec_mem, _  = bench(rf.decrypt,     rfe_token)
idec_ms, idec_mem, _  = bench(s.loads,        its_token)


# ────────────────────────────────────────
# Results
# ────────────────────────────────────────

def diff(base: float, new: float) -> float:
    return ((base - new) / base) * 100


W = 64
print("=" * W)
print(f"{'Benchmark — encipher vs competitors':^{W}}")
print(f"{'Iterations: ' + str(ITERATIONS):^{W}}")
print("=" * W)
print(f"\n{'':18} {'encipher':>10} {'Fernet':>10} {'rfernet':>10} {'itsdangerous':>14}")
print("-" * W)
print(f"{'encrypt (ms)':18} {enc_ms:>8.2f}ms {fer_ms:>8.2f}ms {rfe_ms:>8.2f}ms {its_ms:>12.2f}ms")
print(f"{'decrypt (ms)':18} {dec_ms:>8.2f}ms {fdec_ms:>8.2f}ms {rdec_ms:>8.2f}ms {idec_ms:>12.2f}ms")
print(f"{'memory enc (B)':18} {enc_mem:>10} {fer_mem:>10} {rfe_mem:>10} {its_mem:>14}")
print(f"{'memory dec (B)':18} {dec_mem:>10} {fdec_mem:>10} {rdec_mem:>10} {idec_mem:>14}")
print(f"{'encrypts data':18} {'yes':>10} {'yes':>10} {'yes':>10} {'no (signs)':>14}")
print("-" * W)
print(f"\nencipher faster than Fernet        (encrypt) : {diff(fer_ms,  enc_ms):>+.1f}%")
print(f"encipher faster than rfernet       (encrypt) : {diff(rfe_ms,  enc_ms):>+.1f}%")
print(f"encipher faster than itsdangerous  (encrypt) : {diff(its_ms,  enc_ms):>+.1f}%")
print(f"encipher faster than Fernet        (decrypt) : {diff(fdec_ms, dec_ms):>+.1f}%")
print(f"encipher faster than rfernet       (decrypt) : {diff(rdec_ms, dec_ms):>+.1f}%")
print(f"encipher faster than itsdangerous  (decrypt) : {diff(idec_ms, dec_ms):>+.1f}%")
print("=" * W)
