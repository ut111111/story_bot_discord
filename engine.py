import json
import random
import faiss
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from collections import Counter

def normalize_tag(tag):

    if not tag:
        return None

    tag = tag.strip().title()

    fixes = {
        "Roomate": "Roommate",
    }

    return fixes.get(tag, tag)


print("Loading metadata...")

metadata = []

with open("metadata.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        metadata.append(json.loads(line))

print(f"Loaded {len(metadata):,} stories")


print("Building tag/year indexes...")

stories_by_tag = {}
stories_by_year = {}

for story in metadata:

    tag = normalize_tag(
        story.get("tag")
    )

    if tag:
        stories_by_tag.setdefault(
            tag,
            []
        ).append(story)

    try:

        created_utc = int(
            story["created_utc"]
        )

        year = datetime.utcfromtimestamp(
            created_utc
        ).year

        stories_by_year.setdefault(
            year,
            []
        ).append(story)

    except Exception:
        pass

print(f"Tags: {len(stories_by_tag)}")
print(f"Years: {len(stories_by_year)}")


print("Loading full stories...")

full_stories = {}

with open("all_stories_rich.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        story = json.loads(line)
        full_stories[story["id"]] = story

print(f"Loaded {len(full_stories):,} full stories")


print("Loading FAISS index...")

index = faiss.read_index("stories.index")

print("Index loaded")

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded")

def random_story():
    return random.choice(metadata)


def get_full_story(story_id):
    return full_stories.get(story_id)


def split_story(text, size=1800):

    return [
        text[i:i + size]
        for i in range(0, len(text), size)
    ]


def format_story_card(story):

    preview = (
        story["story_preview"]
        .replace("\n", " ")
        .strip()[:500]
    )

    return (
        f"📖 **{story['title']}**\n\n"
        f"{preview}..."
    )


def top_stories(limit=100):

    return sorted(
        metadata,
        key=lambda x: x["score"],
        reverse=True
    )[:limit]


def format_top_story(story, rank):

    try:
        year = datetime.utcfromtimestamp(
            int(story["created_utc"])
        ).year
    except Exception:
        year = "Unknown"

    preview = (
        story["story_preview"]
        .replace("\n", " ")
        .strip()[:300]
    )

    return (
        f"🏆 **Top Story #{rank}**\n\n"
        f"📖 **{story['title']}**\n\n"
        f"⭐ Score: {story['score']:,}\n"
        f"📅 Year: {year}\n"
        f"📝 Words: {story['word_count']:,}\n\n"
        f"{preview}..."
    )


def get_tags():
    return sorted(stories_by_tag.keys())


def get_tag_stories(tag):
    return stories_by_tag.get(tag, [])


def get_years():
    return sorted(stories_by_year.keys())


def get_year_stories(year):
    return stories_by_year.get(year, [])
def semantic_search(query, limit=20):

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    faiss.normalize_L2(
        query_embedding
    )

    scores, ids = index.search(
        query_embedding,
        limit
    )

    results = []

    for idx in ids[0]:

        if idx < 0:
            continue

        results.append(
            metadata[idx]
        )

    return results
def get_stats():

    total_stories = len(metadata)

    total_tags = len(stories_by_tag)

    years = sorted(stories_by_year.keys())

    total_words = sum(
        story.get("word_count", 0)
        for story in metadata
    )

    longest_story = max(
        metadata,
        key=lambda x: x.get(
            "word_count",
            0
        )
    )

    highest_score = max(
        metadata,
        key=lambda x: x.get(
            "score",
            0
        )
    )

    tags = Counter()

    for story in metadata:

        tag = normalize_tag(
            story.get("tag")
        )

        if tag:
            tags[tag] += 1

    return {
        "total_stories": total_stories,
        "total_tags": total_tags,
        "first_year": years[0],
        "last_year": years[-1],
        "total_words": total_words,
        "longest_story": longest_story,
        "highest_score": highest_score,
        "top_tags": tags.most_common(5)
    }
