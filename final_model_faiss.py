import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

INPUT_FILE = "all_stories_rich.jsonl"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading model...")
model = SentenceTransformer(MODEL_NAME)

texts = []

print("Loading stories...")

with open(INPUT_FILE, encoding="utf-8") as fin, open(
    "metadata.jsonl", "w", encoding="utf-8"
) as meta_out:

    count = 0

    for line in tqdm(fin):
        try:
            obj = json.loads(line)

            title = obj.get("title", "").strip()
            story = obj.get("story", "").strip()

            if not story:
                continue

            # Main embedding text
            text = f"{title}\n{story[:1200]}"
            texts.append(text)

            metadata = {
                "title": title,
                "subreddit": obj.get("subreddit"),
                "score": obj.get("score"),
                "created_utc": obj.get("created_utc"),
                "tag": obj.get("tag"),
                "char_count": obj.get("char_count"),
                "word_count": obj.get("word_count"),
                "story_preview": story[:1000],
            }

            meta_out.write(json.dumps(metadata, ensure_ascii=False) + "\n")
            count += 1

        except Exception:
            continue

print(f"Stories loaded: {count:,}")
print("Creating embeddings...")

embeddings = model.encode(
    texts, batch_size=32, show_progress_bar=True, convert_to_numpy=True
)

embeddings = embeddings.astype(np.float32)

print("Normalizing embeddings...")
faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

print("Building FAISS index...")
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

print("Saving files...")
faiss.write_index(index, "stories.index")
np.save("embeddings.npy", embeddings)

print("\nDone!")
print("Stories indexed:", index.ntotal)
print("Index file: stories.index")
print("Embeddings: embeddings.npy")
print("Metadata: metadata.jsonl")
