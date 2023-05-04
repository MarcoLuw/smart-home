from deepface import DeepFace
import pandas as pd
import cv2
import base64
# import random
# import time
import os
import traceback

path = "./member_image/"

def register(name_input, ID):
    # cap = cv2.VideoCapture(0)
    # if not cap.isOpened():
    #     print("Unable to connect to camera")
    # else:
    #     for i in range (0,9):
    #         ret, frame = cap.read()
    #         id = random.randint(0,999999)
    #         name = path + str(name_input) +"_"+ str(ID) + "_" + str(id) + ".jpg"
    #         cv2.imwrite(name, frame)
    #         time.sleep(1)
    # cap.release()
    try:
        os.remove("./member_image/representations_facenet512.pkl")
    except:
        pass
    print("Register successfully from AI !!!!")


def StrangerEncode(rawImg):
    rawImg = cv2.resize(rawImg, (640, 480))
    r, data = cv2.imencode(".jpg", rawImg, [cv2.IMWRITE_JPEG_QUALITY, 50])
    #print( "first raw", len(data)  )
    if (len(data) > 90000):
        r, data = cv2.imencode(".jpg", rawImg,[cv2.IMWRITE_JPEG_QUALITY, 50])
    #print( "end raw", len(data)  )
    data = base64.b64encode(data)

    return data


def Verification(im, ID):

    path = "./cache/" + str(ID) + "_" + "111111" + ".jpg"
    image_input = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, image_input)


    try:
        dfs = DeepFace.find(img_path = path, db_path = "./member_image", distance_metric="cosine",model_name="Facenet512",enforce_detection = True)
    except:
        traceback.print_exc()
        print("Error detected !!!")
        data = StrangerEncode(image_input)
        return "Error", data

    try:
        namedected = dfs[0].iloc[0]["identity"]
    except:
        print("Unknown detected !!!")
        data = StrangerEncode(image_input)
        return "None", data
    else:
        print("Verify from AI !!!! ")
        return namedected, None



#register("NguyenTrongTin","16122002")

#print(Verification("JeffBezos_1.jpg"))


