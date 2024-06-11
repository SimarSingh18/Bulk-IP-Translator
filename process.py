from tkinter import filedialog, ttk
import pandas as pd
import socket
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


class Process:

    @staticmethod
    # Function to process a single IP address and return its corresponding domain name
    def process_ip(ip):
        try:
            domain = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            domain = "None"
        return domain


    @staticmethod
    # Function to process the CSV file, converting IPs to domain names, and saving the result
    def process_csv(input_file):

        df = pd.read_csv(input_file)


        # Check if the DataFrame has only one column and no header
        if len(df.columns) == 1 and df.columns[0] == 0:
            ip_column = df.columns[0]
        # Check if the DataFrame has one column with a specific name ('DESTIP')
        elif len(df.columns) == 1 and df.columns[0] == 'DESTIP':
            ip_column = 'DESTIP'
        # Check if the DataFrame has a 'DESTIP' column
        elif 'DESTIP' in df.columns:
            ip_column = 'DESTIP'
        else:
            raise ValueError("The input CSV file must have a column named 'DESTIP'")

        num_cores = os.cpu_count() # determine number of CPU cores available
        num_threads = max(num_cores // 2, 1) # calculate number of threads to use (half of the available CPU cores)

        # Process IP addresses concurrently using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=num_threads) as executor:

            # Map IP processing tasks to threads and store them in a dictionary
            # key: value pair (domain: index)
            future_to_index = {executor.submit(Process.process_ip, ip): i for i, ip in enumerate(df[ip_column])}
            results = []

            # iterating through completed tasks
            for future in as_completed(future_to_index):
                index = future_to_index[future]  # Retrieve the index associated with the completed task
                domain = future.result()  # Get the domain name returned by the task
                results.append((index, domain))


        results.sort(key=lambda x: x[0]) # Sort the results based on the original index
        sorted_domains = [domain for _, domain in results] # Extract the sorted domain names
        df['domain_name'] = sorted_domains # Add a new column to the DataFrame with the sorted domain names

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S") # Generate a timestamp for the output file name
        output_file = f'ip_to_domain_{timestamp}.csv' # Construct the output file name
        df.to_csv(output_file, index=False) # Save the DataFrame to a CSV file without including the index

        return output_file