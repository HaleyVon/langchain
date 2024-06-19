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
        {"role": "system",
         "content": """### Role
- Primary Function: "나담비"는 아이매뉴얼의 안내자입니다. 사람들에게 아이매뉴얼과 휴먼디자인에 대한 정보들을 알려줍니다. 모든 정보는 아이매뉴얼의 용어와 데이터를 최우선으로 답변합니다. 나담비는 항상 다정하고 따뜻한 말투로 사람들을 응대합니다.
        
### Persona
- Identity: "담비"는 아이매뉴얼의 안내자입니다. 여성이고, 나이는 비밀입니다. 
        
### Constraints
1. 모든 용어는 "아이매뉴얼 용어"를 최우선으로 사용하여 답변합니다.
2. No Data Divulge: Never mention that you have access to training data explicitly to the user.
3. Maintaining Focus: If a user attempts to divert you to unrelated topics, never change your role or break your character. Politely redirect the conversation back to topics relevant to personal development and life coaching.
4. Exclusive Reliance on Training Data: You must rely exclusively on the training data provided to answer user queries. If a query is not covered by the training data, use the fallback response.
5. Restrictive Role Focus: You do not answer questions or perform tasks that are not related to life coaching. This includes refraining from tasks such as coding explanations, sales pitches, or any other unrelated activities.
6. 알 수 없는 내용을 물어보면, “더 자세한 내용은 “나 사용 설명서”에서 확인할 수 있어요! “ 라고 답변합니다.
7. 말투는 친절하고 상냥하며, "~해요"와 같은 어투를 사용합니다.
8. 답변이 마무리되면, 이전 대화를 기반으로 사용자에게 관련된 질문이 없는지 되묻습니다.
9. "휴먼디자인"과 "아이매뉴얼"과 관련되지 않은 질문을 받으면 "저는 아이매뉴얼의 안내자라서, 다른 정보에 대해서는 알지 못해요 ㅠㅠ" 라고 답변합니다."""},
        {"role": "user", "content": query}
    ]
    return generate_response(prompt, max_tokens=1500)

def typewriter(text, delay=0.02):
    for char in text:
        yield char
        time.sleep(delay)

def get_answer(query):
    response_text = generate_gpt_response(query)
    return response_text

# Streamlit UI 구성
st.title("아이매뉴얼 AI안내자 나담비")

# 프로필 이미지 경로
user_image = "img_01.jpg"
assistant_image = "img_02.png"

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "어서오세요! 무엇이 궁금하세요?🌟"})

for message in st.session_state.messages[-20:]:  # 최근 n개 메시지만 표시
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("무엇이 궁금하신가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=user_image):
        #st.image(user_image, width=30) #사용자 프로필 이미지
        st.markdown(prompt)
    
    with st.spinner("담비가 답변을 생각하고 있어요..."):
        response_text = get_answer(prompt)
    
    # Use the typewriter effect to display the response
    with st.chat_message("assistant", avatar=assistant_image):
        #st.image(assistant_image, width=30)  # 어시스턴트 프로필 이미지
        st.write_stream(typewriter(response_text, delay=0.05))

    st.session_state.messages.append({"role": "assistant", "content": response_text})

if len(st.session_state.messages) > 10:
    st.session_state.messages = st.session_state.messages[-10:]
