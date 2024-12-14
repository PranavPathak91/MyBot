from embeddings.pinecone_client import index

def test_pinecone():
    """
    Tests the Pinecone index by inserting and retrieving a sample vector.
    """
    # Insert a test vector
    test_vector = [0.1] * 768  # Mock embedding vector
    index.upsert([
        {
            "id": "test-id",
            "values": test_vector,
            "metadata": {"content": "This is a test document."}
        }
    ])
    print("Test vector inserted.")

    # Query the test vector
    query_vector = [0.1] * 768  # Mock query vector
    results = index.query(
        vector=query_vector,
        top_k=1,
        include_metadata=True
    )

    print("Query results:", results)

if __name__ == "__main__":
    test_pinecone()
