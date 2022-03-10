import streamlit as st
import requests

title = st.title('HOA QA Service')

with st.form('form'):
    input = st.text_input('Query', placeholder='Enter question here...')
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner("🧠 Performing neural search on documents..."):
            payload = {
                "query": input
            }
            r = requests.post('http://127.0.0.1:8000/haystack-query/', json=payload)
            full_response = r.json()
            try:
                first_answer = full_response['0']
                answer = first_answer['answer']
                context = first_answer['context']
                output = {'answer': answer, 'context': context}
                st.json(output)
            except KeyError:
                st.error('Hmm...is the Haystack service running?')
