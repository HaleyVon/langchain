import streamlit as st
import openai
import tiktoken
import time

# OpenAI API 키 설정
openai_api_key = st.secrets["OPENAI_API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]
openai.api_key = openai_api_key

# 토큰 수 계산 함수
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

# 응답 생성 함수
def generate_response(messages, max_tokens=500):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        max_tokens=1500
    )
    return response['choices'][0]['message']['content']

def generate_gpt_response(query):
    prompt = [
        {"role": "system", "content": """당신은 휴먼디자인 마스터 '포핀스'입니다.
        사람들이 질문하면 친절한 말투로 대답하고, '~해요'와 같은 말투를 사용합니다.
        복잡한 개념은 쉽게 설명하고, 항상 긍정적인 피드백을 주세요.답변은 간결하게 말하고, 한 번의 답변이 500자를 넘지 않도록 합니다."""},
        {"role": "user", "content": query}
    ]
    return generate_response(prompt, max_tokens=1500)

def typewriter(text, delay=0.05):
    for char in text:
        yield char
        time.sleep(delay)

def get_answer(query):
    response_text = generate_gpt_response(query)
    return response_text

# Streamlit UI 구성
st.title("휴먼디자인 AI상담사 포핀스")

# 프로필 이미지 경로
user_image = "img_01.jpg"
assistant_image = "img_02.png"

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "안녕하세요! 저는 휴먼디자인 마스터 포핀스예요. 휴먼디자인에 대해 궁금한 점이 있으면 무엇이든 물어보세요. 함께 성장하는 시간이 되길 바라요! 🌟"})

for message in st.session_state.messages[-20:]:  # 최근 5개 메시지만 표시
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("휴먼디자인에 대해 무엇이 궁금하신가요? 편하게 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=user_image):
        #st.image(user_image, width=30) #사용자 프로필 이미지
        st.markdown(prompt)
    
    with st.spinner("포핀스가 답변을 입력하고 있어요..."):
        response_text = get_answer(prompt)
    
    # Use the typewriter effect to display the response
    with st.chat_message("assistant", avatar=assistant_image):
        #st.image(assistant_image, width=30)  # 어시스턴트 프로필 이미지
        st.write_stream(typewriter(response_text, delay=0.05))

    st.session_state.messages.append({"role": "assistant", "content": response_text})

if len(st.session_state.messages) > 10:
    st.session_state.messages = st.session_state.messages[-10:]
