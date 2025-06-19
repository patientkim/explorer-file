import streamlit as st
import requests

# 🔍 검색 함수
def search_artworks(query):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    return response.json().get("objectIDs", [])[:10]  # 상위 10개만 반환

# 📄 상세정보 함수
def get_artwork_details(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    return requests.get(url).json()

# 🎨 Streamlit 앱 UI 시작
st.title("🎨 Explore Artworks with MET Museum API")

# 🔡 사용자 입력
query = st.text_input("Search for Artworks:")

# 🔍 검색 실행
if query:
    ids = search_artworks(query)

    if not ids:
        st.warning("No artworks found for that search.")
    else:
        for object_id in ids:
            data = get_artwork_details(object_id)

            # 제목 표시
            st.subheader(data.get("title", "Untitled"))

            # 이미지 표시 (있을 경우에만)
            image_url = data.get("primaryImageSmall")
            if image_url:
                st.image(image_url, width=300)
            else:
                st.info("No image available.")

            # 작가와 연도 정보 표시
            st.write(f"**Artist:** {data.get('artistDisplayName', 'Unknown')}")
            st.write(f"**Year:** {data.get('objectDate', 'N/A')}")
            st.markdown("---")
