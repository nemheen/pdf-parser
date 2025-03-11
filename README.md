# PDF Text Extraction Tool

## Overview
This Python script extracts text from PDF files, handling edge cases of scanned PDFs. For scanned PDFs, it uses OCR (Optical Character Recognition) via Tesseract to detect if pdf is image and skips it.

## Features
- Detects whether a PDF is scanned or text-based.
- Extracts text from text-based PDFs using PyMuPDF.
- Saves the extracted text to a file.

## Dependencies
Ensure you have the following installed:
- `poppler-utils`
- `tesseract-ocr-jpn`
- Python libraries: `pdf2image`, `pytesseract`, `PyMuPDF`

## Installation
```bash
apt-get install -y poppler-utils tesseract-ocr-jpn
pip install pdf2image pytesseract PyMuPDF
```

## Usage
Run the script with:
```bash
python script.py <path-to-pdf>
```

## Output
Extracted text is saved as `<pdf_filename>_output.txt` in the same directory.
