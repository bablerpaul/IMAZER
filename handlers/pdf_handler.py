import os
import re
import json
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from tkinter import Tk, filedialog
from typing import Dict, List, Optional

class PDF_Handler:
    def __init__(self, pdf_path: str = None):
        self.pdf_path = pdf_path
        self.metadata: Dict[str, str] = {}
        self.geolocations: List[Dict[str, float]] = []
        self.content_analysis: Dict = {}
        self.errors: List[str] = []
        self.raw_text: str = ''

    @staticmethod
    def select_pdf_file() -> Optional[str]:
        Tk().withdraw()
        while True:
            file_path = filedialog.askopenfilename(
                title="Select PDF File",
                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
            )
            if not file_path:
                return None
            if os.path.isfile(file_path):
                return file_path
            print("Invalid file selection. Please try again.")

    def _decode_metadata_value(self, value) -> str:
        try:
            return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else str(value)
        except Exception as e:
            return f"[Decode Error: {str(e)}]"

    def _extract_metadata(self) -> None:
        try:
            with open(self.pdf_path, 'rb') as file:
                parser = PDFParser(file)
                document = PDFDocument(parser)
                if document.info:
                    self.metadata = {
                        self._decode_metadata_key(key): self._decode_metadata_value(value)
                        for key, value in document.info[0].items()
                    }
                self.metadata.update({
                    'PDF Version': str(document.pdf_version),
                    'XMP Metadata': bool(document.xmpmetadata),
                    'Encrypted': document.is_encrypted,
                    'Page Count': str(len(list(document.get_pages())))
                })
        except Exception as e:
            self.errors.append(f"Metadata extraction failed: {str(e)}")

    def _decode_metadata_key(self, key) -> str:
        key_map = {
            'Title': ['/Title', 'title'],
            'Author': ['/Author', 'author'],
            'Subject': ['/Subject', 'subject'],
            'Keywords': ['/Keywords', 'keywords'],
            'Creator': ['/Creator', 'creator'],
            'Producer': ['/Producer', 'producer'],
            'CreationDate': ['/CreationDate', 'creationdate'],
            'ModDate': ['/ModDate', 'moddate']
        }
        str_key = self._decode_metadata_value(key)
        for pretty_name, variants in key_map.items():
            if any(variant in str_key.lower() for variant in variants):
                return pretty_name
        return str_key

    def _extract_geolocations(self) -> None:
        if not self.raw_text:
            return
        patterns = [
            (
                r'(\d+\.?\d*)°?\s*([NS])\W+(\d+\.?\d*)°?\s*([EW])',
                lambda m: (
                    float(m[0]) * (-1 if m[1].upper() == 'S' else 1),
                    float(m[2]) * (-1 if m[3].upper() == 'W' else 1)
                )
            ),
            (
                r'(-?\d+\.\d+)[°]?[\s,;]+(-?\d+\.\d+)°?',
                lambda m: (float(m[0]), float(m[1]))
            ),
            (
                r'(\d+)°\s*(\d+)\'\s*(\d+)"\s*([NS])\W+(\d+)°\s*(\d+)\'\s*(\d+)"\s*([EW])',
                lambda m: (
                    (int(m[0]) + int(m[1]) / 60 + int(m[2]) / 3600) * (-1 if m[3].upper() == 'S' else 1),
                    (int(m[4]) + int(m[5]) / 60 + int(m[6]) / 3600) * (-1 if m[7].upper() == 'W' else 1)
                )
            )
        ]
        locations = []
        for pattern, converter in patterns:
            matches = re.finditer(pattern, self.raw_text, re.IGNORECASE)
            for match in matches:
                try:
                    lat, lon = converter(match.groups())
                    locations.append({
                        'latitude': round(lat, 6),
                        'longitude': round(lon, 6),
                        'raw_match': match.group(0)
                    })
                except Exception:
                    continue
        self.geolocations = locations

    def _analyze_content(self) -> None:
        self.content_analysis = {
            'character_count': len(self.raw_text),
            'word_count': len(self.raw_text.split()),
            'line_count': len(self.raw_text.split('\n')),
            'has_geodata': bool(self.geolocations)
        }
        self.content_analysis.update({
            'contains_table': bool(re.search(r'\b(table|figure|chart)\b', self.raw_text, re.I)),
            'contains_email': bool(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.raw_text)),
            'contains_phone': bool(re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', self.raw_text)),
            'contains_url': bool(re.findall(r'https?://\S+', self.raw_text))
        })

    def analyze(self) -> None:
        if not self.pdf_path or not os.path.isfile(self.pdf_path):
            self.errors.append("Invalid PDF file path")
            return
        try:
            self._extract_metadata()
            try:
                self.raw_text = extract_text(self.pdf_path)
            except PDFTextExtractionNotAllowed:
                self.errors.append("Text extraction not allowed by PDF permissions")
                return
            self._extract_geolocations()
            self._analyze_content()
        except Exception as e:
            self.errors.append(f'Analysis failed: {str(e)}')

    def print_results(self) -> None:
        print("\n=== Metadata ===")
        print(json.dumps(self.metadata, indent=4))
        if self.geolocations:
            print("\n=== Geolocations Found ===")
            for loc in self.geolocations:
                print(f"Coordinates: {loc['latitude']}, {loc['longitude']}")
                print(f"Raw Match: {loc['raw_match']}\n")
        print("\n=== Content Analysis ===")
        print(json.dumps(self.content_analysis, indent=4))
        if self.errors:
            print("\n=== Errors ===")
            print("\n".join(self.errors))
