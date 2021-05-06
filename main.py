import streamlit as st
import matplotlib.pyplot as plt
import numpy as numpy
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

def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text

st.title("Text summarizer")
uploaded_file = st.file_uploader("Select a text file",["txt","pdf"])
st.write("or")
default_value = "This is the text you want to summarize"
user_input = st.text_area("Enter your own text", default_value)

text=""


if uploaded_file is not None:
    if uploaded_file.name.__contains__(".pdf"):
        text = read_pdf(uploaded_file)
        text.lower()
    elif uploaded_file.name.__contains__(".txt"):
        raw_text = uploaded_file.read()
        text = str(raw_text, 'UTF-8')
        text.lower()
    st.subheader('Here is your summarized text:')
    textArray = Summarize(text)
    summarized = " ".join(textArray)
    st.write(summarized)
elif user_input is not None:
    text = user_input
    text.lower()
    textArray = Summarize(text)
    summarized = " ".join(textArray)
    st.write(summarized)