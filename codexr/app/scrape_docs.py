import requests
from bs4 import BeautifulSoup
import os

# Define the documentation sources with corrected, more stable URLs
DOCS_URLS = [
    # Unity Documentation Hubs (more stable)
    "https://docs.unity3d.com/Manual/index.html",
    "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest/manual/index.html",
    "https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest/manual/index.html",
    "https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/manual/index.html",
    
    # Unreal Engine Documentation (might require a different user-agent or method if 403 persists)
    "https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-reality-development",
    
    # Other reliable sources
    "https://developer.apple.com/documentation/ARKit/occluding-virtual-content-with-people",
    "https://developers.google.com/ar/develop/unity/depth/developer-guide",
]

# Define a directory to save the cleaned text files
CLEAN_DOCS_DIR = "clean_docs"
os.makedirs(CLEAN_DOCS_DIR, exist_ok=True)

def fetch_html(url):
    """Fetches the HTML content from a given URL with a common user agent."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Successfully fetched {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_clean_text(html_content, url):
    """
    Parses HTML and extracts clean text, ignoring code blocks, headers, and footers.
    This logic is tailored to the structure of the provided docs.
    """
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove common irrelevant HTML elements
    for element in soup(["header", "nav", "footer", "aside", "script", "style"]):
        element.decompose()
    
    # This is a specific tag that holds the main content in some of the doc sites
    main_content = soup.find("main")
    if not main_content:
        main_content = soup.find("article")

    # If a specific content area is found, process only that
    if main_content:
        # Get all text and join it
        text = main_content.get_text(separator="\n", strip=True)
    else:
        # Fallback to getting all text
        text = soup.get_text(separator="\n", strip=True)

    # Clean up multiple newlines and extra spaces
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def main():
    """Main function to run the scraping process."""
    print("Starting documentation scraping...")
    for i, url in enumerate(DOCS_URLS):
        html_content = fetch_html(url)
        if html_content:
            clean_text = extract_clean_text(html_content, url)
            
            # Save the clean text to a file
            filename = os.path.join(CLEAN_DOCS_DIR, f"doc_{i}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(clean_text)
            print(f"Saved clean text to {filename}")

if __name__ == "__main__":
    main()