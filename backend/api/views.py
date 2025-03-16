# Import necessary libraries
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import TextDocument, UserQuery
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
from rest_framework.exceptions import ValidationError, APIException

# Initialize Chroma vector database
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

# Load GPT-Neo for text generation
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")


def add_text_content(content):
    """API to store text content and process embeddings"""
    if not content:
        return Response({'error': 'Content is required'}, status=400)

    # Store text document
    text_doc = TextDocument.objects.create(content=content)

    # Split and process text into embeddings
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_text(content)

    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_texts(docs, embedding_function, persist_directory="./chroma_db")

    text_doc.processed = True
    text_doc.save()
    return Response({'message': 'Text added and processed successfully', 'doc_id': text_doc.id})

# Function to get context from the database
def get_relevant_context_from_db(query: str):
    """
    Retrieves the relevant context for a given query from the Chroma vector database.
    """
    try:
        context = ""
        search_results = vector_db.similarity_search(query, k=6)
        for result in search_results:
            context += result.page_content + "\n"
        return context.strip() or "No relevant context available from the database."
    except Exception as e:
        raise APIException(f"Error generating answer: {str(e)}")

# Function to generate a prompt for the LLM
def generate_rag_prompt(query: str, context: str):
    """
    Generates a prompt for the LLM.
    """
    escaped = context.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = (f"""
    You are an AI assistant, tasked with providing informative and comprehensive answers to user queries.
    
    **Query:** {query}
    **Context:** {escaped}
    
    **Your Task:**
    1. Understand the Query
    2. Leverage the Context
    3. Generate a Response
    4. Maintain Objectivity
    5. Provide Proper Formatting
    """)
    return prompt

# Function to generate an answer using Hugging Face's GPT-Neo
def generate_answer(prompt: str):
    """
    Generates an answer using Hugging Face's GPT-Neo model.
    """
    try:
        generated_text = generator(
            prompt,
            max_new_tokens=50,  # Allow space for new tokens
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        return generated_text[0]["generated_text"].strip()
    except Exception as e:
        raise APIException(f"Error generating answer: {str(e)}")

@api_view(['POST'])
def handle_query(request):
    """
    Handles user queries by fetching relevant context and generating an answer using a free LLM.
    """
    user_id = request.data.get('user_id')
    query = request.data.get('query')

    if not query or query.strip() == "":
        raise ValidationError("Query cannot be empty.")
    if not user_id:
        raise ValidationError("User ID is required.")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError("User not found.")

    context = get_relevant_context_from_db(query)
    prompt = generate_rag_prompt(query, context)
    answer = generate_answer(prompt)

    UserQuery.objects.create(
        user=user,
        query_text=query,
        response_text=answer
    )

    return Response({
        "query": query,
        "context": context,
        "answer": answer
    })