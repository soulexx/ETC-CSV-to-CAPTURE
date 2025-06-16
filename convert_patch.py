import csv
import uuid
import re

INPUT_FILE = 'patch_klein.csv'
OUTPUT_FILE = 'capture_patch_export.csv'

OUTPUT_HEADER = [
    "Fixture", "Optics", "Wattage", "Unit", "Circuit", "Channel", "Groups", "Patch",
    "DMX Mode", "DMX Channels", "Position X", "Position Y", "Position Z",
    "Focus Pan", "Focus Tilt", "Invert Pan", "Pan Start Limit", "Pan End Limit",
    "Invert Tilt", "Tilt Start Limit", "Tilt End Limit", "Identifier", "External Identifier"
]

ADDRESS_RE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$")


def convert():
    with open(INPUT_FILE, encoding='latin1', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip START_CHANNELS
        header = next(reader)
        indices = {name: idx for idx, name in enumerate(header)}

        rows = list(reader)

    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(OUTPUT_HEADER)

        for row in rows:
            if not row:
                continue
            tag = row[0]
            if tag in ('END_CHANNELS', 'START_FIXTURES'):
                break

            address_field = row[indices['ADDRESS']]
            m = ADDRESS_RE.match(address_field)
            if not m:
                continue
            patch = f"{m.group(1)}.{m.group(2)}"

            fixture = f"{row[indices['MANUFACTURER']].strip()} {row[indices['FIXTURE_TYPE']].strip()}".strip()
            channel = row[indices['CHANNEL']].strip()
            pos_x = f"{row[indices['LOCATION_X']]}m"
            pos_y = f"{row[indices['LOCATION_Z']]}m"
            pos_z = f"{row[indices['LOCATION_Y']]}m"
            identifier = str(uuid.uuid4())

            out_row = [
                fixture,
                'N/A',     # Optics
                'N/A',     # Wattage
                '',        # Unit
                '',        # Circuit
                channel,
                '',        # Groups
                patch,
                'Standard',  # DMX Mode
                1,           # DMX Channels
                pos_x,
                pos_y,
                pos_z,
                '0°',     # Focus Pan
                '0°',     # Focus Tilt
                'No',     # Invert Pan
                '0°',     # Pan Start Limit
                '0°',     # Pan End Limit
                'No',     # Invert Tilt
                '0°',     # Tilt Start Limit
                '0°',     # Tilt End Limit
                identifier,
                'N/A'      # External Identifier
            ]
            writer.writerow(out_row)

if __name__ == '__main__':
    convert()
