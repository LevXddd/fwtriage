
# extract_strings

> [!NOTE]
> **In one sentence**
> Pull the human-readable text out of a binary. This is the function we will actually use most, so it is worth understanding.

## ASCII in short

I hope you know what "ASCII" means: shortly, it is a table that gives a number to each symbol. It has **128** codes (0–127).

| Range | What it is |
|---|---|
| 0 – 31 | control characters: `0x00` is the null byte (end of a string in C), `9` is `\t` (tab), `10` is `\n` (newline) |
| 32 – 126 | **printable**: space, letters, digits, symbols |
| 127 | DEL, also a control character |

Usually, control characters are just an instruction for the computer, not for us.

## The algorithm

1. Keep a **"current run"** buffer, starting empty.
2. Walk through each byte:
    - If it is printable (32–126): add its character to the current run.
    - If it is not: the run just ended. If the run is **long enough** (4+ characters — short runs are usually coincidence, not real text), save it. Then reset the buffer to empty.
3. After the loop ends, **flush once more** — the file might end in the middle of a run, and you don't want to lose it.

## The code

```python
def extract_strings(data, min_len = 4):
    results= []
    current = ""
    for byte in data:
        if 32 <= byte <= 126: # IN ASCII, FROM 32 TO 126 ARE PRINTABLE CHARACTERS, WHILE OTHERS ARE USUALLY AN INSTRUCTION FOR THE PC
            current += chr(byte) # chr(byte) converts the byte to a character
        else:
            if len(current) >= min_len:
                results.append(current)
            current = ""
    if len(current) >= min_len:
        results.append(current) # Again, why? imagine we have like %PDF\HELLO", it will stop after 0 and will not add the "HELLO" string, so we need to add one more, that is our purpose.
    return results
```

> [!TIP]
> **Try it**
> `extract_strings(b"\x00\x01HELLO\x02hi\x03WORLD")` → `['HELLO', 'WORLD']`
> `hi` is dropped — only 2 characters, shorter than `min_len`.

## Related
- [detect_filetype](detect_filetype.md)
- [entropy](entropy.md)
