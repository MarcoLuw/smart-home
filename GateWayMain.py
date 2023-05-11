import sys
from Adafruit_IO import MQTTClient, Client, Feed
import time
import serial.tools.list_ports



ser = None




#1.-----config login Ada
AIO_USERNAME = "jackwrion12345"
AIO_KEY = "aio_jgfr16Jb92VLez2J9XJ1ooVLxTsq"


#2.-----Connect Microbit
def getPort () :
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range (0 , N) :
        port = ports [ i ]
        strPort = str( port )
        if "USB-SERIAL CH340" in strPort :
            splitPort = strPort.split (" ")
            commPort = ( splitPort [0])
    return commPort

def ConnectPort():
    port = getPort()
    if (port == 'None'): return
    return serial.Serial(port , baudrate =115200)


def accessPort():
    global ser
    ser = ConnectPort()
    print('Connecting Serial: ' , ser)



#3.------Connect Adafruit

#Function about Adafruit
def connected ( client ) :
    print ("Ket noi thanh cong ...")
    client.subscribe( "bbc-led" )
    client.subscribe( "door" )
    client.subscribe( "alert" )

    #client.subscribe( 'face-reg' )

def subscribe ( client , userdata , mid , granted_qos ) :
    print("Subcribe thanh cong ...", mid)

def disconnected ( client ) :
    print("Ngat ket noi ...")
    sys.exit(1)

def message ( client , feed_id , payload ):
    print (" Nhan du lieu tu " + str(feed_id) + ' : ' + payload )
    # ser.write(  ( str(payload) ).encode() )
    
    if (feed_id == "bbc-led" and ser):
        print("Writing to Yolobit....")
        ser.write(  ( str(payload) ).encode() )

    
    if (feed_id == "door" and str(payload) == "2" ):
        time.sleep(5)
        client.publish("door", 3)

    


#readSerial from Microbit --> processData --> publish to Adafruit
#Get message from Adafruit --> ser.write to Microbit



###################################################################################
######################    Send from Microbit to Gateway   #########################


# Read from Microbit

#Function about Reading process
def processData ( data ) :
    data = data.replace ("!", "")
    data = data.replace ("#", "")
    splitData = data.split(":")
    print ( splitData )
    if splitData[1] == "TEMP":
        client.publish("bbc-temp", splitData[2])


mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


###################################################################################






# Connect to Ada

client = MQTTClient ( AIO_USERNAME , AIO_KEY )
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background ()





# API
# Open door
# Close door


def FaceReg_In(ID):
    try:
        client.publish (str(ID), 1)
    except:
        print('Stranger detected !!!!\n')
    else:
        client.publish("bbc-led", 1)
        client.publish("door", 2)

        print ("Check In:", ID ,"\n")
    

def FaceReg_Out(ID, count):
    try:
        client.publish (str(ID), 0)
    except:
        print('Stranger detected !!!!\n')
    else:
        
        if (count == 0):
            client.publish("bbc-led", 0)

        client.publish("door", 2)
        print ("Check Out:", ID ,"\n")
    
    
def Register(ID):
    try:
        client.publish (str(ID), 0)
    except:
        print ("Register from Adafruit ERROR !!!: ", ID,"\n" )
        pass
    else:
        print ("Register from Adafruit successfully: ", ID ,"\n")


def stranger(data):
    client.publish("alert",5)
    client.publish("image", data)
    print("Alert from Adafruit...\n")
    
    


def ConnectAdafruit():
    client = MQTTClient ( AIO_USERNAME , AIO_KEY )
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_background ()


# while True:
#     time.sleep(3)
#     data = cv2.imread("ElonMusk1.jpg")
#     print(len(data))
