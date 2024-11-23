import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json

def select_image():
    """Open a file dialog to select an image."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        label_selected.config(text=f"Selected: {file_path}")
        send_image_to_server(file_path)

def send_image_to_server(file_path):
    """Send the selected image to the local server."""
    url = "http://127.0.0.1:8000/predict/"  # Update to the provided endpoint
    try:
        with open(file_path, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            # Process the server response
            result = response.json()  # Assuming the server response is JSON
            if "results" in result and isinstance(result["results"], list):
                parsed_result = parse_results(result["results"])
                messagebox.showinfo("Prediction Result", parsed_result)
            else:
                messagebox.showerror("Error", "Unexpected response format")
        else:
            messagebox.showerror("Error", f"Server Error: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to the server.\n{e}")

def parse_results(results):
    """Parse the results list to a readable string format."""
    output = "Predictions:\n"
    for item in results:
        for label, confidence in item.items():
            output += f"{label}: {confidence * 100:.2f}%\n"
    return output

# Create the main tkinter window
root = tk.Tk()
root.title("Image Prediction Uploader")

# Create and place widgets
btn_select = tk.Button(root, text="Select Image", command=select_image)
btn_select.pack(pady=10)

label_selected = tk.Label(root, text="No image selected")
label_selected.pack(pady=5)

# Run the tkinter event loop
root.mainloop()
