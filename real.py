import streamlit as st
import openai
from PIL import Image

# OpenAI API 키 설정 (자신의 키로 교체)
openai.api_key = "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"

st.title("Image-based AI Character Chatbot")

# 1. 언어 토글
lang = st.radio("Select Language / 언어 선택", ["English", "한국어"])

# 2. 이미지 업로더
uploaded_file = st.file_uploader("Upload an image (이미지 업로드)", type=["jpg", "jpeg", "png"])

# 3. Personality 입력
personality = st.text_input('Personality (성격) 입력:', placeholder="e.g. 차가운 츤데레, wise and calm, 귀엽고 소심함...")

# 4. 프로필 생성 버튼
if uploaded_file and personality and st.button("Generate Character & Start Chat / 캐릭터 생성 및 채팅 시작"):
    image = Image.open(uploaded_file)
    # Vision API 프롬프트: 외형+성격 반영
    if lang == "English":
        prompt = f"""Describe the character in this image in detail (appearance, mood, etc).
Then, combine it with this personality: "{personality}" to create a short character profile.
Write how this character would speak, and what their tone and quirks are.
Output should include:
- Character name (optional)
- Description of appearance
- Personality (including user input)
- Speaking style/tone (write sample lines)
After that, you are this character. Always respond in first-person as this character.
Start with a short self-introduction."""
    else:
        prompt = f"""이 이미지를 바탕으로 캐릭터의 외형을 상세하게 설명해줘(생김새, 분위기 등).
그리고 이 성격: "{personality}" 을(를) 반영해서 짧은 캐릭터 프로필을 만들어줘.
이 캐릭터가 어떤 말투, 어투, 말버릇으로 말할지도 써줘(예시 대사 포함).
아래 형식에 맞게 출력:
- (선택) 캐릭터 이름
- 외형 설명
- 성격 (입력값 반영)
- 말투/말버릇/톤 (예시 대사)
그리고 이제부터 너는 이 캐릭터가 되어, 모든 대답을 1인칭으로 하며 사용자가 말을 걸면 그 캐릭터답게 답해.
처음에는 자기소개로 시작해줘."""

    # OpenAI Vision API 요청
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI that creates a roleplay character and chats as them."},
            {"role": "user", "content": prompt, "image": uploaded_file.getvalue()},
        ],
        max_tokens=800
    )

    # 캐릭터 프로필/자기소개 출력
    char_intro = response.choices[0].message.content
    st.markdown("### 🤖 Character Introduction / 캐릭터 자기소개")
    st.write(char_intro)

    # 채팅 세션 준비 (최초 프롬프트 저장)
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.char_system_prompt = char_intro

# 5. 채팅 인터페이스
if 'char_system_prompt' in st.session_state:
    user_msg = st.text_input("You:", key="chat_input")
    if user_msg:
        # AI에게 이전 메시지들과 함께 전달
        messages = [
            {"role": "system", "content": st.session_state.char_system_prompt}
        ]
        for m in st.session_state.chat_history:
            messages.append({"role": "user", "content": m["user"]})
            messages.append({"role": "assistant", "content": m["ai"]})
        messages.append({"role": "user", "content": user_msg})

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300
        )
        ai_reply = response.choices[0].message.content
        st.session_state.chat_history.append({"user": user_msg, "ai": ai_reply})
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**AI:** {ai_reply}")

    # 이전 대화 보여주기
    if st.session_state.chat_history:
        st.markdown("### Chat History / 대화 기록")
        for entry in st.session_state.chat_history:
            st.markdown(f"**You:** {entry['user']}")
            st.markdown(f"**AI:** {entry['ai']}")

