
# carve_embedded

> [!NOTE]
> **In one sentence**
> Search for magic numbers **everywhere** in the file, not only at the start — to find files hidden inside other files.

## The idea

In [detect_filetype](detect_filetype.md) we checked only the very beginning of the file. But firmware is often like a box with other files inside: a PNG logo, a gzip archive, an ELF program — all glued together into one `.bin`.

So the same signatures from `SIGNATURES` can appear in the **middle** of the file. If we find `\x89PNG` at position 4096 — there is probably a PNG image starting there.

```
combined.bin
[ ELF header ... ][ \x89PNG ... image ... ][ \x1f\x8b ... gzip ... ]
 0                 4096                     9000
```

## The algorithm

1. For each signature in `SIGNATURES`:
2. Search for it with `find`, starting from position 0.
3. `find` returns the position, or **-1** if there is nothing.
4. While it is not -1: save `(position, name)`, then search again starting from `position + 1`.

> [!TIP]
> **Why `position + 1`?**
> If we searched again from the same `position`, `find` would return the same result forever — an infinite loop. Moving one byte forward lets it find the **next** match.

## The code

```python
def carve_embedded(name):
    results = []
    for key, value in SIGNATURES.items():
        starting_point = 0
        position = name.find(key, starting_point)
        while position != -1:
            results.append((position, value))
            # why do we use two parentheses? because we need a tuple.
            starting_point = position + 1
            position = name.find(key, starting_point)
    return results
```

> [!TIP]
> **Example output**
> ```
> Position: 0, Name: ELF executable
> Position: 4096, Name: PNG image
> ```
> Position 0 is the file itself — the same answer as `detect_filetype`.

> [!WARNING]
> **Limits worth knowing**
> - **False positives:** short signatures like gzip (`1F 8B`, only 2 bytes) can appear by pure coincidence inside random data.
> - **Order:** results are grouped by signature, not by position. Sorting them (`sorted(results)`) would read more naturally.
> - It only **finds** files — it does not extract them yet. A real carver also saves each file to disk.

## Related
- [detect_filetype](detect_filetype.md) — the same signatures
- [entropy_map](entropy_map.md)
