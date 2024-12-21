import os
import requests
from tqdm import tqdm
from colorama import Fore, Style, init
from urllib.parse import urlparse

init()  # Initialize colorama for Windows

# User-Agent and custom headers definition
headers = {
    'Accept': '*/*',
    'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://recu.me',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

# Function to get the file size
def get_file_size(url):
    response = requests.head(url, headers=headers)
    size = int(response.headers.get('content-length', 0))
    return size

# Function to download a chunk of the file
def download_chunk(url, start, end, save_path):
    chunk_headers = headers.copy()
    chunk_headers['Range'] = f'bytes={start}-{end}'
    response = requests.get(url, headers=chunk_headers, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

# Main download function with progress bar
def download_file_with_progress(url, download_folder):
    # Extract the original file name from the URL
    file_name = os.path.basename(urlparse(url).path)
    save_path = os.path.join(download_folder, file_name)  # Save with the original file name in 'downloads'
    
    # Check if the file already exists
    if os.path.exists(save_path):
        print(f"{Fore.YELLOW}File already exists, skipping download:{Style.RESET_ALL} {file_name}")
        return  # Skip download if file exists
    
    file_size = get_file_size(url)
    print(f"{Fore.CYAN}Total file size to download:{Style.RESET_ALL} {file_size / (1024 * 1024):.2f} MB")

    # Download the entire file in one request with a progress bar
    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Downloading", ncols=100, colour='green') as pbar:
        response = requests.get(url, headers=headers, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                pbar.update(len(chunk))
    
    print(f"{Fore.GREEN}Download completed successfully!{Style.RESET_ALL}")

# Function to read URLs from a file and download each one sequentially
def download_from_file(file_path, download_folder):
    with open(file_path, 'r') as f:
        links = f.readlines()
    
    # Create the 'downloads' folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Download each link from the file sequentially
    for link in links:
        download_file_with_progress(link.strip(), download_folder)

# Main execution
file_path = "links_log.txt"  # Path to your links file
download_folder = "downloads"  # Folder where files will be saved
download_from_file(file_path, download_folder)
