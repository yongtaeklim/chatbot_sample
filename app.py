import streamlit as st
from transformers import pipeline
import openai

# 페이지 설정
st.set_page_config(page_title="Chatbot Interface", layout="centered")

st.title("Chatbot Interface")

# 챗봇 모드 선택
chat_mode = st.radio("Choose the chatbot mode:", ("Hugging Face Model", "ChatGPT API"))

# 대화 기록 초기화
if "recent_chat_list" not in st.session_state:
    st.session_state.recent_chat_list = []

# 초기화 버튼
if st.button("Reset Chat"):
    st.session_state.recent_chat_list = []
    st.success("Chat history has been reset.")

# Hugging Face 모델 사용 시
if chat_mode == "Hugging Face Model":
    model_id = st.text_input("Enter Hugging Face Model ID (e.g., gpt2)")
    hf_system_prompt = st.text_area("Enter system prompt for Hugging Face model")

    if model_id:
        # Hugging Face 모델 로드
        try:
            hf_pipeline = pipeline("text-generation", model=model_id)
        except Exception as e:
            st.error(f"Error loading Hugging Face model: {e}")

# ChatGPT API 사용 시
elif chat_mode == "ChatGPT API":
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    chatgpt_model = st.text_input("Enter ChatGPT Model (e.g., gpt-3.5-turbo)")
    gpt_system_prompt = st.text_area("Enter system prompt for ChatGPT")

# 사용자 입력
user_input = st.text_input("Your message:")

if user_input:
    # 유저 입력 저장
    st.session_state.recent_chat_list.append({"role": "user", "content": user_input})

    if chat_mode == "Hugging Face Model" and model_id:
        try:
            # 시스템 프롬프트와 대화 기록을 합쳐 Hugging Face 모델 입력
            hf_input = hf_system_prompt + " ".join([msg["content"] for msg in st.session_state.recent_chat_list])
            hf_response = hf_pipeline(hf_input, max_length=100)[0]["generated_text"]
            st.session_state.recent_chat_list.append({"role": "assistant", "content": hf_response})
        except Exception as e:
            st.error(f"Error generating response with Hugging Face model: {e}")

    elif chat_mode == "ChatGPT API" and openai_api_key and chatgpt_model:
        try:
            # OpenAI API 호출에 대화 기록과 시스템 프롬프트 포함
            openai.api_key = openai_api_key
            messages = [{"role": "system", "content": gpt_system_prompt}] + st.session_state.recent_chat_list
            response = openai.ChatCompletion.create(model=chatgpt_model, messages=messages)
            chatgpt_response = response.choices[0].message['content']
            st.session_state.recent_chat_list.append({"role": "assistant", "content": chatgpt_response})
        except Exception as e:
            st.error(f"Error generating response with ChatGPT API: {e}")

# 대화 내용 표시
for chat in st.session_state.recent_chat_list:
    if chat["role"] == "user":
        st.write(f"**User:** {chat['content']}")
    elif chat["role"] == "assistant":
        st.write(f"**Bot:** {chat['content']}")
