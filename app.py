
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
#from dotenv import load_dotenv

OPENAI_API_KEY= st.secrets["OPENAI_API_KEY"]

hide_st_style = """ <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #viewerBadge_link__qRIco {visibility: hidden;}
            viewerBadge_link__qRIco {visibility: hidden;}
            </style>"""



def main():
    # load_dotenv()
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    st.sidebar.info("Developed by - Sudhakar G.")
    st.sidebar.info("Only for Learning Purpose.")
    #st.set_page_config(page_title="Document Assistant")
    st.header("Gen-AI Doc Assist 💬")
    
    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    
    # extract the text
    if pdf is not None:
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
        
      # split into chunks
      text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
      )
      chunks = text_splitter.split_text(text)
      
      # create embeddings
      embeddings = OpenAIEmbeddings()
      knowledge_base = FAISS.from_texts(chunks, embeddings)
      
      # show user input
      user_question = st.text_input("Extract Doc info - Ask a question")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)
        
        llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          st.write(cb)
           
        st.write("Response : ")
        st.success(response)
        
    

if __name__ == '__main__':
     main()
