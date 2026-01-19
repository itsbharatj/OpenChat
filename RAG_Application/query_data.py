from RAG_Application.embeddings import get_embedding
import chromadb

client = chromadb.PersistentClient("RAG_Application/chroma_data")
collection = client.get_collection("RAG_Database")

def get_results(collection, user_query, n_results=10): 
    # query_embedding = get_embedding(user_query)

    results = collection.query(
    query_texts=user_query,
    n_results=n_results,
    include=["documents","distances"]
)
    return results


if __name__ == "__main__": 

    ## Testing the embeddings

    print("Results::",get_results("What is the next line after this line: This book has brought us together again, always a joy in the book?",4))


