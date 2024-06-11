import pandas as pd
import socket
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Function to get domain name from IP address
def get_domain(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        domain = None
    return domain

# Read the CSV file with IP addresses
input_file = "C:/Users/Simar/Downloads/GPCSSI-TEST.csv"
df = pd.read_csv(input_file)

# Ensure the CSV has a column named 'DESTIP'
if 'DESTIP' not in df.columns:
    raise ValueError("The input CSV file must have a column named 'DESTIP'")

# Calculate the number of threads to use
num_cores = os.cpu_count()
num_threads = max(num_cores // 2, 1)  # Use half of the available CPU cores, but at least 1 thread

# Function to process each IP address and get the domain name
def process_ip(ip):
    domain = get_domain(ip)
    if domain is None:
        domain = "None"
    return domain

# Use ThreadPoolExecutor to handle multithreading
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit tasks for each IP address, and record their original order
    future_to_index = {executor.submit(process_ip, ip): i for i, ip in enumerate(df['DESTIP'])}
    results = []

    # Collect results as they become available
    for future in as_completed(future_to_index):
        index = future_to_index[future]
        domain = future.result()
        results.append((index, domain))

# Sort the results based on their original order
results.sort(key=lambda x: x[0])

# Extract domains from the sorted results
sorted_domains = [domain for _, domain in results]

# Update the DataFrame with the sorted domains
df['domain_name'] = sorted_domains

# Save the results to a new CSV file

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file = f'C:/Users/Simar/Downloads/ip_to_domain_{timestamp}.csv'
#output_file = 'C:/Users/Simar/Downloads/ip_to_domain.csv'  # Replace with your desired output file path
df.to_csv(output_file, index=False)

print(f"Translated IP addresses to domain names and saved to {output_file}")
