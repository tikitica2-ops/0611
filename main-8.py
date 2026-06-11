import os
import tempfile

import streamlit as st
from langchain_community.document_loaders import (  PyPDFLoader )
from langchain_text_splitters import (    RecursiveCharacterTextSplitter )
from langchain_chroma import (    Chroma  )
from langchain_openai import   OpenAIEmbeddings,    ChatOpenAI 
from langchain_classic.chains import (   create_retrieval_chain )
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import (   ChatPromptTemplate )
from langchain_core.callbacks import   BaseCallbackHandler

st.title("📄 PDF File Reader")
st.write("----------------")


openai_key = st.text_input(  "OPENAI_API_KEY",    type="password" )

uploaded_file = st.file_uploader(   "PDF 파일을 올려주세요",   type=["pdf"] )
st.write("----------------")

def pdf_to_document(uploaded_file):
    """    Streamlit 업로드 PDF를
    LangChain Document 형태로 변환
    """
    # 임시 폴더 생성
    temp_dir = tempfile.TemporaryDirectory()

    # 임시 PDF 파일
    temp_filepath = os.path.join(     temp_dir.name,    uploaded_file.name    )

    with open(   temp_filepath,    "wb"  ) as f:
        f.write(    uploaded_file.getvalue()    )

    loader = PyPDFLoader(   temp_filepath   )

    pages = loader.load()
    return pages

class StreamHandler(  BaseCallbackHandler ):
    """
    GPT가 토큰을 생성할 때마다
    Streamlit 화면에 출력하는 Handler

    예:
    GPT:   안녕하세요
    생성 과정:
    안
    안녕
    안녕하세요

    처럼 실시간 출력
    """
    def __init__(  self,    container  ):
        self.container = container
        self.text = ""
