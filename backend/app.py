from flask import Flask, request, jsonify, session
from flask_cors import CORS
import requests
import googletrans
import os
import soundfile as sf
import numpy as np
from io import BytesIO
import re

# RAG Libs
import pinecone
from torch import cuda
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

# RAG Setup
# pinecone.init(
#     api_key=os.environ.get('8827e1fc-4c19-46f2-97b9-c622b5488a3f') or '8827e1fc-4c19-46f2-97b9-c622b5488a3f',
#     environment=os.environ.get('gcp-starter') or 'gcp-starter'
# )

pc = Pinecone(
        api_key=os.environ.get('8827e1fc-4c19-46f2-97b9-c622b5488a3f') or '8827e1fc-4c19-46f2-97b9-c622b5488a3f',
        environment=os.environ.get('gcp-starter') or 'gcp-starter'       
    )

embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

embed_model = HuggingFaceEmbeddings(
    model_name=embed_model_id,
    model_kwargs={'device': device},
    encode_kwargs={'device': device, 'batch_size': 50}
)

index_name = 'herdhelp-rag'
index = pc.Index(index_name)

text_field = 'text'  # field in metadata that contains text content

from langchain_community.vectorstores import Pinecone
vectorstore = Pinecone(
    index, embed_model.embed_query, text_field
)
# RAG setup end

API_URL = "https://api-inference.huggingface.co/models/ahmed807762/gemma-2b-vetdataset-finetuned"
headers = {"Authorization": "Bearer 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"}

API_URL1 = "https://api-inference.huggingface.co/models/ihanif/whisper-medium-urdu"
headers1 = {"Authorization": "Bearer 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"}

# Dedicated
# API_URL1 = "https://p8345i3xkcgeg28h.us-east-1.aws.endpoints.huggingface.cloud"
# headers1 = {
#     "Accept": "application/json",
#     "Authorization": "Bearer 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",
#     "Content-Type": "audio/flac"
# }


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for the session
CORS(app)

# Dictionary to store chat sessions
chat_sessions = {}


# Define the route for the API endpoint where the frontend will send the user's query
@app.route('/api/query', methods=['POST'])
def api_query():
    # Get the query from the request data sent by the frontend
    data = request.json
    prompt = data.get('prompt')

    # Process the query
    sys_prompt = "As a Pakistani veterinarian, you provide expertise on livestock health and farming, assisting users with relevant queries."
    user_prompt = prompt
    prompt = prompt
    # Perform translation if needed
    # Translator = googletrans.Translator()
    # translation = Translator.translate(prompt, src='ur', dest='en')
    # prompttr = translation.text
    
    # # User's prompt translation
    # Translator = googletrans.Translator()
    # translation = Translator.translate(user_prompt, src='ur', dest='en')
    # prompttr_user = translation.text
    
    # RAG context retrieval
    # quer = prompttr_user
    quer = prompt
    res = vectorstore.similarity_search(
        quer,  # the search query
        k=1  # returns top 3 most relevant chunks of text
    )

    concatenated_content = ""
    for document in res:
        concatenated_content += document.page_content + ' '

    # Query the model
    output = query({
        # "inputs": sys_prompt + " Here is some relevant context, " + concatenated_content + " question " + prompttr_user + " Now generate answer : ",
        "inputs": sys_prompt + " Here is some relevant context, " + concatenated_content + " question " + prompt + " Now generate answer : ",
        "parameters": {"max_new_tokens": 250, "repetition_penalty": 7.0},
        "options": {"wait_for_model": True}
    })
    output = output[0]['generated_text']
    
    print("Output = ", output)

    # Use regex to find the text after the asterisk (*)
    match = re.search(r':(.*)', output)
    if match:
        output = match.group(1)

    # Translate the response back to Urdu
    # translation = Translator.translate(output, src='en', dest='ur')
    # response = translation.text

    # Update the chat session
    session_id = data.get('session_id')
    # chat_sessions[session_id] = chat_sessions.get(session_id, []) + [(prompt, response)]
    chat_sessions[session_id] = chat_sessions.get(session_id, []) + [(prompt, output)]

    # Prepare the response data
    response_data = {
        # 'response': response
        'response': output
    }

    # Return the response data as JSON
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
