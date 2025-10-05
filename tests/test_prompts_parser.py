import os
from src.prompts_parser import parse_prompts_file


def write_tmp(tmp_path, text: str):
    p = tmp_path / "prompts.txt"
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_single_prompt(tmp_path):
    path = write_tmp(tmp_path, "hello world\n")
    prompts = parse_prompts_file(path)
    assert prompts == ["hello world"]


def test_multiline_prompt(tmp_path):
    text = """line1\nline2\n"""
    path = write_tmp(tmp_path, text)
    prompts = parse_prompts_file(path)
    assert prompts == ["line1\nline2"]


def test_two_prompts_with_delimiter(tmp_path):
    text = """first line\n---\nsecond line\n"""
    path = write_tmp(tmp_path, text)
    prompts = parse_prompts_file(path)
    assert prompts == ["first line", "second line"]


def test_ignores_empty_chunks(tmp_path):
    text = """---\n---\nhello\n---\n\n---\n"""
    path = write_tmp(tmp_path, text)
    prompts = parse_prompts_file(path)
    assert prompts == ["hello"]


def test_custom_delimiter(tmp_path):
    text = """a\n***\nb\n"""
    path = write_tmp(tmp_path, text)
    prompts = parse_prompts_file(path, delimiter="***")
    assert prompts == ["a", "b"]
