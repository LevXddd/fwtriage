# detect_filetype

> [!NOTE]
> **In one sentence**
> The very start of a file often has a fixed signature called a **magic number** — and by checking it, we know the file type.

## Known signatures

| Format | Bytes | As text |
|---|---|---|
| ELF executable | `7F 45 4C 46` | `\x7F` followed by `ELF` |
| ZIP | `50 4B 03 04` | `PK` then `\x03\x04` |
| gzip | `1F 8B` | — |
| PNG | `89 50 4E 47` | `\x89PNG` |
| PDF | `25 50 44 46` | `%PDF` |
| JPEG | `FF D8 FF` | — |

## The idea

In order to detect the file, we should check whether its bytes start with one of these.

1. Every valid file **of one format** starts with the same bytes. For example, every valid PDF on Earth starts with `25 50 44 46` (`%PDF`). This is not a coincidence — it is written into each format's official documentation.
2. For storing we use a **dictionary**: signature → name. It is the best way to keep this data.

## How `startswith` works, with a real example

Let's say you open a real PNG file and read its bytes. The first eight bytes are always:

```
89 50 4E 47 0D 0A 1A 0A
```

In Python that data looks like `b"\x89PNG\r\n\x1a\n...thousands more bytes..."`.

`startswith` just asks: **"do the first bytes of data exactly equal the signature?"** Because every PNG begins with `\x89PNG`, this is `True` for every PNG and `False` for everything else. So we match it to `"PNG image"`.

> [!NOTE]
> **Not everything at the start is the type**
> ```
> 25 50 44 46 2D 31 2E 34   =  "%PDF-1.4"
> ```
> Only the first **four** bytes (`%PDF`) tell the type. The rest (`-1.4`) is the version and other information, which is not static — it changes from file to file.

## The code

```python
SIGNATURES = {
    b"\x7FELF": "ELF executable",
    b"PK\x03\x04": "ZIP archive",
    b"\x1f\x8b": "gzip compressed",
    b"\x89PNG": "PNG image",
    b"%PDF": "PDF document",
    b"\xff\xd8\xff": "JPEG image",
}

def detect_filetype(data):
    for signature, name in SIGNATURES.items():
        if data.startswith(signature):
            return name
    else:
        return "unknown"
```

> [!TIP]
> **Why `for ... else`?**
> The `else` belongs to the `for`, not the `if`. It runs only if the loop finished **without** returning — meaning no signature matched.

The function is built, and it works without any errors — checked via Pytest.

## Related
- [extract_strings](extract_strings.md)
- [carve_embedded](carve_embedded.md) — the same matching, but at every position, not only the start


