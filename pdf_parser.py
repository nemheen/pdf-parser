# # necessary dependencies
# !apt-get install -y poppler-utils tesseract-ocr-jpn
# !apt-get install -y poppler-utils
# !pip install pdf2image pytesseract PyMuPDF

import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import argparse
import time
import re
import unicodedata

# Set the TESSDATA_PREFIX environment variable
os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"


def check_if_scanned(pdf_path):
    """
    Checks if a PDF is scanned by looking for text in the first page.
    Returns True if no text is found (scanned), False otherwise.
    """
    doc = fitz.open(pdf_path)
    first_page = doc[0]
    text = first_page.get_text("text")
    return len(text.strip()) == 0


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file. Handles both text-based and scanned PDFs.
    """
    text = ""
    doc = fitz.open(pdf_path)
    is_scanned = check_if_scanned(pdf_path)

    if is_scanned:
        #for scanned pdfs
        print(f"Processing scanned PDF: {pdf_path}")
        pages = convert_from_path(pdf_path, 300)
        for page_num, page in enumerate(pages, start=1):
            page_text = pytesseract.image_to_string(page, lang="jpn")
            print(f"Text from page {page_num} extracted.")
            print(page_text)
            print("-" * 80)  # Separator for readability
            text += f"\n--- Page {page_num} ---\n"
            text += page_text + "\n"
    else:
        # for text-based pdfs
        print(f"Processing text-based PDF: {pdf_path}")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text("text")
            print(f"Text from page {page_num + 1} extracted.")
            print(page_text)
            print("-" * 80)  # Separator for readability
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page_text + "\n"

    doc.close()
    return text

def save_output_to_file(text, output_file_path):
    """
    Saves the extracted text to a file with '_output.txt' appended to the base name.
    """
    try:
        base, _ = os.path.splitext(output_file_path)
        output_file_path = f"{base}_output.txt"

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(text)
            print(f"File saved successfully: {output_file_path}")
    except Exception as e:
        print(f"Error occurred while saving the file: {e}")

    return output_file_path



def main(input_pdf_path):
    """
    Main function to process the PDF and save extracted text.
    """
    if not os.path.exists(input_pdf_path):
        print(f"Error: File '{input_pdf_path}' does not exist.")
        return
    start_time = time.time()
    print(f"Processing PDF: {input_pdf_path}")
    text = extract_text_from_pdf(input_pdf_path)
    text = preprocess_text(text) #remove if deems unnecessary 
    save_output_to_file(text, input_pdf_path)

    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Processing time for {input_pdf_path}: {processing_time:.2f} seconds")



if __name__ == "__main__":

    main()

