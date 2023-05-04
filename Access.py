import gradio as gr
import GateWayMain as gw
import mongodb as db
import AI
import cv2

gw.accessPort()

def checkin(im,ID):
    
    ## Client --> AI --> DB --> Gateway --> Done


    ## Detect with AI first

    face_path,data = AI.Verification(im=im, ID=ID)
    print(face_path)

    if face_path == "None" or  face_path == "Error":
        gw.stranger(data)
        greeting = 'Stranger detected !!!!'
        return im, greeting, None


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


    return im, greeting, None



def checkout(im,ID):
    #ID = 16122002
    
    # detect with  __AI__  first

    face_path, data = AI.Verification(im,ID)
    print(face_path)

    if face_path == "None" or face_path == "Error":
        gw.stranger(data)
        greeting = 'Stranger detected !!!!'
        return im, greeting, None

    face_parse = face_path.replace("./member_image/","")
    face_parse = face_parse.split('_')

    userID = face_parse[1]
    username = face_parse[0]


    ## Check out DB
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

    return im, greeting, None


def Alert(im):
    image = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
    data = AI.StrangerEncode(image)
    gw.stranger(data=data)
    return im, "Alert Successfully. Please wait a minute...!!!"



with gr.Blocks(theme='JohnSmith9982/small_and_pretty'  , css="#warning {background-color: red}") as demo:
    with gr.Tab("Demo Recognition: "):
        with gr.Row():
            with gr.Column():
                #img_in = gr.Image(source="webcam", streaming=True)
                img_in = gr.Image(source="upload")
                text = gr.Text(placeholder="ID here")
                with gr.Row():
                    Checkin_btn = gr.Button("Check in")
                    Checkout_btn = gr.Button("Check out")
                    Alert_btn = gr.Button(value="ALERT", elem_id="warning").style(full_width=200)

            with gr.Column():
                imgout = gr.Image().style(height=500)
                textout = gr.Text()
        
        #demo_button = gr.Button("DEMO").style(css="background-color: orange")

    Checkin_btn.click(checkin, inputs = [img_in,text], outputs=[imgout,textout,text])
    Checkout_btn.click(checkout, inputs = [img_in,text], outputs=[imgout,textout,text])
    Alert_btn.click(Alert, inputs = img_in,outputs=[imgout,textout])

    with gr.Tab("Recognition Streaming: "):
        with gr.Row():
            with gr.Column():
                img_in2 = gr.Image(source="webcam", streaming=True).style(height=500)
                text2 = gr.Text(placeholder="ID here")
                with gr.Row():
                    Checkin_btn2 = gr.Button("Check in")
                    Checkout_btn2 = gr.Button("Check out")
                    Alert_btn2 = gr.Button(value="ALERT", elem_id="warning").style(full_width=200)
                    
            with gr.Column():
                imgout2 = gr.Image().style(height=500)
                textout2 = gr.Text()
        
    Checkin_btn2.click(checkin, inputs = [img_in2,text2], outputs=[imgout2,textout2,text2])
    Checkout_btn2.click(checkout, inputs = [img_in2,text2], outputs=[imgout2,textout2,text2])
    Alert_btn2.click(Alert, inputs = img_in2, outputs=[imgout2,textout2])



 

if __name__ == '__main__':
    demo.launch(server_port=7800)
