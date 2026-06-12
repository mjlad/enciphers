# enciphers

Fast Rust-powered encryption for Python.

## Benchmark

> Tested on 1000 iterations. enciphers uses Rust bindings.
> Fernet and itsdangerous are pure Python. rfernet uses Rust bindings (Fernet algorithm).

| | enciphers | Fernet | rfernet | itsdangerous |
|---|---|---|---|---|
| encrypt (ms) | **0.45ms** | 10.42ms | 2.68ms | 11.96ms |
| decrypt (ms) | **0.41ms** | 9.12ms | 1.69ms | 9.15ms |
| memory enc (B) | **176** | 1330 | 225 | 383,391 |
| memory dec (B) | **99** | 830 | 99 | 59,594 |
| encrypts data | ✅ | ✅ | ✅ | ❌ signs only |
| algorithm | Substitution + HMAC-SHA256 | AES-128-CBC | AES-128-CBC | HMAC |

> **Note:** enciphers uses a custom substitution cipher optimized for speed.
> It is not a standard cryptographic algorithm and is not recommended
> for highly sensitive data. Suitable for session tokens and non-critical data.

## Features

- **Fast** — up to 95% faster than Fernet in Python
- **Lightweight** — minimal memory footprint
- **Simple API** — two methods: `encrypt` and `decrypt`
- **Unique tokens** — same input produces different output every time
- **Signed** — HMAC-SHA256 on every token

## Installation

```bash
pip install enciphers
```

## Usage

```python
import orjson
from enciphers import Encipher

cipher = Encipher(step=7, key=42)
# or from environment variable
cipher = Encipher(step=7, key_env="CIPHER_KEY")

token = cipher.encrypt(orjson.dumps({"id": "1", "name": "mejlad"}))
data  = orjson.loads(cipher.decrypt(token))
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `step` | `int` | Encryption step (required) |
| `key` | `int` | Secret key (takes priority over `key_env`) |
| `key_env` | `str` | Environment variable name for the key |

> At least one of `key` or `key_env` must be provided.

## License

Apache-2.0 — Copyright 2026 Mejlad Alsubaie
