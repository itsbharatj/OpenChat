'''
    ON THE APP (SHOW): 
        - The current items (sentences) in the vector database 
        - Ask for items to add 

        - Query the database with a respective query ()
        - Show all the items in a table with a sorted property 
'''
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st 
import chromadb
from RAG_Application.embeddings import store_db
from RAG_Application.query_data import get_results
import pandas as pd
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
load_dotenv()
import uuid



chorma_client = chromadb.PersistentClient("RAG_Application/chroma_data")

collection = chorma_client.get_or_create_collection(
    name="embedding_application",
    embedding_function=OpenAIEmbeddingFunction(
        api_key=st.secrets["OPEN_AI"],
        model_name="text-embedding-3-large"
    )
)


url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

## Init the st.session_state:
if "input_sentence" not in st.session_state:
    st.session_state.input_sentence = ""
if "query_sentence" not in st.session_state:
    st.session_state.query_sentence = ""



st.title("Ranking Similar Sentences (Using Embeddings)")
st.header("The app allows you to add sentences in a database and then input a query to see which of the sentences are the closest semantically")
st.markdown("---")

st.header("Add to Database")
sentence = st.text_input("Enter a sentence to be added to the database","")


print("This is the sentence: ",st.session_state)
print(st.session_state.input_sentence != sentence and sentence != "")

if st.session_state.input_sentence != sentence and sentence != "": 
    store_db(collection,doc_id=str(uuid.uuid4()),document=sentence)
    st.session_state.input_sentence = sentence
    st.write("Added to the database")
    st.rerun()

st.write("Current Database") 
current_collection = collection.get()
unsorted_df = pd.DataFrame({"text":current_collection["documents"]})
print(current_collection)
st.table(unsorted_df)


# unsorted_df = st.dataframe(collection.get(include=["documents"]))
# print(unsorted_df)
# st.write(unsorted_df)

st.markdown("---")

st.header("Query the database")
query = st.text_input("Enter your query")

st.markdown("---")
st.subheader(f"Ranking after the query {query}")

# sorted_df = unsorted_df
print(st.session_state.query_sentence != query and query != "")
if st.session_state.query_sentence != query and query != "": 
    results = get_results(collection,query)
    print(results)
    results_df = pd.DataFrame({"Document":results["documents"][0],"Distance":results["distances"][0]})
    st.table(results_df)
    st.session_state.query_sentence = sentence
    st.session_state.last_result = results_df
elif "last_result" in st.session_state:
    print("Last table",st.session_state.last_result)
    st.table(st.session_state.last_result)

if "last_reset_state" not in st.session_state: 
    st.session_state.last_reset_state = False

reset_state = st.button("Reset database")
if reset_state and reset_state != st.session_state.last_reset_state: 
    chorma_client.delete_collection(name="embedding_application")
    st.write("Data Reset Successful")
    st.rerun()