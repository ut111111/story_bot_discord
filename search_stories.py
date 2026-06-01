import faiss
import json
from sentence_transformers import SentenceTransformer

# Load model
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load index
print("Loading index...")
index = faiss.read_index("stories.index")

# Load metadata
print("Loading metadata...")
metadata = []

with open("metadata.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        metadata.append(json.loads(line))

print(f"Stories: {len(metadata)}")
print("Ready!\n")


def search(query, top_k=50):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        results.append({
            "score": float(score),
            "story": metadata[idx]
        })

    return results


def show_page(results, start, page_size=5):
    end = min(start + page_size, len(results))

    for i in range(start, end):
        result = results[i]

        print("\n" + "=" * 80)
        print(f"Result #{i+1}")
        print(f"Score: {result['score']:.4f}")

        story = result["story"]

        if isinstance(story, dict):
            for key, value in story.items():
                text = str(value)

                if len(text) > 300:
                    text = text[:300] + "..."

                print(f"{key}: {text}")
        else:
            print(story)

    return end


while True:
    query = input("\nSearch> ").strip()

    if query.lower() in ["exit", "quit"]:
        break

    results = search(query, top_k=50)

    if not results:
        print("No results found.")
        continue

    position = 0

    while True:
        position = show_page(results, position, page_size=5)

        if position >= len(results):
            print("\nNo more results.")
            break

        cmd = input(
            "\nPress Enter or type 'more' for next 5 results "
            "(new search/exit also works): "
        ).strip()

        if cmd.lower() in ["", "more"]:
            continue

        if cmd.lower() in ["exit", "quit"]:
            exit()

        # treat anything else as a new search
        query = cmd
        results = search(query, top_k=50)
        position = 0
