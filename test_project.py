
from project import detect_filetype, extract_strings, calculate_the_entropy, entropy_map, carve_embedded
import os


def test_detect_filetype():
    assert detect_filetype(b"\x7FELF\x02\x01") == "ELF executable"
    assert detect_filetype(b"PK\x03\x04data") == "ZIP archive"
    assert detect_filetype(b"Hello world") == "unknown"


def test_extract_strings():
    assert extract_strings(b"\x00\x01hello\x00\xff", 4) == ["hello"]
    assert extract_strings(b"\x00hi\x00", 4) == []                 
    assert extract_strings(b"GET /update HTTP\x00", 4) == ["GET /update HTTP"]


def test_calculate_the_entropy():
    assert calculate_the_entropy(b"AAAA") == 0.0
    assert calculate_the_entropy(b"AABB") == 1.0
    assert calculate_the_entropy(b"") == 0.0


def test_entropy_map():
    assert entropy_map(os.urandom(512)) != {}   
    assert entropy_map(b"A" * 512) == {}         #



def test_carve_embedded():
    data = b"XXXX\x89PNGyyyy%PDFzzzz"   
    found = carve_embedded(data)
    offsets = [name for _, name in found]
    assert "PNG image" in offsets
    assert "PDF document" in offsets