
# main

> [!NOTE]
> **In one sentence**
> `main` reads the file and runs every function one after another — it is the glue of the whole tool.

## Usage

```bash
python project.py combined.bin
```

`sys.argv` is the list of words from the command line: `sys.argv[0]` is `project.py`, `sys.argv[1]` is the file name. So we need **exactly 2** — otherwise we exit.

## The flow

1. Check arguments — if not exactly 2, exit with `"Incorrect"`.
2. Open the file in **`"rb"`** mode — read **b**inary. We need raw bytes, not text.
3. If the file does not exist — exit with `"File is not found"`.
4. Otherwise run everything:

| Step | Function | Prints |
|---|---|---|
| 1 | [detect_filetype](detect_filetype.md) | file type |
| 2 | [extract_strings](extract_strings.md) | readable strings |
| 3 | [entropy](entropy.md) | entropy of the whole file |
| 4 | [entropy_map](entropy_map.md) | suspicious chunks, or "There are no suspicious chunks" |
| 5 | [carve_embedded](carve_embedded.md) | hidden files, or "None" |

> [!TIP]
> **Why `try / except / else`?**
> `try` holds only the risky part (opening the file). `else` runs only if nothing failed — so the analysis never starts on a file that could not be opened.

## The code

```python
def main():
    try:
        if len(sys.argv) != 2:
            sys.exit("Incorrect")
        with open(sys.argv[1], "rb") as file:
            data = file.read()
    except FileNotFoundError:
        sys.exit("File is not found")
    else:
        print(f"File type: {detect_filetype(data)}")
        print("Extracted strings:")
        for letter in extract_strings(data):
            print(" ", letter)
        print(f"Entropy of the file: {calculate_the_entropy(data):.2f} ")
        check = entropy_map(data)
        if not check:
            print('There are no suspicious chunks')
        else:
            print(f"Suspicious chunks with high entropy: ")
            for key, value in check.items():
                print(f" Offset: {key}, Entropy: {value:.3f}")
        listing = carve_embedded(data)
        if not listing:
            print("None")
        for key, value in listing:
            print(f"Position: {key}, Name: {value}")
```

> [!NOTE]
> **Small things to polish later**
> `"Incorrect"` could say how to use it: `"Usage: python project.py FILE"`. And `"None"` could be clearer, like `"No embedded files found"`.
