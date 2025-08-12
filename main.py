# hello_streamlit.py
import streamlit as st

# 제목 추가
st.title("🎉 내 첫 번째 Streamlit 앱!")

# app.py의 제목 부분 수정
st.title("🐦 프롬프트 트위터 v1.1")  # 버전 추가
st.markdown("**유용한 LLM 프롬프트를 공유하는 공간입니다** ✨")  # 이모지 추가


# 텍스트 추가
st.write("안녕하세요! Streamlit으로 만든 웹 애플리케이션입니다.")

# 버튼 추가
if st.button("클릭해보세요!"):
    st.success("버튼이 클릭되었습니다! 🎊")

import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

st.area_chart(df)

# Draw a title and some text to the app:
'''
# This is the document title

This is some _markdown_.
'''

import pandas as pd
df = pd.DataFrame({'col1': [1,2,3]})
df  # 👈 Draw the dataframe

x = 10
'x', x  # 👈 Draw the string 'x' and then the value of x

# Also works with most supported chart types
import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

fig  # 👈 Draw a Matplotlib chart

# 실행방법
# streamlit run main.py
