
import streamlit as st
import cv2
import face_recognition as frg
import yaml 
from utils import recognize, build_dataset
import base64

st.set_page_config(layout="wide",page_title="Face Recognition App")
#Config
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("assets/back.jpg")
img1 = get_img_as_base64("assets/back.jpg")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/jpg;base64,{img}");
background-size: 200%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img1}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.sidebar.title("Settings")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#Create a menu bar
menu = ["Picture","Webcam"]
choice = st.sidebar.selectbox("Input type",menu)
#Put slide to adjust tolerance
TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.5,0.01)
st.sidebar.info("Tolerance is the threshold for face recognition. The lower the tolerance, the more strict the face recognition. The higher the tolerance, the more loose the face recognition.")

#Infomation section 
st.sidebar.title("Person Information")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()
name_container.info('Name: Unnknown')
id_container.success('ID: Unknown')
if choice == "Picture":
    st.title("Face Recognition App")
    st.write(PICTURE_PROMPT)
    uploaded_images = st.file_uploader("Upload",type=['jpg','png','jpeg'],accept_multiple_files=True)
    if len(uploaded_images) != 0:
        #Read uploaded image with face_recognition
        for image in uploaded_images:
            image = frg.load_image_file(image)
            image, name, id = recognize(image,TOLERANCE) 
            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            st.image(image)
    else: 
        st.info("Please upload an image")
    
elif choice == "Webcam":
    st.title("Face Recognition App")
    st.write(WEBCAM_PROMPT)
    #Camera Settings
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    FRAME_WINDOW = st.image([])
    
    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to capture frame from camera")
            st.info("Please turn off the other app that is using the camera and restart app")
            st.stop()
        image, name, id = recognize(frame,TOLERANCE)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #Display name and ID of the person
        
        name_container.info(f"Name: {name}")
        id_container.success(f"ID: {id}")
        FRAME_WINDOW.image(image)

with st.sidebar.form(key='my_form'):
    st.title("Developer Section")
    submit_button = st.form_submit_button(label='REBUILD DATASET')
    if submit_button:
        with st.spinner("Rebuilding dataset..."):
            build_dataset()
        st.success("Dataset has been reset")