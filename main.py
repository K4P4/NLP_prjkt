import streamlit as st
import PyPDF2
from PyPDF2 import PdfFileReader
import spacy

nlp = spacy.load('en_core_web_lg')

junk_pos=['X', 'AUX', 'PUNCT', 'ADV', 'INTJ', 'ADP', 'DET']

def nonStop(token):
    return token.is_stop == False
    
def nonDuplicate(token, cleaned):
    return token.text not in cleaned
    
def nonJunk(token):
    flag=True
    if token.pos_ in junk_pos:
        flag=False
    return flag

def Summarize(text):
    doc = nlp(text)
    cleaned = []
    for token in doc:
        if nonStop(token):
            if nonDuplicate(token, cleaned):
                if nonJunk(token):
                    cleaned.append(token.text)
    return cleaned

st.title("Keyword extractor")
default_value = "This is the text you want to extract keywords from"
user_input = st.text_area("Enter your own text", default_value)
text=""

if user_input is not None:
    text = user_input
    text.lower()
    textArray = Summarize(text)
    summarized = " ".join(textArray)
st.write(summarized)