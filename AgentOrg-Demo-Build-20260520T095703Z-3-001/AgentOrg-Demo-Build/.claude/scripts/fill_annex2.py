"""
Fill QSD app form-E-Annex 2 standard mode ODT with Millipore SOP data.
Maps each ISO 13485 clause to Procedure number and Version.
"""
import zipfile, shutil, os, re
from xml.etree import ElementTree as ET

SRC = r'C:\D\MRS client-2014\MRS\AI training\Claude-QSD\QSD app form-E-Annex 2 standard mode.odt'
DST = r'C:\Users\USER\Desktop\QSD50750 Millipore-amendment-2026\QSD-output\QSD50750_Annex2_filled.odt'

# -------------------------------------------------------------------
# Mapping: ISO clause keyword → (procedure_number, version)
# -------------------------------------------------------------------
FILL = {
    '4.1':    ('00005007POL; 00080958MP', '31.0; 5.0'),
    '4.2.1':  ('000107MP; 20119650', '35.0; 42'),
    '4.2.2':  ('QM', '56.0'),
    '4.2.3':  ('SOP R&D 03', '42.0'),
    '4.2.4':  ('000107MP; 20119650', '35.0; 42'),
    '4.2.5':  ('000107MP; 20119650', '35.0; 42'),
    '5.1':    ('00005042POL', '9.0'),
    '5.2':    ('20185800; 20278615', '13.0; 6.0'),
    '5.3':    ('00005042POL', '9.0'),
    '5.4.1':  ('00005042POL', '9.0'),
    '5.4.2':  ('052009MP; 20255032', '34.0; 19.0'),
    '5.5.1':  ('20773295 (pending)', 'N/A'),
    '5.5.2':  ('QM', '56.0'),
    '5.5.3':  ('QM', '56.0'),
    '5.6.1':  ('SOP QA 13', '39.0'),
    '5.6.2':  ('SOP QA 13', '39.0'),
    '5.6.3':  ('SOP QA 13; 20346694', '39.0; 7.0'),
    '6.1':    ('QM', '56.0'),
    '6.2':    ('(pending supplement)', 'N/A'),
    '6.3':    ('POL MAINT 01', '8.0'),
    '6.4.1':  ('SOP MICRO 23', '87.0'),
    '6.4.2':  ('SOP MICRO 23', '87.0'),
    '7.1':    ('00080958MP; SOP REG 05; 00005007POL', '5.0; 28.0; 31.0'),
    '7.2.1':  ('SOP R&D 03', '42.0'),
    '7.2.2':  ('SOP R&D 03', '42.0'),
    '7.2.3':  ('20185800; 20278615; 000116MP', '13.0; 6.0; 29.0'),
    '7.3.1':  ('SOP R&D 03', '42.0'),
    '7.3.2':  ('SOP R&D 03', '42.0'),
    '7.3.3':  ('SOP R&D 03', '42.0'),
    '7.3.4':  ('SOP R&D 03', '42.0'),
    '7.3.5':  ('SOP R&D 03', '42.0'),
    '7.3.6':  ('SOP R&D 03', '42.0'),
    '7.3.7':  ('SOP R&D 03; 00005007POL', '42.0; 31.0'),
    '7.3.8':  ('SOP R&D 03', '42.0'),
    '7.3.9':  ('SOP R&D 03; 052009MP; 20255032', '42.0; 34.0; 19.0'),
    '7.3.10': ('SOP R&D 03', '42.0'),
    '7.4.1':  ('SOP PUR 01; SOP PUR 03', '45.0; 39.0'),
    '7.4.2':  ('SOP PUR 03', '39.0'),
    '7.4.3':  ('SOP QA 44; SOP PRO0 05', '28.0; 39.0'),
    '7.5.1':  ('SOP RECO 02', '61.0'),
    '7.5.2':  ('SOP MICRO 23', '87.0'),
    '7.5.3':  ('N/A', 'N/A'),
    '7.5.4':  ('N/A', 'N/A'),
    '7.5.5':  ('N/A', 'N/A'),
    '7.5.6':  ('00005007POL', '31.0'),
    '7.5.7':  ('N/A', 'N/A'),
    '7.5.8':  ('SOP RECO 02', '61.0'),
    '7.5.9.1':('SOP RECO 02', '61.0'),
    '7.5.9.2':('N/A', 'N/A'),
    '7.5.10': ('20136246', '24.0'),
    '7.5.11': ('(pending supplement)', 'N/A'),
    '7.6':    ('POL MAINT 01', '8.0'),
    '8.1':    ('QM', '56.0'),
    '8.2.1':  ('20185800; 20278615', '13.0; 6.0'),
    '8.2.2':  ('20185800', '13.0'),
    '8.2.3':  ('000116MP', '29.0'),
    '8.2.4':  ('SOP QA 02', '48.0'),
    '8.2.5':  ('SOP QA 33', '53.0'),
    '8.2.6':  ('SOP QA 44', '28.0'),
    '8.3.1':  ('SOP QA 33', '53.0'),
    '8.3.2':  ('SOP QA 33', '53.0'),
    '8.3.3':  ('000116MP; 20185800', '29.0; 13.0'),
    '8.3.4':  ('SOP QA 33', '53.0'),
    '8.4':    ('SOP QA 13; 20346694', '39.0; 7.0'),
    '8.5.1':  ('052009MP; 20255032', '34.0; 19.0'),
    '8.5.2':  ('SOP QA 33', '53.0'),
    '8.5.3':  ('SOP QA 33', '53.0'),
}

NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}

def get_cell_text(cell):
    """Extract all text from a table cell."""
    parts = []
    for p in cell.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
        t = ''.join(p.itertext())
        if t.strip():
            parts.append(t.strip())
    return ' '.join(parts)

def set_cell_text(cell, text, style=None):
    """Replace all text in a table cell with the given text."""
    text_ns = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
    # Remove existing paragraphs
    for p in list(cell.findall(f'{{{text_ns}}}p')):
        cell.remove(p)
    # Add new paragraph
    p = ET.SubElement(cell, f'{{{text_ns}}}p')
    if style:
        p.set(f'{{urn:oasis:names:tc:opendocument:xmlns:text:1.0}}style-name', style)
    p.text = text

def find_clause_key(cell_text):
    """Find matching FILL key from cell text containing ISO clause."""
    # Try longest match first (e.g. 7.5.9.1 before 7.5.9)
    for key in sorted(FILL.keys(), key=len, reverse=True):
        if key in cell_text:
            return key
    return None

def main():
    shutil.copy2(SRC, DST)

    # Read all files from ODT zip
    with zipfile.ZipFile(SRC, 'r') as zin:
        names = zin.namelist()
        files = {}
        for name in names:
            files[name] = zin.read(name)

    # Parse content.xml
    xml_bytes = files['content.xml']
    root = ET.fromstring(xml_bytes)

    table_ns = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
    text_ns  = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

    filled = 0
    # Find all table rows
    for row in root.iter(f'{{{table_ns}}}table-row'):
        cells = list(row.findall(f'{{{table_ns}}}table-cell'))
        if len(cells) < 3:
            continue

        # Collect text from all cells to find the ISO clause
        row_texts = [get_cell_text(c) for c in cells]
        full_row = ' '.join(row_texts)

        clause_key = find_clause_key(full_row)
        if not clause_key:
            continue

        proc_num, version = FILL[clause_key]

        # The blank cells are the last two (Procedure number, Version)
        # Find cells that are empty
        empty_cells = [i for i, c in enumerate(cells) if not get_cell_text(c).strip()]

        if len(empty_cells) >= 2:
            set_cell_text(cells[empty_cells[-2]], proc_num)
            set_cell_text(cells[empty_cells[-1]], version)
            filled += 1
            print(f'  Filled {clause_key}: {proc_num} | {version}')
        elif len(empty_cells) == 1:
            # Only one empty — fill as procedure number
            set_cell_text(cells[empty_cells[0]], proc_num)
            filled += 1
            print(f'  Filled {clause_key} (1 cell): {proc_num}')

    print(f'\nTotal rows filled: {filled}')

    # Write back
    files['content.xml'] = ET.tostring(root, encoding='utf-8', xml_declaration=True)

    with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            zout.writestr(name, files[name])

    print(f'Saved to: {DST}')

if __name__ == '__main__':
    main()
