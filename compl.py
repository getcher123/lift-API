import aiohttp
import asyncio
import time
import os
import time
from openai.embeddings_utils import get_embedding
from scipy.spatial.distance import cosine
import math

class Customer:
    def __init__(self, df):
        self.df = df
        self.maxStage = df.shape[0]
        self.stage = 0
        self.first_phrase = os.environ['FIRST_PHRASE']
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

        
    
