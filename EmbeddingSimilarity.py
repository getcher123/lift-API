import pandas as pd
import sys
import time

from openai.embeddings_utils import get_embedding
from scipy.spatial.distance import cosine

from Morph.stopwords import TextProcessor


class EmbeddingSimilarity:
    def __init__(self, df, collumn_emb, embedding_model="text-embedding-ada-002", max_tokens=8000):
        self.df = df
        self.embedding_model = embedding_model
        self.max_tokens = max_tokens
        self.collumn_emb = collumn_emb
        self._init_data()

    def _init_data(self):
        # generate embeddings for Employee Question column
        self.df[self.collumn_emb + " Embedding"] = self.df[self.collumn_emb].apply(
            lambda x: get_embedding(x, engine=self.embedding_model))
        print(self.df)

    def get_similarity(self, query_embedding):
        start_time = time.time()
        self.df["similarity"] = self.df[self.collumn_emb +
                                        " Embedding"].apply(lambda x: 1 - cosine(query_embedding, x))
        most_similar = self.df.sort_values(
            "similarity", ascending=False).iloc[0]
        end_time = time.time()
        response_time = end_time - start_time
        print(f"Searching of embedding time: {response_time:.2f} seconds")
        memory_usage = self.df.memory_usage(deep=True).sum()
        # выводим результат
        print(f"Размер DataFrame: {memory_usage} байт")
        return most_similar.drop(self.collumn_emb + " Embedding")
