# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 21:01:13 2025

@author: MUSTAFA
"""

import requests
from bs4 import BeautifulSoup
import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def get_text_from_url(url_input):
    try:
        response = requests.get(url_input)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join([p.text for p in paragraphs])
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch text from URL: {e}")
        return None

def summarize_text(text, language, summary_length):
    if language == 'Turkish':
        language = 'Turkish'
    elif language == 'English':
        language = 'english'
    else:
        language = 'german'
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=summary_length)
    return " ".join([str(sentence) for sentence in summary])

def main():
    st.title('Text Summarizer')
    text_input = st.text_area('Enter text or URL:', height=200)
    url_input = st.text_input('Enter a URL (Optional)')
    lang = st.selectbox('Select Language', ['Turkish', 'English', 'German']) 
    summary_length = st.slider('Summary Length (Number of Sentences):', 1, 10, 3)
    
    if st.button('Summarize'):
        if url_input:
            text_input = get_text_from_url(url_input)
            if text_input:
                st.write("Text fetched from URL")
                st.write('Summarization in progress...')
                summary = summarize_text(text_input, lang, summary_length)
                st.write('Summary (Sumy):')
                st.write(summary)
            else:
                return
        elif text_input:
            st.write('Summarization in progress...')
            summary = summarize_text(text_input, lang, summary_length)
            st.write('Summary (Sumy):')
            st.write(summary)
        else:
            st.warning('Please enter text')
        
        st.download_button(label='Download Summary',
                           data=summary.encode('utf-8'),
                           file_name='summary.txt',
                           mime='text/plain')

if __name__ == '__main__':
    main()
