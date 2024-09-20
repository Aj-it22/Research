import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from tkinter import Tk, Label, Button, filedialog, Frame
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import time
import threading
import matplotlib.pyplot as plt

# Function to convert PE file to an image
def convert_pe_to_image(pe_file, output_path):
    with open(pe_file, 'rb') as f:
        file_content = f.read()

    padding_size = (512 - len(file_content) % 512) % 512
    padded_content = file_content + bytearray(padding_size)
    padded_content_list = list(padded_content)

    while int(np.sqrt(len(padded_content_list))) * int(np.sqrt(len(padded_content_list))) != len(padded_content_list):
        padded_content_list.append(0)

    img_array = np.array(padded_content_list, dtype=np.uint8).reshape((int(np.sqrt(len(padded_content_list))), int(np.sqrt(len(padded_content_list)))))
    image_file_path = os.path.join(output_path, os.path.basename(pe_file) + '.png')
    plt.imsave(image_file_path, img_array, cmap='gray')
    plt.close()
    
    return image_file_path

# Function to preprocess the image for the model
def preprocess_external_image(img_path, target_size=(64, 64)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

# Function to perform the prediction and update the GUI
def predict_image():
    # Open file dialog to select the PE file
    pe_file = filedialog.askopenfilename(title="Select PE File")
    
    if pe_file:
        output_path = r"D:\Research-Final\Output"
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Start the progress bar
        progress_bar.start()
        
        # Run the prediction in a separate thread
        threading.Thread(target=run_prediction, args=(pe_file, output_path)).start()

def run_prediction(pe_file, output_path):
    # Record the start time
    start_time = time.time()
    
    # Generate the image from the PE file
    image_path = convert_pe_to_image(pe_file, output_path)
    
    # Preprocess the generated image
    processed_img = preprocess_external_image(image_path)
    
    # Perform prediction on the generated image
    prediction = model.predict(processed_img)
    
    # Record the end time
    end_time = time.time()
    
    # Calculate the total time taken
    total_time = end_time - start_time
    
    # Decode the prediction
    class_indices = {'1': 'benign', '0': 'malware'}
    predicted_class = np.argmax(prediction)
    predicted_class_name = class_indices[str(predicted_class)]
    
    # Load and display the image in the GUI
    img = Image.open(image_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    
    # Update the GUI elements in the main thread
    root.after(0, update_gui, img, predicted_class_name, total_time)

def update_gui(img, predicted_class_name, total_time):
    img_label.config(image=img)
    img_label.image = img
    result_label.config(text=f"Predicted Class: {predicted_class_name}\nTime taken: {total_time:.2f} seconds", fg="white", bg="#5D6D7E")
    progress_bar.stop()

# Load your saved model
model = tf.keras.models.load_model(r'D:\Research-Final\Output.keras')

# Create the main application window
root = Tk()
root.title("PE File Classification")
root.geometry("600x450")
root.configure(bg="#34495E")

# Create a frame for layout management
frame = Frame(root, bg="#34495E")
frame.pack(pady=20)

# Create a label for the title
title_label = Label(frame, text="PE File Classification", font=("Helvetica", 24, "bold"), bg="#34495E", fg="white")
title_label.pack()

# Create a label to display the image
img_label = Label(frame, bg="#34495E")
img_label.pack(pady=20)

# Create a label to display the prediction result
result_label = Label(frame, text="Prediction Result", font=("Helvetica", 16), bg="#5D6D7E", fg="white", width=40, height=2)
result_label.pack(pady=10)

# Create a button to upload the file and perform the prediction
upload_button = Button(frame, text="Upload and Predict", command=predict_image, font=("Helvetica", 14), bg="#1ABC9C", fg="white", padx=20, pady=10)
upload_button.pack(pady=10)

# Add a progress bar
progress_bar = Progressbar(root, orient='horizontal', mode='indeterminate', length=400)
progress_bar.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
