import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageTk
from tkinter import simpledialog

from PIL.ImageTk import PhotoImage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize variables

        self.user_input = None
        # self.geometry("800x400")  # Set the initial size of the window

        self.label = None  # Initialize the label variable
        self.title("Watermark Maker")  # Set the window title
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.create_widget()  # Call the method to create widgets

    def create_widget(self):
        # Create buttons
        self.file_btn()
        self.quit_btn()
        self.wtm_text_btn()
        self.wtm_same_photo_btn()
        self.show_photo_btn()


    def file_btn(self):
        # Create a button to select a file
        self.button = tk.Button(text="Search File", command=self.open_file_name)
        self.button.grid(column=0, row=0,sticky="w",padx=10, pady=5)  # Set the position of the button

    def wtm_same_photo_btn(self):
        # Create a button to add the same photo as a watermark
        self.button = tk.Button(text="Add Same photo as WaterMarker", command=self.wtm_same_img)
        self.button.grid(column=0, row=1,sticky="w",padx=10, pady=5)  # Set the position of the button

    def wtm_text_btn(self):
        # Create a button to add text as a watermark
        self.button = tk.Button(text="Add Text as WaterMarker", command=self.wtm_text)
        self.button.grid(column=0, row=2, sticky="w", padx=10, pady=5)  # Set the position of the button

    def show_photo_btn(self):

        self.button = tk.Button(text="Show Photo", command=self.show_photo)
        self.button.grid(column=0, row=3,sticky="w",padx=10, pady=5)




    def quit_btn(self):
        # Create a Quit button
        self.button = tk.Button(text="Quit", command=self.quit)
        self.button.grid(column=0, row=4,sticky="w",padx=10, pady=5)  # Set the position of the button

    def show_photo(self):
        if self.file_name:
            self.canvas.delete("all")

            image =  ImageTk.PhotoImage(Image.open(self.file_name))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.config(width=image.width(), height=image.height())
            self.canvas.grid(column=1,row=2, rowspan=10)
            self.canvas.image = image

    def open_file_name(self):
        # Open a file dialog to select a file
        self.file_name = filedialog.askopenfilename(initialdir="/", title="Select A File")
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
        # Open the image file and convert it to RGBA mode (with alpha channel)
        image = Image.open(self.file_name).convert("RGBA")

        # Set the opacity level (from 0 to 255)
        opacity_level = int(80)

        # Open the watermark image file and convert it to RGBA mode
        watermark = Image.open(self.file_name).convert("RGBA")

        # Resize the watermark image to half of the size of the main image
        watermark = watermark.resize((image.width // 2, image.height // 2))

        # Extract the alpha channel from the watermark image
        alpha = watermark.getchannel('A')

        # Apply the opacity level to the alpha channel
        new_alpha = alpha.point(lambda i: opacity_level if i > 0 else 0)

        # Apply the modified alpha channel back to the watermark image
        watermark.putalpha(new_alpha)

        # Calculate the position to paste the watermark onto the main image
        position = ((image.width - watermark.width) // 2, (image.height - watermark.height) // 2)

        # Paste the watermark onto the main image
        image.paste(watermark, position, watermark)

        # Save the modified image
        self.save_image(image)

    def save_image(self, image):
        try:
            image = image.convert("RGB")
            image.save(f"{self.file_name.split('.')[0]}-watermarked-image.jpeg")  # Save the image
            label_text = "Image Upload: " + self.file_name
        except OSError as er:
            return print(er)
        if self.label is not None:
            self.label.destroy()  # Destroy the label if it exists

        self.label = tk.Label(text="Image Upload")
        self.label.grid(sticky=tk.N)
        self.label.configure(text=f"SAVED: \n"  # Update the label
                                  f" {self.file_name}")


# Create the application instance and run it
app = App()
app.mainloop()
