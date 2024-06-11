import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import socket
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from PIL import Image, ImageTk




# Function to get domain name from an IP address
def get_domain(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        domain = None
    return domain



# Function to process a single IP address to a domain name
def process_ip(ip):
    domain = get_domain(ip)
    if domain is None:
        domain = "None"
    return domain






# Function to process the CSV file, converting IPs to domain names, and saving the result
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


    # Prompt user for output file location
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    output_file = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=f"ip_to_domain_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    )

    root.destroy()

    df['domain_name'] = sorted_domains
    df.to_csv(output_file, index=False)

    return output_file






# Function to browse for a CSV file and initiate processing
def browse_file():
    
    browse_button.config(bg='blue', fg='white')
    
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        filename_label.config(text=f"Selected file: {os.path.basename(file_path)}")
        filename_label.update_idletasks()  # Update the label immediately
        process_and_save(file_path)






# Function to process the input file and save the output to a user-specified location
def process_and_save(input_file):
    
    output_file = process_csv(input_file)
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if save_path:
        os.rename(output_file, save_path)  # Move the output file to the selected location
        result_label.config(text=f"Translated IP addresses to domain names!\n Output saved to {save_path}")
        root.after(3000, root.quit)
    else:
        os.remove(output_file)  # Delete the output file if the user cancels the save dialog






# Function to revert the button color after being clicked
def revert_button_color():    
    browse_button.config(bg='black', fg='white')




# Create the main Tkinter window
root = tk.Tk()
root.geometry('500x500')
root.title("IP TO DNS CONVERTER")



# Calculate the center of the screen and set window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.5)
window_height = int(screen_height * 0.5)
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")



# Load and display the background image
bg_image = Image.open("police_logo.jpg").resize((window_width, window_height))
bg_image.putalpha(40)
bg_image_tk = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_image_tk, bg="white", bd=0)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)



# Create and pack the GUI elements
browse_button = tk.Button(root, text="Browse CSV File", command=browse_file, font=("Arial", 14), padx=20, pady=10, bg='black', fg='white')
browse_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

filename_label = tk.Label(root, text="", wraplength=300)
filename_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

result_label = tk.Label(root, text="")
result_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)


# Bind the revert button color function to the browse button
browse_button.bind('<Button-1>', lambda event: root.after(200, revert_button_color))


# Run the Tkinter event loop
root.mainloop()