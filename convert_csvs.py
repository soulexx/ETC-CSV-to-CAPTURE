import csv
import os
import uuid
from pathlib import Path

INPUT_DIR = Path('convert-cvs')
OUTPUT_DIR = Path('converted-csvs')

OUTPUT_HEADER = [
    'Fixture', 'Optics', 'Wattage', 'Unit', 'Circuit', 'Channel', 'Groups',
    'Patch', 'DMX Mode', 'DMX Channels', 'Position X', 'Position Y', 'Position Z',
    'Focus Pan', 'Focus Tilt', 'Invert Pan', 'Pan Start Limit', 'Pan End Limit',
    'Invert Tilt', 'Tilt Start Limit', 'Tilt End Limit', 'Identifier',
    'External Identifier'
]

def convert_file(path, out_path):
    with open(path, encoding='latin1', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip START_CHANNELS
        header = next(reader)
        indices = {name: i for i, name in enumerate(header)}
        rows = list(reader)

    with open(out_path, 'w', encoding='latin1', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(OUTPUT_HEADER)

        for row in rows:
            if not row:
                continue

            tag = row[0]
            if tag in ('END_CHANNELS', 'START_FIXTURES'):
                break

            def safe(index):
                return row[indices[index]].strip() if index in indices and row[indices[index]] else ''

            fixture = f"{safe('MANUFACTURER')} {safe('FIXTURE_TYPE')}".strip()
            address = safe('ADDRESS').replace('/', '.')
            channel = safe('CHANNEL')

            pos_x = f"{safe('LOCATION_X')}m"
            pos_y = f"{safe('LOCATION_Z')}m"  # Tiefe
            pos_z = f"{safe('LOCATION_Y')}m"  # Höhe

            identifier = str(uuid.uuid4())

            out_row = [
                fixture,
                'N/A',  # Optics
                'N/A',  # Wattage
                '',     # Unit
                '',     # Circuit
                channel,
                '',     # Groups
                address,
                'Standard',  # DMX Mode
                1,           # DMX Channels
                pos_x,
                pos_y,
                pos_z,
                '0°',  # Focus Pan
                '0°',  # Focus Tilt
                'No',    # Invert Pan
                '0°',  # Pan Start Limit
                '0°',  # Pan End Limit
                'No',    # Invert Tilt
                '0°',  # Tilt Start Limit
                '0°',  # Tilt End Limit
                identifier,
                'N/A'   # External Identifier
            ]

            writer.writerow(out_row)

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for csv_file in INPUT_DIR.glob('*.csv'):
        out_name = f"{csv_file.stem}_capture_patch_export.csv"
        out_file = OUTPUT_DIR / out_name
        convert_file(csv_file, out_file)

if __name__ == '__main__':
    main()
