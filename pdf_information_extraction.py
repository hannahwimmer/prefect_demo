import os
import csv
from glob import glob
from PyPDF2 import PdfReader
from datetime import datetime

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
OUTPUT_DIR = "data/output"

def extract_pdf_form_data(pdf_path):
    reader = PdfReader(pdf_path)
    fields = {}

    if reader.get_fields():
        for key, value in reader.get_fields().items():
            fields[key] = value.get('/V', '')  # Get value or empty string
    else:
        print(f"No form fields found in {pdf_path}")

    return fields

def get_timestamped_filename(prefix="extracted", ext=".csv"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}{ext}"

def process_pdfs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pdf_files = glob(os.path.join(RAW_DIR, "*.pdf"))

    if not pdf_files:
        print("No new PDFs found in data/raw/.")
        return

    output_file = os.path.join(OUTPUT_DIR, get_timestamped_filename())

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = None

        for pdf in pdf_files:
            print(f"Processing {pdf}...")
            data = extract_pdf_form_data(pdf)

            if not data:
                continue

            if writer is None:
                writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                writer.writeheader()

            writer.writerow(data)

            # Move PDF to processed folder
            basename = os.path.basename(pdf)
            os.rename(pdf, os.path.join(PROCESSED_DIR, basename))

    print(f"\n✅ Extraction complete. Saved to: {output_file}")

if __name__ == "__main__":
    process_pdfs()
