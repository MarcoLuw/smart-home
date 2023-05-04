import gradio as gr
import GateWayMain as gw
import mongodb as db
import AI
import cv2
import random



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
    return None, None,None,None,None




with gr.Blocks(theme='finlaymacklon/boxy_violet@0.0.2') as demo:
    
    with gr.Tab("Register: "):
            with gr.Row():
                with gr.Column():
                    #image_input = gr.Image(source="webcam", streaming=True)
                    image_input = gr.Image(source="upload")
                    name_input = gr.Text(label="Name:")
                    ID_input = gr.Text(label="ID:")
                with gr.Column():
                    img_out = gr.Image().style(height=500)
                    text_out = gr.Text()

            with gr.Row():
                reg_button = gr.Button("SUBMIT")
                clear_button = gr.Button("CLEAR")
    
    reg_button.click(regis, inputs= [image_input, name_input, ID_input], outputs= [img_out,text_out])
    clear_button.click(clear, inputs= None , outputs= [image_input,name_input, ID_input, img_out, text_out])
    #demo_button.click(demo, inputs= image_input, outputs= None)    


    with gr.Tab("Register Stream: "):
            with gr.Row():
                with gr.Column():
                    image_input2 = gr.Image(source="webcam", streaming=True).style(height=500)
                    #image_input = gr.Image(source="upload")
                    name_input2 = gr.Text(label="Name:")
                    ID_input2 = gr.Text(label="ID:")
                with gr.Column():
                    img_out2 = gr.Image().style(height=500)
                    text_out2 = gr.Text()

            with gr.Row():
                reg_button2 = gr.Button("SUBMIT")
                clear_button2 = gr.Button("CLEAR")
                #demo_button = gr.Button("DEMO").style(css="background-color: orange")
                
    reg_button2.click(regis, inputs= [image_input2, name_input2, ID_input2], outputs= [img_out2,text_out2])
    clear_button2.click(clear, inputs= None , outputs= [image_input2,name_input2, ID_input2, img_out2, text_out2])

if __name__ == '__main__':
    demo.launch(server_port=7900, auth=("adminvippro", "1"), )

