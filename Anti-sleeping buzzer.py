import cv2
from gpiozero import Buzzer
import time

buzzerPin = Buzzer(16)

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

    # Haar Cascade 파일 로드
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'
    face_cascade = cv2.CascadeClassifier(face_xml)
    eyes_cascade = cv2.CascadeClassifier(eye_xml)

    while True:
        ret, image = camera.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 얼굴 검출
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        print("Faces detected: " + str(len(faces)))

        # 얼굴 및 눈 검출
        if len(faces) == 0:
            buzzerPin.on()  # 얼굴이 검출되지 않을 경우 부저 켬
        else:
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                face_gray = gray[y:y + h, x:x + w]
                face_color = image[y:y + h, x:x + w]

                # 눈 검출
                eyes = eyes_cascade.detectMultiScale(
                    face_gray,
                    scaleFactor=1.1,
                    minNeighbors=5
                )

                # 부저 작동
                if len(eyes) <= 1:  # 눈이 1개 이하일 경우
                    buzzerPin.on()
                else:
                    buzzerPin.off()

                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        cv2.imshow('result', image)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    buzzerPin.off()

if __name__ == '__main__':
    main()   
