"""
convert_to_word.py — Script to convert all harvested markdown documents in data/
to Decree 30/2020/NĐ-CP administrative Word (.docx) files in data/word/.
"""

import sys
from pathlib import Path
from src.docx_converter import convert_all

def main():
    print("Starting Administrative DOCX Conversion per Decree 30/2020/NĐ-CP...")
    converted_files = convert_all(data_dir="data", output_dir="data/word")
    
    print(f"\nSuccessfully converted {len(converted_files)} markdown files into data/word/:")
    empty_files = []
    for filepath in converted_files:
        size = filepath.stat().st_size
        print(f" - {filepath} ({size} bytes)")
        if size == 0:
            empty_files.append(filepath)
            
    if empty_files:
        print(f"\nERROR: Found {len(empty_files)} empty .docx files!", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nVerification PASSED: All generated .docx files exist and are non-empty!")

if __name__ == "__main__":
    main()
