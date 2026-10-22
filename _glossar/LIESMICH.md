# Glossar-Quelle (wird nicht veröffentlicht)

- `terms.py`: alle Begriffe (Begriff, Kategorie, Definition, Formel, verwandte Begriffe)
- `build.py`: erzeugt daraus `glossar.html`

Neuen Begriff ergänzen: Eintrag in `terms.py` hinzufügen, dann im Ordner `_glossar` ausführen: `python3 build.py`
(In `build.py` den Ausgabepfad ggf. auf `../glossar.html` anpassen.)

Regel: nur eigene Texte, keine fremden Definitionen übernehmen. Netstock nicht erwähnen.
