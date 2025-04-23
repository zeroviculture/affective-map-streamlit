
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# --- 데이터 로드 (엑셀 기반 정동 descriptor + category + color)
descriptor_data = [
    ("uneasy", "Tension / Unease", (1.0, 0.2, 0.2, 1.0)),
    ("melancholic", "Melancholy / Sentimentality", (0.2, 0.4, 1.0, 1.0)),
    ("tense", "Tension / Unease", (1.0, 0.2, 0.2, 1.0)),
    ("poignant", "Melancholy / Sentimentality", (0.2, 0.4, 1.0, 1.0)),
    ("exposed", "Explicitness / Exposure", (1.0, 0.1, 0.1, 1.0)),
    ("nostalgic", "Melancholy / Sentimentality", (0.2, 0.4, 1.0, 1.0)),
    ("playful", "Play / Lightness", (1.0, 0.9, 0.3, 1.0)),
    ("serious", "Gravitas / Seriousness", (0.5, 0.5, 0.5, 1.0)),
    ("uncanny", "Strangeness / Uncanny", (1.0, 0.5, 0.2, 1.0)),
    ("sublime", "Sublimity / Ominousness", (0.6, 0.2, 0.8, 1.0)),
    ("meta", "meta-affect", (0.8, 0.4, 0.9, 1.0))
]
df = pd.DataFrame(descriptor_data, columns=["Descriptor", "Category", "Color"])

# --- Streamlit 앱 시작
st.set_page_config(layout="wide")
st.title("Affective Terrain Map Generator")

# --- 사용자 입력: descriptor 선택
selected_descriptors = st.multiselect(
    "Select Descriptors (up to 10)",
    options=df["Descriptor"].unique(),
    default=df["Descriptor"].unique()[:4]
)

# --- 지형 생성
width, height = 100, 100
canvas = np.zeros((height, width, 4))  # RGBA

np.random.seed(42)  # 재현 가능성
for desc in selected_descriptors:
    row = df[df["Descriptor"] == desc].iloc[0]
    x, y = np.random.randint(20, 80), np.random.randint(20, 80)
    intensity_map = np.zeros((height, width))
    intensity_map[y, x] = 1.0
    blurred = gaussian_filter(intensity_map, sigma=12)
    color = row['Color']
    for i in range(4):
        canvas[:, :, i] += blurred * color[i]

# 정규화
for i in range(3):
    max_val = canvas[:, :, i].max()
    if max_val > 0:
        canvas[:, :, i] /= max_val

# --- 시각화 출력
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(canvas, origin='lower')
ax.set_title("Flow-based Affective Terrain Map")
ax.axis('off')
st.pyplot(fig)

# --- 범례 표시
if st.checkbox("Show Legend"):
    st.dataframe(df[df["Descriptor"].isin(selected_descriptors)])
