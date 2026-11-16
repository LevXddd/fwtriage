# fwtriage

#### Description:

fwtriage is a command-line tool for taking a first look at an unknown binary file - a step security analysts call triage. I chose this project because I was always interested in Cybersecurity, which from my perspective of view, is important for every individual. 
Firmware and embedded security is a major field today: analysts are regularly handed files with no documentation - a router's firmware, a device memory dump, a suspicious sample - and they must work out what the file contains without running it, because running an unknown binary is dangerous. fwtriage cannot decompile code, but it answers the fast questions: what type of file this is, what readable text is hidden inside, how random (and therefore possibly encrypted or compressed) its contents are, and whether other files are buried within it. 

You run it from the terminal with a single argument:

    python project.py <some_file>

After this, it prints a short report - the detected file type, the readable strings that it did find, the overall entropy of the file, any high-entropy regions, and any embedded files it located


The project is built from five functions plus a main() that ties them together. 


**detect_filetype** reads the first bytes of the file and compares them against a table of known *magic numbers* - fixed byte sequences that every file of a format begins with (for example, every PDF starts with `%PDF`, and every PNG with `\x89PNG`). If one matches it returns the format name. Otherwise it returns `"unknown"`.


**extract_strings** pulls human-readable text out of the binary. It walks through the bytes and collects runs of printable ASCII characters - the range 32 to 126, which covers the symbols people actually read and type. Only runs of at least four characters are kept, which filters out random coincidences and leaves real content such as file paths, URLs and error messages.

**calculate_the_entropy** measures how random the file's bytes are, using Shannon entropy:

$$H = -\sum_{x} p(x)\,\log_2 p(x)$$

where `p(x)` is the probability of each byte value. The result runs from 0 (completely predictable) to 8 (completely random). Ordinary code scores around 6, while encrypted or compressed data scores close to 8.

**entropy_map** applies that measurement across the file in fixed windows of 256 bytes and flags every window scoring 7 or even higher. One number for a whole file hides a small encrypted region, but a window-by-window scan reveals exactly where it is.

**carve_embedded** does the same kind of matching as detect_filetype, but instead of checking only the start, it scans the whole file for magic numbers at every position. Each hit marks the start of a file hidden inside the main one.

#### Design decisions

Carving only uses signatures of four bytes or more. This comes from probability: a short two-byte signature such as gzip's matches by pure chance roughly once every 65,536 positions, which means hundreds of false hits in a large file, while a four-byte signature almost never matches by accident. In the future I plan to rewrite the entropy loop in C to make it much faster on large files, keeping the Python version as a fallback.

#### Limitations

The tool cannot determine the exact end of an embedded file, so carving reports where files begin but not their precise size. It is a triage tool, not a full extractor or decompiler.
