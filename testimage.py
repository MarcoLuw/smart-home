import cv2
import base64


rawImg = cv2.imread("jack.jpg")
print( len(rawImg)  )

rawImg = cv2.resize(rawImg, (640, 480))

r, data = cv2.imencode(".jpg", rawImg,[cv2.IMWRITE_JPEG_QUALITY, 70])
print( len(data)  )

data = base64.b64encode(data)
print( len(data)  )