# ETC-CSV-to-CAPTURE

"""
🎯 Zweck:
Konvertiert einen ETC EOS Patch-CSV-Export in ein Capture-kompatibles Fixture-Format.

📥 Eingabe:
- CSV-Datei (latin1-kodiert)
- Erste Zeile ignorieren (START_CHANNELS)
- Kopfzeile ab Zeile 2
- Relevante Spalten:
    - CHANNEL, FIXTURE_TYPE, MANUFACTURER, ADDRESS
    - LOCATION_X, LOCATION_Y, LOCATION_Z

📤 Ausgabe:
Neue CSV-Datei mit folgendem Format für Capture:
[
 "Fixture", "Optics", "Wattage", "Unit", "Circuit", "Channel", "Groups", "Patch",
 "DMX Mode", "DMX Channels", "Position X", "Position Y", "Position Z",
 "Focus Pan", "Focus Tilt", "Invert Pan", "Pan Start Limit", "Pan End Limit",
 "Invert Tilt", "Tilt Start Limit", "Tilt End Limit", "Identifier", "External Identifier"
]

🔄 Konvertierungslogik:
- "Fixture" = MANUFACTURER + " " + FIXTURE_TYPE
- "Patch" = ADDRESS als Dezimal (z. B. "1/276" → "1.276")
- "Channel" = CHANNEL
- "Position X/Y/Z" = LOCATION_X/Y/Z + "m" (z. B. -5.00 → "-5.00m")
- "Identifier" = zufällig generierte UUID
- Standardwerte für alle übrigen Felder:
    - "Optics" = "N/A", "Wattage" = "N/A"
    - "DMX Mode" = "Standard", "DMX Channels" = 1
    - "Focus Pan", "Focus Tilt" = "0°"
    - "Invert Pan", "Invert Tilt" = "No"
    - "Pan/Tilt Start/End Limit" = "0°"
    - "External Identifier" = "N/A"

💾 Ausgabe-Dateiname: capture_patch_export.csv
"""

## Nutzung

Alle CSV-Dateien im Ordner `convert-cvs` lassen sich gesammelt mit
`convert_csvs.py` konvertieren:

```bash
python3 convert_csvs.py
```

Die erzeugten Dateien werden im Ordner `converted-csvs` abgelegt.
Der Dateiname richtet sich nach der Eingabedatei und endet auf
`_capture_patch_export.csv`.
