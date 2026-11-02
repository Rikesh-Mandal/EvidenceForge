import pytest
from app.ingest import chunk_pages, extract_pages
def test_txt_is_utf8_and_has_no_page_number():
    assert extract_pages("notes.txt", b"hello world") == [(None, "hello world")]
def test_chunk_overlap_is_deterministic():
    pages = [(2, "one two three four five six seven")]
    pieces = chunk_pages(pages, size=4, overlap=2)
    assert pieces[0]["content"] == "one two three four"
    assert pieces[1]["content"] == "three four five six"
    assert all(item["page_number"] == 2 for item in pieces)
def test_unknown_type_is_rejected():
    with pytest.raises(ValueError):
        extract_pages("file.exe", b"payload")
def test_overlap_constraints():
    with pytest.raises(ValueError):
        chunk_pages([(1, "a b")], size=5, overlap=5)