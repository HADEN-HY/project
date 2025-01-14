import speech_recognition as sr
import requests
import re
import os

# 기상청 API URL
url = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2635053000'

# 음성을 출력하는 함수
def speak(option, msg):
    os.system("espeak {} '{}'".format(option, msg))

# 메인 코드
try:
    while True:
        # 음성 인식 초기화
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            # 음성을 텍스트로 변환
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)

            # "날씨"라는 명령어 감지
            if "날씨" in text:
                print("날씨 정보 검색 중...")

                # 기상청 API 요청
                response = requests.get(url)
                temp = re.findall(r'<temp>(.+)</temp>', response.text)
                humi = re.findall(r'<reh>(.+)</reh>', response.text)

                # 결과 메시지 생성
                msg = f"기온은 {int(float(temp[0]))}도, 습도는 {humi[0]} 퍼센트 입니다."

                # TTS 출력
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option, msg)

        except sr.UnknownValueError:
            print("Google Speech could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google service: {e}")

except KeyboardInterrupt:
    pass