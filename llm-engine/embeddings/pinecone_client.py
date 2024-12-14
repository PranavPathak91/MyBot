from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(
    api_key="pcsk_YZany_6dVP28ckbLDTJCsxfCouwaLcd4esofdWdK3jAe9fydzitR49X31BnLynHU6AT1z"
)

# Define the index name
INDEX_NAME = "document-embeddings"

# Ensure the index exists
if INDEX_NAME not in pc.list_indexes():
    pc.create_index(
        name=INDEX_NAME,
        dimension=768,  # Set to match your embedding size
        metric="cosine",  # You can also use dotproduct or euclidean
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Access the index
index = pc.Index(INDEX_NAME)
