# Sankey Generator

## Infos

Der Generator wurde nur mit Finanzguru csv dateien getestet

## Einführung

Der Sankey Generator ist eine Anwendung zur Erstellung von Sankey-Diagrammen basierend auf CSV-Daten. Diese Anleitung hilft dir, die Anwendung zu installieren und zu verwenden.

## Voraussetzungen

-   Python 3.8 oder höher
-   Poetry (ein Paket- und Abhängigkeitsmanager für Python)

## Installation

### Schritt 1: Python installieren

Stelle sicher, dass Python 3.8 oder höher auf deinem System installiert ist. Du kannst Python von der offiziellen [Python-Website](https://www.python.org/downloads/) herunterladen und installieren.

### Schritt 2: Poetry installieren

Um Poetry zu installieren, öffne ein Terminal und führe Sie den folgenden Befehl aus:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### Schritt 3: Projekt herunterladen

Falls git installiert ist:

```
git clone https://github.com/Phil5888/sankey_generator.git
cd sankey_generator_pyqt
```

ansonsten code manuell herunterladen

https://github.com/Phil5888/sankey_generator

### Schritt 4: Abhängigkeiten installieren

Im Projektverzeichnis führe den folgenden Befehl aus, um alle Abhängigkeiten zu installieren:

```
poetry install
```

### Schritt 5: Virtuelle Umgebung aktivieren

Aktiviere die virtuelle Umgebung mit dem folgenden Befehl:

```
poetry shell
```

## Konfigurationsdatei

Die Anwendung verwendet eine Konfigurationsdatei (config.json), um verschiedene Einstellungen zu laden.

1. Die Datei "config.json.example" umbennen in "config.json"
2. Die Datei "config.json" öffnen und folgende Werte anpassen

### Pfad zur csv datei

Pfad zu deiner CSV datei. Im Beispiel gibt es im projektordner den Ordner "input_files" in dem die Datei "input.csv" liegt.

```
"input_file": "input_files/input.csv",
```

### income_reference_accounts

Eine Liste von IBANs. Hier werden die accounts für die einkommensberechnung hinterlegt. Ersetze zum die beispiel IBANs mit deinem Girokonto (für gehalt usw.) und deinem Depot (für zinsen usw.).
Bei bedarf kann auch nur eine IBAN angegeben werden.

```
"Income iban 1",
"Income iban 2"
```

### income_sources

Hier werden die Einkommensquellen beschrieben

-   label: Text der im Sankey verwendet wird
-   column: Spalte auf die gefiltert wird
-   values: Hier können unterschiedliche filter eingetragen werden. Zum Beispiel dein Arbeitgeber oder "lohn" oder "gehalt"

```
{
"label": "Gehalt",
"column": "Beguenstigter/Auftraggeber",
"values": [
"Your employer"
]
},
```

### income_data_frame_filters

Eine Liste von IBANs. Hier am besten nochmal die IBANs von oben eintragen. Ggf. wird das später verwendet um Umbuchungen zu erkennen. Falls es keine spalte dafür gibt.
Nur die IBANs ändern, den rest nicht.

```
"Income iban 1",
"Income iban 2"
```

### Standard werte für die eingabefelder

Die folgenden Werte können angepasst werden um den inhalt der Eingabefelder beim start der Anwendung zu befüllen.
Info: Später sollen die werte auch automatisch gespeichert werden.

```
"last_used_month": 8,
"last_used_year": 2024,
"last_used_issue_level": 1,
```

Passen Sie die Konfigurationsdatei nach Ihren Bedürfnissen an.

## Anwendung starten

Um die Anwendung zu starten, führen Sie den folgenden Befehl im Projektverzeichnis aus:

```
python src/main.py
```
