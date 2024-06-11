import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from process import Process
from datetime import datetime


class App(tk.Tk):


    def __init__(self):
        super().__init__()
        self.title("IP TO DNS CONVERTER")
        self.setup_ui()


    # Setup User Interface
    def setup_ui(self):
        self.setup_window()
        self.setup_buttons()
        self.setup_labels()
        self.setup_logo()


    # Setup Windows and Centering
    def setup_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")


    # Setup Buttons
    def setup_buttons(self):
        # invoking browse_file function
        self.browse_button = tk.Button(self, text="Browse CSV File", command=self.browse_file, font=("Calibri", 12), padx=20, pady=10, bg='black', fg='white')
        self.browse_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        
        #invoking revert button color function
        self.browse_button.bind('<Button-1>', lambda event: self.after(200, self.revert_button_color))


    # Setup Labels
    def setup_labels(self):
        # label 1
        self.filename_label = tk.Label(self, text="", wraplength=500, font=("Calibri", 12))
        self.filename_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        # label 2
        self.result_label = tk.Label(self, text="", wraplength=700, font=("Calibri", 12))
        self.result_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


    # Setup Logo
    def setup_logo(self):
        logo_image = Image.open("police_logo.jpg")
        logo_image = logo_image.resize((250, 200))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)


    # Browse for Input CSV File
    def browse_file(self):
        self.filename_label.config(text="")
        self.result_label.config(text="")

        # asking user for input file path
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        
        if file_path:

            # displaying selected file name
            self.filename_label.config(text=f"Selected file: {os.path.basename(file_path)}, translating...")
            self.update()
            
            # invoking process_csv function from process.py
            output_file = Process.process_csv(file_path)

            # invoking prompt_save_dialog function
            self.prompt_save_dialog(output_file)



    # Prompt User to save output file
    def prompt_save_dialog(self, output_file):

        save_folder = filedialog.askdirectory()
        if save_folder:
            output_path = os.path.join(save_folder, f"ip_to_domain_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
            os.rename(output_file, output_path)  # Move the output file to the selected location
            self.result_label.config(text=f"Translated IP addresses to domain names!\n\n Output saved to {output_path}")
        else:
            os.remove(output_file)  # Delete the output file if the user cancels the save dialog
            self.result_label.config(text="Translation completed but output file not saved", fg="red")



    # Revert color of button
    def revert_button_color(self):
        self.browse_button.config(bg='black', fg='white')



if __name__ == "__main__":
    app = App()
    app.mainloop()