# tests/test_basic.py
import os
from extractor import extract_text_pdf
from preprocess import tokenize_sentences
from summarizer import textrank

def test_extract_and_summarize():
    pdf_path = "exemplo.pdf"
    assert os.path.exists(pdf_path), "Coloque um exemplo.pdf na raiz do projeto para o teste."
    text = extract_text_pdf(pdf_path)
    assert len(text) > 100
    sents = tokenize_sentences(text)
    summary = textrank(sents, top_n=5)
    assert len(summary) > 20
