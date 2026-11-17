
# entropy_map

> [!NOTE]
> **In one sentence**
> Instead of one entropy number for the whole file, we cut it into pieces and measure **each piece** — so we can see *where* the suspicious data is.

## Why one number is not enough

Imagine a firmware: first part is normal code, second part is an encrypted blob. If we calculate [entropy](entropy.md) for the whole file, we get something in the middle, like 5.5 — and it tells us nothing. The encrypted part is hidden inside the average.

So we split the file into **chunks of 256 bytes**, and calculate entropy for each one separately.

```
offset 0      offset 256    offset 512    offset 768
[ code 5.1 ] [ code 5.3 ] [ ??? 7.6 ] [ ??? 7.5 ]
                              ↑ suspicious
```

## The algorithm

1. Walk through the file with a step of 256: `0, 256, 512, ...`
2. Take a slice `name[key : key + 256]` — that is one chunk.
3. Calculate its entropy with `calculate_the_entropy`.
4. If the score is **7 or higher** — save it in a dictionary: offset → score.

## The code

```python
def entropy_map(name):
    suspicious = {}
    for key in range(0, len(name), 256):
        chunk = name[key: key + 256]
        score = calculate_the_entropy(chunk)
        if score >= 7:
            suspicious[key] = score
    return suspicious
```

> [!TIP]
> **Why `range(0, len(name), 256)`?**
> The third argument is the **step**. So `key` jumps 0 → 256 → 512 → ... and every chunk starts exactly where the previous one ended.

> [!WARNING]
> **Limits worth knowing**
> - **The last chunk** can be shorter than 256 bytes, so its entropy is naturally lower.
> - **256 bytes is small.** Even perfectly random data in a 256-byte chunk usually scores around 7.2, not 8 — because 256 bytes is not enough for every value to appear evenly. So the threshold of 7 is close to the edge. A bigger chunk (like 1024) or a configurable threshold would make it more reliable.

## Related
- [entropy](entropy.md) — the formula behind it
- [carve_embedded](carve_embedded.md) — high entropy often means a compressed file is hidden there
