import uuid
import codestats_filetypes


def test_filetype_to_language():
    assert codestats_filetypes.get_language_name("") == "Plain text"
    assert codestats_filetypes.get_language_name("zsh") == "Shell Script (Zsh)"


def test_unknown_filetype_to_language():
    for i in range(10):
        # generate a string that certainly isn't a known filetype
        filetype = uuid.uuid4()
        assert codestats_filetypes.get_language_name(filetype) == filetype
