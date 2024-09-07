import streamlit as st
from openai import OpenAI
import os

# OpenAI 클라이언트 초기화
openai_api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=openai_api_key)

# Streamlit 앱 레이아웃
st.title("AI 이미지 생성기")
st.write("텍스트 프롬프트를 입력하고 AI 이미지를 생성하세요.")

# 텍스트 입력
prompt = st.text_input("프롬프트를 입력하세요:")

# 이미지 사이즈 선택
image_size = st.selectbox(
    "이미지 크기를 선택하세요:",
    ("256x256", "512x512", "1024x1024")
)

# 그림 화풍 선택
style = st.radio(
    "그림 화풍을 선택하세요:",
    ("기본", "모네 스타일", "고흐 스타일", "피카소 스타일")
)

# 화풍에 따른 프롬프트 수정 함수
def apply_style(prompt, style):
    if style == "모네 스타일":
        return f"A painting in the style of Claude Monet: {prompt}"
    elif style == "고흐 스타일":
        return f"A painting in the style of Vincent van Gogh: {prompt}"
    elif style == "피카소 스타일":
        return f"A painting in the style of Pablo Picasso: {prompt}"
    else:
        return prompt

if st.button("이미지 생성"):
    if prompt:
        try:
            styled_prompt = apply_style(prompt, style)
            kwargs = {
                "prompt": styled_prompt,
                "n": 1,
                "size": image_size
            }

            # OpenAI API를 사용하여 이미지 생성
            response = client.images.generate(**kwargs)

            # 응답에서 이미지 URL 추출
            image_url = response.data[0].url

            # 생성된 이미지 표시
            st.image(image_url, caption="생성된 이미지", use_column_width=True)

        except Exception as e:
            st.error(f"이미지 생성 중 오류 발생: {e}")
    else:
        st.warning("이미지를 생성하려면 프롬프트를 입력하세요.")
