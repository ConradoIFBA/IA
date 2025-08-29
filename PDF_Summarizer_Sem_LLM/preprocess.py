# preprocess.py
import spacy

# Ajuste o modelo de acordo com seu idioma (pt_core_news_sm / en_core_web_sm)
nlp = spacy.load("pt_core_news_sm")

def tokenize_sentences(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    return sentences
