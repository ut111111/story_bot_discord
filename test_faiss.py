import json
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

INPUT_FILE = "all_stories_rich.jsonl"
LIMIT = 10000

print("Loading model...")
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

texts = []
metadata = []

print("Reading dataset...")

with open(INPUT_FILE, encoding="utf-8") as f:

    for i, line in enumerate(f):

        if i >= LIMIT:
            break

        obj = json.loads(line)

        title = obj["title"]
        story = obj["story"]

        text = f"{title}\n{story[:1200]}"

        texts.append(text)

        metadata.append({
            "title": title,
            "subreddit": obj["subreddit"],
            "score": obj["score"],
            "tag": obj.get("tag")
        })

print(f"Loaded {len(texts)} stories")

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)

embeddings = embeddings.astype("float32")

faiss.normalize_L2(embeddings)

dim = embeddings.shape[1]

index = faiss.IndexFlatIP(dim)

index.add(embeddings)

print("Index size:", index.ntotal)

while True:

    query = input("\nSearch> ").strip()

    if query.lower() in ["exit", "quit"]:
        break

    q = model.encode([query])

    q = np.array(q).astype("float32")

    faiss.normalize_L2(q)

    scores, ids = index.search(q, 5)

    print("\nTop Results:\n")

    for rank, idx in enumerate(ids[0], start=1):

        item = metadata[idx]

        print("=" * 80)
        print(f"#{rank}")
        print("Score:", round(float(scores[0][rank-1]), 3))
        print("Subreddit:", item["subreddit"])
        print("Tag:", item["tag"])
        print("Reddit Score:", item["score"])
        print("Title:", item["title"])
