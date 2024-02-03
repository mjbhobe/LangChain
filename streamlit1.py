import os, sys
from dotenv import load_dotenv
import streamlit as st
import numpy as np
import pandas as pd

load_dotenv()
print(f"OPENAI_API_KEY = {os.getenv('OPENAI_API_KEY')}")

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        },
        {
            "role": "user",
            "content": "Compose a poem that explains the concept of recursion in programming.",
        },
    ],
)

print(completion.choices[0].message)
sys.exit(-1)


mumbai = [19.08, 72.88]
san_fran = [37.76, -122.4]

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [25, 50] + [19.08, 72.88],
    columns=["lat", "lon"],
)

st.map(map_data)
