from sentence_transformers import SentenceTransformer


def main():
    """ Based on: https://sbert.net/ """

    # Load a pretrained Sentence Transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # The sentences to encode
    sentences = [
        "My corgi loves chasing RC Cars. So I strapped a GoPro to one...",
        "Corgi-sized meteor as heavy as 4 baby elephants",
        "Border collies run freely and at full speed",
    ]
    print("Sentences:\n", sentences)

    # Calculate embeddings by calling model.encode()
    embeddings = model.encode(sentences)
    #print("Embeddings:\n", embeddings)
    print("Embedding shape:", embeddings.shape)

    # Calculate the embedding similarities
    similarities = model.similarity(embeddings, embeddings)
    print("Similarities:\n", similarities.numpy())


if __name__ == "__main__":
    main()
