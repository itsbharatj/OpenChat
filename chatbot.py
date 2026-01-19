from openai import OpenAI 
import os 
from dotenv import load_dotenv
from RAG_Application.query_data import get_results

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ"),
    base_url="https://api.groq.com/openai/v1"
)

def _get_context(prompt,n): 
    '''
        Get's the context from the embedded documents and uses them to answer the query and the question 
        Appends the context with the original prompt and returns that as output
    '''
    context = ""
    print(prompt)
    documents = get_results(prompt,n)
    # for ind,document in enumerate (documents[0]): 
    #     if document is not "None": 
    #         context = f"Context {ind} is {document}\n"
    
    final_prompt = f"""
        Original User Query: {prompt}, 
        Relevant context you can use to answer the question: 
        {documents}
    """
    print(f"Final Prompt: \n {final_prompt}")
    return final_prompt


def response(prompt,include_rag=False,n=4): 
    
    if include_rag: 
        prompt = _get_context(prompt,n)
    
    response = client.responses.create(
        input = prompt, 
        model = "openai/gpt-oss-20b"
    )

    return (response.output_text)


if __name__ == "__main__": 
    print(response(input("prompt?"),include_rag=True))