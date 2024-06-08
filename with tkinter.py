import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import socket
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


# hello

from PIL import Image, ImageTk


def get_domain(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        domain = None
    return domain


def process_csv(input_file):
    df = pd.read_csv(input_file)

    if 'DESTIP' not in df.columns:
        raise ValueError("The input CSV file must have a column named 'DESTIP'")

    num_cores = os.cpu_count()
    num_threads = max(num_cores // 2, 1)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_index = {executor.submit(process_ip, ip): i for i, ip in enumerate(df['DESTIP'])}
        results = []

        for future in as_completed(future_to_index):
            index = future_to_index[future]
            domain = future.result()
            results.append((index, domain))

    results.sort(key=lambda x: x[0])
    sorted_domains = [domain for _, domain in results]

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f'C:/Users/Simar/Downloads/ip_to_domain_{timestamp}.csv'

    df['domain_name'] = sorted_domains
    df.to_csv(output_file, index=False)

    return output_file


def process_ip(ip):
    domain = get_domain(ip)
    if domain is None:
        domain = "None"
    return domain


def browse_file():
    browse_button.config(bg='blue', fg='white')
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        filename_label.config(text=f"Selected file: {os.path.basename(file_path)}")
        filename_label.update_idletasks()  # Update the label immediately
        #output_file = process_csv(file_path)
        #result_label.config(text=f"Translated IP addresses to domain names and saved to {output_file}")
        #root.after(3000, root.quit)

        process_and_save(file_path)

def process_and_save(input_file):
    output_file = process_csv(input_file)
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        os.rename(output_file, save_path)  # Move the output file to the selected location
        result_label.config(text=f"Translated IP addresses to domain names and saved to {save_path}")
        root.after(3000, root.quit)
    else:
        os.remove(output_file)  # Delete the output file if the user cancels the save dialog

def revert_button_color():
    browse_button.config(bg='black', fg='white')

# Create the main Tkinter window
root = tk.Tk()
root.geometry('500x500')
root.title("IP TO DNS CONVERTER")


bg_image = Image.open("police logo.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)



# Create a canvas and display the background image
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")



# Create and pack the GUI elements
browse_button = tk.Button(root, text="Browse CSV File", command=browse_file, font=("Arial", 14), padx=20, pady=10, bg='black', fg='white')
browse_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

filename_label = tk.Label(root, text="", wraplength=300)
filename_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

result_label = tk.Label(root, text="")
result_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)


browse_button.bind('<Button-1>', lambda event: root.after(200, revert_button_color))

# Run the Tkinter event loop
root.mainloop()
