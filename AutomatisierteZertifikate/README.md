# 🧾 Zertifikatsgenerator – Digitale Hermeneutik

Dieses Programm erzeugt automatisiert Teilnahmezertifikate für Workshops der Digitalen Hermeneutik.
Es wird lokal mit einer grafischen Oberfläche ausgeführt und verarbeitet Teilnehmerlisten im CSV-Format.

## 🔧 Voraussetzungen

- **Python 3.9+**
- Installation notwendiger Bibliotheken:
  ```bash
  pip install Pillow
  ```

## 🚀 Start des Programms

Starte das Programm mit:

```bash
python Main.py
```

## 🖼️ Funktionen

- Generierung von PDF-Zertifikaten auf Basis einer Teilnehmerliste
- Anpassbare Workshopdaten (Titel, Inhalte, Datum, Sprache)
- Integration eines grafischen Templates
- Unterstützung von Signaturbildern
- Deutsch/Englisch auswählbar
- Speicherung & Laden von Eingaben via JSON

## 📋 Anwendungsschritte

1. **Grundeinstellungen:** Semester, Präfix, Datum, Sprache wählen
2. **Signaturbild laden (optional)**
3. **CSV-Teilnehmerliste importieren**
4. **Zielordner zum Speichern wählen**
5. **Workshopbeschreibung eintragen (Titel, max. 10 Inhalte)**
6. **Schriftgröße anpassen (optional)**
7. **Einstellungen speichern/laden**
8. **Zertifikate generieren**

## ⚠️ Typische Fehlermeldungen

- *Filepräfix entspricht nicht dem erwarteten Muster*  
  → Beispiel: `20241124_XML`

- *Teilnehmerliste hat mehr als eine Spalte*  
  → Nur eine Spalte mit Namen zulässig

- *Zeitformat ungültig*  
  → Format: `YYYY-MM-DD`

- *Keine Sprache gewählt*  
  → Auswahl erforderlich

## 📂 Projektstruktur

| Datei/Ordner                | Beschreibung                             |
|----------------------------|------------------------------------------|
| `Main.py`                  | Startpunkt mit GUI                       |
| `input_checker.py`         | Prüft Eingaben, Formate & Dateiinhalte  |
| `CertGUI.py`               | GUI-Logik                                |
| `Media/`                   | Layout-Bild (`WKT_Certificate-01.png`)  |
| `Data/`                    | Sprachvorlagen (`de_text.json`, `en_text.json`) |
| `unterschrift.png`         | Optionale Signaturdatei                  |

## 📝 Lizenz

Dieses Projekt wurde von mir erstellt und darf gerne **nicht-kommerziell genutzt, verändert und erweitert** werden.  
Eine kommerzielle Nutzung oder Weiterverbreitung ist **nur nach vorheriger Rücksprache** gestattet.  
Bitte bei Weiterverwendung den ursprünglichen Urheber nennen.
