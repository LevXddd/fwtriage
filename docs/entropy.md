
# Entropy

> [!NOTE]
> **In one sentence**
> Entropy is a number that answers: **"how unpredictable are these bytes?"**
> Or equivalently: **"how surprised will you be, on average, by the next byte?"**

## The formula

$$H = -\sum_{x} p(x) \cdot \log_2 p(x)$$

- **x** is just a variable — one possible byte. If we have `AAAA`, then x will be `A`.
- **p(x)** is how often x appears, divided by the total length (its probability).
- **log₂** — because we measure in **bits**. One byte has 256 possible values, so the maximum is $$\log_2 256 = 8$$ bits.

## Examples

For example, it is fair to mention that `00 00 00 00` are all the same byte, and accordingly, entropy is **zero** — there is no surprise at all.

| Data | Entropy (bits per byte) | Why |
|---|---|---|
| `00 00 00 00` | 0 | one value, fully predictable |
| `Hello World` | ≈ 2.85 | short text, few different letters |
| long English text | ≈ 4 – 4.5 | letters repeat in patterns |
| compressed / encrypted data | ≈ 7.9 – 8 | looks completely random |

> [!TIP]
> **Why this matters for firmware**
> High entropy (close to 8) usually means the data is **compressed or encrypted**. That is exactly how fwtriage finds suspicious regions inside a binary.

## The example of implementation

```python
from math import log

def calculate_the_entropy(name):
    # first of all, we have formula like -Σ p(x) * log2 p(x)
    # x is just a variable, like if we have AAAA, then x will be A
    total = 0
    counts = {}

    for letter in name:
        if letter in counts:
            counts[letter] += 1  # we are just adding value
        else:
            counts[letter] = 1

    for i in counts:
        p = counts[i] / len(name)
        total += -1 * p * log(p, 2)

    return total
```

> [!WARNING]
> **Edge case**
> If `name` is empty, `len(name)` is 0. Here the loop simply never runs and the result is 0, but keep it in mind.

## Related
- [The concept of the project(detect_filetype)](The concept of the project(detect_filetype).md)]
