import os
import pandas as pd
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
from qdrant_client.http import model

load_dotenv()

endpoint = " "
deployment = " "
apiKey = " "

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=apiKey,
    api_version="2024-08-01-preview"
)

# embedding 模型
model = 'text-embedding-3-large'
SIMILARITIES_RESULTS_THRESHOLD = 0.75
DATASET_NAME = "../embedding_index_3m.json"


# 加载JSON 数据
def load_dataset(source: str) -> pd.core.frame.DataFrame:
    pd_vectors = pd.read_json(source)
    return pd_vectors.drop(columns=["text"], errors="ignore").fillna("")


# 余弦相似度
def cosine_similarity(a, b):
    if len(a) > len(b):
        b = np.pad(b, (0, len(a) - len(b)), 'constant')
    elif len(b) > len(a):
        a = np.pad(a, (0, len(b) - len(a)), 'constant')
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 获取视频
def get_videos(
        query: str, dataset: pd.core.frame.DataFrame, rows: int
) -> pd.core.frame.DataFrame:
    video_vectors = dataset.copy()
    query_embeddings = client.embeddings.create(input=query, model=model).data[0].embedding

    video_vectors["similarity"] = video_vectors["ada_v2"].apply(
        lambda x: cosine_similarity(np.array(query_embeddings), np.array(x))
    )

    mask = video_vectors["similarity"] >= SIMILARITIES_RESULTS_THRESHOLD
    video_vectors = video_vectors[mask].copy()

    video_vectors = video_vectors.sort_values(by="similarity", ascending=False).head(rows)

    return video_vectors.head(rows)


def display_results(videos: pd.core.frame.DataFrame, query: str):
    def _gen_yt_url(video_id: str, seconds: int) -> str:
        """convert time in format 00:00:00 to seconds"""
        return f"https://youtu.be/{video_id}?t={seconds}"

    print(f"\nVideos similar to '{query}':")
    for _, row in videos.iterrows():
        youtube_url = _gen_yt_url(row["videoId"], row["seconds"])
        print(f" - {row['title']}")
        print(f"   Summary: {' '.join(row['summary'].split()[:15])}...")
        print(f"   YouTube: {youtube_url}")
        print(f"   Similarity: {row['similarity']}")
        print(f"   Speakers: {row['speaker']}")


pd_vestors=load_dataset(DATASET_NAME)

while True:
    query=input("Enter a query:")
    if query =="exit":
        break
    videos = get_videos(query, pd_vestors, 5)
    display_results(videos,query)


