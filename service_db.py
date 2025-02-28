import os
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from IPython.display import Markdown
import textwrap
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings.bedrock import BedrockEmbeddings