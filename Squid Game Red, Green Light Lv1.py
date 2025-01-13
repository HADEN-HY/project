from gpiozero import LED, MotionSensor
import time
import os
import random

# LED 설정
Red_Light = LED(2)
Green_Light = LED(3)

# PIR 센서 설정
pirPin = MotionSensor(16)

# 게임 시간 (2분 30초 = 150초)
GAME_TIME_LIMIT = 150
MOVEMENT_TIMEOUT = 10  # 빨간불 상태에서 최대 대기 시간 (10초)

def speak(option, msg):
    os.system("espeak {} '{}'".format(option, msg))

def game_round():
    option = '-s 180 -p 50 -a 200 -v ko+f5'
    
    # 초록불 상태 (움직일 수 있음)
    Green_Light.on()
    Red_Light.off()
    msg = 'Green Light!'
    speak(option, msg)
    time.sleep(random.randint(3, 6))  # 초록불 지속 시간 (3~6초 랜덤)

    # 빨간불 상태 (움직이면 게임 오버)
    Green_Light.off()
    Red_Light.on()
    msg = 'Red Light! Stop moving!'
    speak(option, msg)
    time.sleep(6.0)  # 빨간불 지속 시간 (6초)

    # 빨간불일 때 움직임 감지 (최대 10초 대기)
    print("Checking for movement during Red Light...")
    start_wait = time.time()
    
    while time.time() - start_wait < MOVEMENT_TIMEOUT:
        if pirPin.value == 1:  # 움직임 감지 시
            print("Game Over: You moved during Red Light!")
            return False  # 게임 오버
        time.sleep(0.1)  # 조금씩 대기하며 계속 확인
    
    print("No movement detected during Red Light.")
    return True  # 성공적으로 지나감

def main():
    start_time = time.time()  # 게임 시작 시간 기록
    try:
        while True:
            elapsed_time = time.time() - start_time  # 경과 시간 계산

            # 게임 시간이 초과되면 종료
            if elapsed_time >= GAME_TIME_LIMIT:
                print("Time's up! Game Over!")
                break

            if not game_round():
                break  # 게임 오버 시 종료
            time.sleep(1)  # 라운드 간의 짧은 대기 시간

    except KeyboardInterrupt:
        pass