import streamlit as st
from PIL import Image
import os

# Constants
UPLOAD_FOLDER = "uploads"
ADMIN_PASSWORD = "123456789"

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to display images with download and delete options
def display_images():
    image_files = os.listdir(UPLOAD_FOLDER)
    if not image_files:
        st.info("No images uploaded yet.")
    else:
        for image_file in image_files:
            image_path = os.path.join(UPLOAD_FOLDER, image_file)
            st.image(Image.open(image_path), caption=image_file)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="Download",
                    data=open(image_path, "rb").read(),
                    file_name=image_file,
                    mime="image/png"
                )
            if admin_mode:
                with col2:
                    if st.button(f"Delete {image_file}"):
                        os.remove(image_path)
                        st.success(f"{image_file} deleted.")
                        st.info("Please refresh the page to see the changes.")

# Streamlit App
st.title("Image Gallery")

# Toggle for Admin Mode
admin_mode = False
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

st.sidebar.header("Admin Login")
password = st.sidebar.text_input("Enter Admin Password", type="password")
if password == ADMIN_PASSWORD:
    st.sidebar.success("Admin mode activated!")
    st.session_state.admin_mode = True
    admin_mode = True
else:
    st.sidebar.warning("Incorrect Password. Viewing as User.")

# Admin Upload Section
if admin_mode:
    st.subheader("Admin Panel: Upload Images")
    uploaded_files = st.file_uploader(
        "Choose up to 10,000 images...", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    if uploaded_files:
        for uploaded_file in uploaded_files:
            save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} file(s) to /uploads")
        st.info("Please refresh the page to see the uploaded images.")

# Display Images for Download
st.subheader("Image Gallery")
display_images()
