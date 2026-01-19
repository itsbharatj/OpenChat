from openai import OpenAI  
import os 
from dotenv import load_dotenv
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import uuid

load_dotenv()

## Init 

chorma_client = chromadb.PersistentClient("RAG_Application/chroma_data")
collection = chorma_client.get_or_create_collection("RAG_Database")


client = OpenAI(api_key=os.getenv("OPEN_AI"))

def get_rag():
    files = get_document()
    for file in files: 
        chunks = chunk_doc(file)
        ind = 0
        for chunk in chunks: 
            store_db(get_embedding(chunk),file+str(ind),chunk,{"chunk_number":chunk,"document":file})
            ind+=1
            print(f"Chunk {ind} of {file} done")
        print(f"File {file} done")
        
def get_embedding(text): 
    
    response = client.embeddings.create(
    input=text, 
    model="text-embedding-3-small"
    )   

    return response.data[0].embedding

def get_document(path="Documents",types=["txt","md"]): 
    ## Get a set of filtered documents: 
    cwd = os.getcwd()

    _files = os.listdir("/Users/bharatjain/Desktop/Chatbot/RAG_Application/Documents")
    files = []
    for i in _files: 
        if i[i.rfind(".")+1:] in types: 
            files.append(os.path.join(cwd,"Documents",i))
    return files
    

def chunk_doc(document,chunk_size=1000,overlap=500):
    ## Open the file, and get all the text 
    with open(document,'r') as file: 
        content = file.read()

    chunks = []
    
    curr_ind = 0
    for _ in range(len(content)//(chunk_size-overlap)): 
        chunks.append(content[curr_ind:curr_ind+chunk_size])
        curr_ind=curr_ind+(chunk_size-overlap)
    
    return chunks


## The embeddings are not being stored in the database

def store_db(collection,document,doc_id=str(uuid.uuid4()),metadata=None): 

    collection.add(
        ids=doc_id,
        documents=document,
        metadatas=metadata
    )

if __name__ == "__main__": 
    get_rag()