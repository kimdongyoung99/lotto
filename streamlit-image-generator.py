import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Unsplash API 키 설정 (실제 키로 교체 필요)
UNSPLASH_ACCESS_KEY = 'YOUR_UNSPLASH_ACCESS_KEY'

def fetch_image_from_unsplash(prompt, count=2):
    endpoint = f"https://api.unsplash.com/search/photos"
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
    }
    params = {
        'query': prompt,
        'per_page': count
    }
    
    response = requests.get(endpoint, headers=headers, params=params)
    data = response.json()
    return [item['urls']['regular'] for item in data['results']]

def main():
    st.set_page_config(page_title="AI Image Generator", page_icon="🖼️", layout="wide")

    # 배경 이미지 설정
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("https://source.unsplash.com/1600x900/?nature,technology");
        background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # 앱 제목
    st.title("AI Image Generator")

    # 사이드바에 모델 선택 옵션 추가
    model = st.sidebar.selectbox(
        "Choose a model",
        ("AI Generated", "Real Photo")
    )

    # 메인 영역에 프롬프트 입력 필드 추가
    prompt = st.text_input("Enter your prompt here...")

    if st.button("Generate"):
        if prompt:
            with st.spinner('Generating images...'):
                try:
                    image_urls = fetch_image_from_unsplash(prompt)
                    
                    # 이미지 표시
                    cols = st.columns(2)
                    for idx, img_url in enumerate(image_urls):
                        response = requests.get(img_url)
                        img = Image.open(BytesIO(response.content))
                        cols[idx].image(img, caption=f"Image {idx+1} based on: '{prompt}'", use_column_width=True)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a prompt.")

    # 면책 조항
    st.markdown("---")
    st.caption("Disclaimer: This app uses the Unsplash API to fetch relevant images based on your prompt.")

if __name__ == "__main__":
    main()
