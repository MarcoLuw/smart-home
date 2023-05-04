import gradio as gr
import numpy as np
import GateWayMain as gw
import mongodb as db
import AI
import cv2
import random

def checkin(im,ID):
    
    ## Client --> AI --> DB --> Gateway --> Done


    ## Detect with AI first

    name = "./cache/" + str(ID) + "_" + "111111" + ".jpg"
    image_input = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
    cv2.imwrite(name, image_input)

    face_path = AI.Verification(name)

    if face_path == "None" or  face_path == "Error":
        greeting = 'Stranger detected !!!!'
        return im, greeting


    ## parse ID of face detected and compare with input ID 

    face_parse = face_path.replace("./member_image/","")
    face_parse = face_parse.split('_')

    userID = face_parse[1]
    username = face_parse[0]

    if userID == ID:
        # check in DATABASE if user outdoor
        status = db.checkin(ID_input=userID, name_input=username)
        if status == 0:
            # Update to MQTT
            gw.FaceReg_In(ID)
            greeting =  f"Welcome back, {username} !!!"
        else:
            greeting =  f"You are already in, {username} !\nMaybe, You want to check-out....??"
        
    else:
        greeting = 'Wrong ID, please try again !!!!'


    return im, greeting



def checkout(im,ID):
    #ID = 16122002
    
    # detect with  __AI__  first

    name = "./cache/" + str(ID) + "_" + "111111" + ".jpg"
    image_input = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
    cv2.imwrite(name, image_input)

    face_path = AI.Verification(name)

    if face_path == "None" or face_path == "Error":
        greeting = 'Stranger detected !!!!'
        return im, greeting

    face_parse = face_path.replace("./member_image/","")
    face_parse = face_parse.split('_')

    userID = face_parse[1]
    username = face_parse[0]


    ## Check in DB
    if userID == ID:
        status,count = db.checkout(ID_input=userID, name_input=username)

        if status == 0:

            ## Update to MQTT
            gw.FaceReg_Out(ID, count)
            greeting =  f"See you soon, {username} !!!"
        else:
            greeting =  f"You are already out, {username} !\nMaybe, You want to check-in....??"

    else:
        greeting = 'Wrong ID, please try again !!!!'

    return im, greeting



def regis(imageinput, name_input, ID_input):
    
    Info = db.getInfo(ID_input)

    #name = "./cache/" +str(name_input) +"_"+ str(ID_input) + "_" + "000000" + ".jpg"
    image_input = cv2.cvtColor(imageinput,cv2.COLOR_RGB2BGR)

    if Info is None:
        name = "./member_image/" +str(name_input) +"_"+ str(ID_input) + "_" + "000000" + ".jpg"
        cv2.imwrite(name, image_input)

        AI.register(name_input= name_input,ID=ID_input)

        greeting = f'Register Successfully !!!!\nWelcome {name_input}!!!'
        
        gw.Register(ID_input)               ## Create feed named by ID
        db.addMember(name, name_input, ID_input)   ## Create log member

        return imageinput , greeting
    
    else:

        greeting =  f"Sorry, This ID [{ID_input}] already exists !!!\nThe image will be added to improve verification !!!"
        id = random.randint(0,999999)
        name = "./member_image/" +str(name_input) +"_"+ str(ID_input) + "_" + str(id) + ".jpg"
        cv2.imwrite(name, image_input)
        AI.register(name_input= name_input,ID=ID_input)

        return imageinput, greeting



def clear():
    return None, None,None,None


# toggle_demo = 1
# def demo(image_input):
#     if toggle_demo == 1:
#         toggle_demo = 0
#         image_input.source = "upload"
#     else:
#         toggle_demo = 1
#         image_input.source = "webcam"

    


with gr.Blocks(css=".input_image { max-width: 800; max-height: none; }") as demo:
    with gr.Tab("Demo Recognition: "):
        with gr.Row():
            with gr.Column():
                #img_in = gr.Image(source="webcam", streaming=True)
                img_in = gr.Image(source="upload")
                text = gr.Text(placeholder="ID here")
                with gr.Row():
                    Checkin_btn = gr.Button("Check in").style(css="background-color: yellow")
                    Checkout_btn = gr.Button("Check out").style(css="background-color: blue")
                    
            with gr.Column():
                imgout = gr.Image()
                textout = gr.Text()
        
        #demo_button = gr.Button("DEMO").style(css="background-color: orange")

    Checkin_btn.click(checkin, inputs = [img_in,text], outputs=[imgout,textout])
    Checkout_btn.click(checkout, inputs = [img_in,text], outputs=[imgout,textout])


    with gr.Tab("Register: "):
            with gr.Row():
                with gr.Column():
                    #image_input = gr.Image(source="webcam", streaming=True)
                    image_input = gr.Image(source="upload")
                    name_input = gr.Text(label="Name:")
                    ID_input = gr.Text(label="ID:")
                with gr.Column():
                    img_out = gr.Image()
                    text_out = gr.Text()

            with gr.Row():
                reg_button = gr.Button("SUBMIT").style(css="background-color: green")
                clear_button = gr.Button("CLEAR")
                #demo_button = gr.Button("DEMO").style(css="background-color: orange")

    
    reg_button.click(regis, inputs= [image_input, name_input, ID_input], outputs= [img_out,text_out])
    clear_button.click(clear, inputs= None , outputs= [name_input, ID_input, img_out, text_out])
    #demo_button.click(demo, inputs= image_input, outputs= None)

demo.launch()

