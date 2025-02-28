from langchain.prompts import PromptTemplate
from template import prompt_template
from langchain_community.vectorstores import Chroma
from langchain_aws import BedrockEmbeddings
import streamlit as st
import boto3

__import__('pysqlite3')

import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Accede a las credenciales desde los secretos de Streamlit
aws_access_key_id = st.secrets["aws"]["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = st.secrets["aws"]["AWS_SECRET_ACCESS_KEY"]
aws_session_token = st.secrets["aws"]["AWS_SESSION_TOKEN"]

CHROMA_PATH = 'chroma_db'
region_name = 'us-east-1'
model_id = "amazon.titan-embed-text-v1"
txt_model_name = "amazon.nova-lite-v1:0"

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
def get_embedding_function():
    embeddings = BedrockEmbeddings(
        region_name=region_name,
        model_id=model_id,
        client=bedrock_client
    
    )
    return embeddings


def get_chroma():
    return Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

def generar_prompt(chunks, question):
    """Genera un prompt formateado para un asistente virtual especializado en Ingeniería de Analítica de Datos."""
    
    prompt = PromptTemplate(
        input_variables=["chunks", "question"],
        template=prompt_template,
    )

    # Formatear el prompt con los valores proporcionados
    return prompt.format(chunks=chunks, question=question)


from langchain_aws import ChatBedrock

def obtener_respuesta(mensaje, region='us-east-1', model_kwargs=None):
    """Genera una respuesta utilizando el modelo ChatBedrock de AWS."""

    if model_kwargs is None:
        model_kwargs = {
            "temperature": 0.2,
            "topP": 0.2,
            "maxTokenCount": 200,
        }

    # Inicializar el modelo ChatBedrock
    chat = ChatBedrock(
        region_name=region,
        model_id=txt_model_name,
        model_kwargs=model_kwargs,
    )

    # Realizar la predicción y retornar la respuesta
    return chat.predict(mensaje)



def inference(pregunta, k=3):
    """Realiza una inferencia utilizando el modelo de lenguaje ChatBedrock de AWS y la base de datos Chroma."""

    # Obtener la base de datos Chroma
    db = get_chroma()

    # Realizar la búsqueda de similitud para recuperar los documentos más relevantes
    resultados = db.similarity_search(pregunta, k=k)

    # Extraer el contenido de las páginas de los documentos recuperados
    contexto = "\n\n---\n\n".join([doc.page_content for doc in resultados])

    # Generar el prompt con el contexto y la pregunta
    prompt = generar_prompt(chunks=contexto, question=pregunta)

    # Obtener la respuesta del modelo de lenguaje
    respuesta = obtener_respuesta(prompt)

    return respuesta
 
