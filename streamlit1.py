import streamlit as st
import numpy as np
import pandas as pd

mumbai = [19.08, 72.88]
san_fran = [37.76, -122.4]

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [25, 50] + [19.08, 72.88],
    columns=["lat", "lon"],
)

st.map(map_data)
