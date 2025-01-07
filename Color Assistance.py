import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import threading

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Flag to control the video capture loop
video_running = False

# Function to recognize the color from the BGR format
def detect_color(bgr):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    hue = hsv[0]  # Extract the hue value (0-179 range)
    sat = hsv[1]  # Saturation
    val = hsv[2]  # Value (brightness)

    # Define color ranges in HSV format (hue ranges from 0 to 179)
    colors = {
        "Red": ((0, 120, 70), (10, 255, 255)),
        "Orange": ((10, 120, 70), (25, 255, 255)),
        "Yellow": ((25, 120, 70), (35, 255, 255)),
        "Green": ((35, 120, 70), (85, 255, 255)),
        "Blue": ((85, 120, 70), (170, 255, 255)),
        "Purple": ((170, 120, 70), (179, 255, 255)),
        "Pink": ((145, 120, 70), (170, 255, 255)),
        "Brown": ((10, 100, 20), (20, 255, 200)),
        "Gray": ((0, 0, 40), (180, 20, 180)),
        "White": ((0, 0, 200), (180, 30, 255))
    }

    # Check the hue value against the color ranges
    for color_name, (lower, upper) in colors.items():
        lower = np.array(lower)
        upper = np.array(upper)

        # Use the hue value to match against the defined color ranges
        if lower[0] <= hue <= upper[0] and lower[1] <= sat <= upper[1] and lower[2] <= val <= upper[2]:
            return color_name

    # Add the RGB logic for detecting rainbow colors
    r, g, b = bgr  # Extract RGB values (BGR is the input format)
    
    if r > g and r > b:
        return "Red"
    elif g > r and g > b:
        return "Green"
    elif b > r and b > g:
        return "Blue"

    return "Unknown"


# Function to convert OpenCV image to Tkinter format
def cv_to_tk(cv_image):
    color_coverted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(color_coverted)
    return ImageTk.PhotoImage(image)

# Function to capture video and detect colors
def capture_video():
    global video_running
    cap = cv2.VideoCapture(0)

    while video_running:
        ret, frame = cap.read()
        if not ret:
            break

        # Get the dimensions of the frame
        height, width, _ = frame.shape
        
        # Define the center of the frame
        center_x, center_y = width // 2, height // 2
        
        # Define the size of the area to highlight (frame dimensions)
        frame_size = 100  # You can adjust this to your desired size
        top_left = (center_x - frame_size // 2, center_y - frame_size // 2)
        bottom_right = (center_x + frame_size // 2, center_y + frame_size // 2)

        # Draw a rectangle (frame) around the center of the frame
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)  # Green frame

        # Get the color from the center of the frame
        center_pixel = frame[center_y, center_x]

        # Detect color
        detected_color = detect_color(center_pixel)

        # Show detected color
        engine.say(f"Detected color is {detected_color}")
        engine.runAndWait()

        # Display the video with the color label
        cv2.putText(frame, detected_color, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Color Blindness Assistant", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to start video capture in a separate thread
def start_video():
    global video_running
    video_running = True
    video_thread = threading.Thread(target=capture_video)
    video_thread.start()

# Function to stop the video capture
def stop_video():
    global video_running
    video_running = False

# GUI to start and stop the video capture
def start_gui():
    root = tk.Tk()
    root.title("Color Blindness Assistant")

    # Button to start the video capture
    start_button = tk.Button(root, text="Start", command=start_video, font=('Helvetica', 14))
    start_button.pack(pady=20)

    # Button to stop the video capture
    stop_button = tk.Button(root, text="Stop", command=stop_video, font=('Helvetica', 14))
    stop_button.pack(pady=20)

    # Display message in the GUI
    label = tk.Label(root, text="Press 'Start' to begin color detection", font=('Helvetica', 14))
    label.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    start_gui()
 