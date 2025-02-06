import os
import requests
import sys

def download_file(url, destination):
    """
    Download a file with simple progress printing
    """
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    print("Starting download...")
    try:
        # Download the file
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        # Open destination file
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # Print progress
                    percent = (downloaded_size / total_size) * 100
                    print(f"Downloaded: {downloaded_size}/{total_size} bytes ({percent:.1f}%)", end='\r')
        print("\nDownload complete!")
    except Exception as e:
        print(f"\nDownload failed: {str(e)}")
        raise

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    geval_dir = os.path.join(current_dir, 'src', 'geval')
    model_path = os.path.join(geval_dir, 'mistral-7b-instruct-v0.2.Q4_K_M.gguf')
    
    # Hugging Face model URL
    url = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

    print(f"Will download to: {model_path}")
    try:
        download_file(url, model_path)
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()