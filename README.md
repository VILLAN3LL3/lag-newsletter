# Anleitung

Folgende Steps müssen nacheinander ausgeführt werden, um die E-Mails zu generieren:

1. Kopiere die `_sensitive_data.json` Datei im `input` Ordner und benenne sie um in `sensitive_data.json`. Ersetze die Beispieldaten mit den echten Daten für deine LAG. Die mit "zoom" beginnenden Daten müssen nur für die Zoomsession-Mail angepasst werden.

3. Anschließend das Python-Script `mailgenerierung.py` ausführen. Dort wählt man aus, ob man eine E-Mail mit reiner Sitzungsankündigung oder mit Zoom-Einwahldaten erstellen will.

4. Das generierte HTML wird im `output` Ordner gespeichert und kann nun verwendet werden, um die E-Mail an die Liste zu verschicken.