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

### Einzelne Datei konvertieren

Um speziell eine Datei `patch_klein.csv` im aktuellen Verzeichnis zu
konvertieren, steht das Skript `convert_patch.py` bereit:

```bash
python3 convert_patch.py
```

Das Ergebnis wird als `capture_patch_export.csv` im selben Ordner
abgelegt.

## Automatische Konvertierung mit GitHub Actions

Dieser Repo enthält ein Workflow unter `.github/workflows/convert_csv.yml`. Der Workflow läuft bei jedem Push oder Pull Request und führt `convert_csvs.py` aus. Die erzeugten Dateien im Ordner `converted-csvs` werden anschließend als Artefakt hochgeladen und können im Action-Log heruntergeladen werden.

### Aktivierung
1. Repository auf GitHub hochladen.
2. Unter "Actions" den Workflow "Convert CSV to Capture" aktivieren.
3. Bei jedem neuen Commit (z.B. durch Codex) startet die Konvertierung automatisch.
4. Nach Abschluss des Workflows lässt sich das Artefakt `converted-csvs` herunterladen.
