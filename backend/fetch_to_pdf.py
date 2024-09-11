import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import os
from tqdm import tqdm

#Storing in pdfs so that we do not need to build a new model which takes in text


# Function to fetch and process webpage content
def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.text

        # Use BeautifulSoup to parse HTML
        soup = BeautifulSoup(data, 'html.parser')

        # Remove unwanted elements
        for script in soup(['script', 'style', 'link']):
            script.decompose()

        # Initialize text and table data
        text = ''
        table_data = []

        # print(soup)

        # Extract text content from common elements and span tags recursively
        def extract_text_from_element(element):
            nonlocal text
            if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
                if element.name in ['h1', 'h2']:
                    text += "**" + element.get_text() + "**\n"
                elif element.name in ['li']:
                    text += "- " + element.get_text().strip() + "\n"
                else:
                    text += element.get_text() + "\n"
            for child in element.children:
                if child.name:
                    extract_text_from_element(child)

        # Traverse the document and extract text
        extract_text_from_element(soup)
        return text
        # return text, table_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None


# Function to write content to PDF
def write_to_pdf(text, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)


    # Add text content
    for line in text.split('\n'):
        if line.strip() != '':
            pdf.multi_cell(0, 10, line)
        pdf.ln()  # Add a line break after each line of text

    pdf.output(filename)


# Main function to read URLs from data.txt and process each one
def main():
    override_file = True
    if not os.path.exists('data_doc'):
        os.makedirs('data_doc')

    if not os.path.exists('data_doc/data5.txt'):
        print("data5.txt file not found.")
        return

    with open('data_doc/data5.txt', 'r') as file:
        urls = file.readlines()

    for url in tqdm(urls, desc="Processing URLs", unit="url"):
        url = url.strip().split('#')[0]
        filename = f"data_doc/{url.split('/')[-1].replace('/', '_')}.pdf"
        if os.path.exists(filename) and not override_file:
            print(f"PDF already exists: {filename}")
            continue
        if url:
            text = fetch_content(url)
            if text:
                write_to_pdf(text, filename)
                print(f"Created PDF: {filename}")


if __name__ == "__main__":
    main()
