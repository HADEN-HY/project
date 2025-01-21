#before start 'pip install openai pyttsx3 speechrecogntiton'

import openai
import speech_recognition as sr
import pyttsx3  # 음성 합성 라이브러리

# OpenAI API 키 설정
openai.api_key = 'YOUR_OPENAI_API_KEY' 

# 음성 인식 함수
def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='ko-KR')
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Google Speech could not understand")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from google service; {e}")
        return None

# ChatGPT와 연결하여 응답 받기 (기본 모델 사용)
def get_chatgpt_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",  # 기본 모델
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# 음성으로 출력하기
def speak_text(text):
    engine = pyttsx3.init()  # 음성 합성 엔진 초기화
    engine.say(text)  # 텍스트 음성으로 변환
    engine.runAndWait()  # 음성 출력 대기

# 메인 루프
try:
    while True:
        # 음성 인식
        speech_text = recognize_speech()
        
        if speech_text:
            # ChatGPT 응답 받기
            gpt_response = get_chatgpt_response(speech_text)
            print(f"ChatGPT says: {gpt_response}")
            
            # 응답을 음성으로 출력
            speak_text(gpt_response)

except KeyboardInterrupt:
    pass