import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from tkinter import simpledialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize variables
        self.user_input = None
        self.geometry("400x400")  # Set the initial size of the window
        self.label = None  # Initialize the label variable
        self.title("Watermark Maker")  # Set the window title
        self.create_widget()  # Call the method to create widgets

    def create_widget(self):
        # Create buttons
        self.file_btn()
        self.quit_btn()
        self.wtm_text_btn()
        self.wtm_same_photo_btn()

    def quit_btn(self):
        # Create a Quit button
        self.button = tk.Button(text="Quit", command=self.quit)
        self.button.place(x=80, y=160)  # Set the position of the button

    def file_btn(self):
        # Create a button to select a file
        self.button = tk.Button(text="Search File", command=self.open_file_name)
        self.button.place(x=80, y=50)  # Set the position of the button

    def wtm_text_btn(self):
        # Create a button to add text as a watermark
        self.button = tk.Button(text="Add Text as WaterMarker", command=self.wtm_text)
        self.button.place(x=80, y=130)  # Set the position of the button

    def wtm_same_photo_btn(self):
        # Create a button to add the same photo as a watermark
        self.button = tk.Button(text="Add Same photo as WaterMarker", command=self.wtm_same_img)
        self.button.place(x=80, y=90)  # Set the position of the button

    def open_file_name(self):
        # Open a file dialog to select a file
        self.file_name = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                    filetypes=(("jpeg", "*.jpg"), ("png", "*.png")))
        if self.label is not None:
            self.label.destroy()  # Destroy the label if it exists
        self.label = tk.Label(text="Image Upload")
        self.label.grid(sticky=tk.N)
        self.label.configure(text=f"Selected: \n"  # Update the label with the selected file
                                  f" {self.file_name}")

    def wtm_text(self):
        # Add text as a watermark
        self.user_input = simpledialog.askstring("Watermark Text", "Type the text:")  # Ask user for input
        image = self.file_name
        image = Image.open(image)  # Open the image

        watermark_image = image.copy()  # Create a copy of the image
        draw = ImageDraw.Draw(watermark_image)  # Create an ImageDraw object

        font = ImageFont.truetype("arial.ttf", 100)  # Load a font and set the size

        draw.text((0, 0), self.user_input, (255, 255, 255), font=font)  # Draw text on the image

        self.save_image(watermark_image)  # Save the image

    def wtm_same_img(self):
        # Add the same photo as a watermark
        image = self.file_name
        image = Image.open(image)  # Open the image
        im2 = image
        im1 = image.convert('L')  # Convert the image to grayscale

        threshold = 50
        im1 = im1.point(lambda x: 255 if x > threshold else 0)  # Thresholding
        im1 = im1.resize((im1.width // 2, im1.height // 2))  # Resize the image
        im1 = im1.filter(ImageFilter.CONTOUR)  # Apply a filter
        im1 = im1.point(lambda x: 0 if x == 255 else 255)  # Thresholding

        im2.paste(im1, ((im2.width - im1.width) // 2, (im2.height - im1.height) // 2), im1)  # Paste the image

        self.save_image(im2)  # Save the image

    def save_image(self, image):
        try:
            image.save(f"{self.file_name.split('.')[0]}-watermarked-image.jpeg")  # Save the image
            label_text = "Image Upload: " + self.file_name
        except OSError:
            return print("Could not find file path")
        if self.label is not None:
            self.label.destroy()  # Destroy the label if it exists

        self.label = tk.Label(text="Image Upload")
        self.label.grid(sticky=tk.N)
        self.label.configure(text=f"SAVED: \n"  # Update the label
                                  f" {self.file_name}")


# Create the application instance and run it
app = App()
app.mainloop()
