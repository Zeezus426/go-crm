from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_neo4j import Neo4jVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, Tool, OpenAIServerModel
from langchain.tools import tool

# Load environment variables
load_dotenv()

# Initialize your Neo4j vector database
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
url = os.getenv("NEO4J_URL")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Load and split documents
loader = TextLoader("/Users/zacharyaldin/Downloads/Pagani Zonda R Specifications and Performance Details.html")  # Replace with your actual file path
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# Create embeddings and database
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

db = Neo4jVector.from_documents(
    docs, 
    embeddings, 
    url=url, 
    username=username, 
    password=password, 
    # search_type="similarity"
)



model = OpenAIServerModel(
    model_id="local-model",
    api_base="http://localhost:1234/v1",
    api_key="Faaahhh",
)


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    try:
        retrieved_docs = db.similarity_search(query, k=2)
        if not retrieved_docs:
            return "No documents found", []
        
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs
    except Exception as e:
        return f"Error retrieving documents: {str(e)}", []

retrieve = Tool.from_langchain(retrieve_context)


# Create agent with the retrieval tool
agent = ToolCallingAgent(
    tools=[retrieve], 
    model=model,
    max_steps=5
)

# Example usage
queries = [
    "What is the weight of the pagani zonda r?",
    "Tell me about the engine specifications of the pagani zonda r.",
    "What is the top speed of the pagani zonda r?"

]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    response = agent.run(query)
    print(f"Agent response: {response}")
    print(f"{'='*60}\n")