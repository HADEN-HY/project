from keras.models import load_model
import cv2
import numpy as np

#Disable scientific notation for clarity
np.set_printoptions(suppress = True)

#Load the model
model = load_model("keras_model.h5",compile = False)

#Load the labels
class_name = open("labels.txt", "r").readlines()

#CAMERA can be 0 or 1 based on default camera of your computer 
camera = cv2.VideoCapture(0)

while True:
    ret, image = camera.read()

    #set image pixels
    image = cv2.resize(image, (224, 224), interpoation = cv2.INTER_AREA)

    #Show image
    cv2.imshow("Cam image", image)

    #Make the image a numpy array and reshape to input shap
    image = np.asarray(image, dtype = np.float32).reshap(1, 224, 224, 3)

    #Normalize the image array
    image = (image / 127.5) -1

    #Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_name[index]
    confidence_score = prediction[0][index]

    #Print prediction and confidence
    print("Class:", class_name[2:], end = "")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    if cv2.waitKey(1) &0xFF == ord('q'):
        break      

camera.release()
cv2.destroyAllWindows()
