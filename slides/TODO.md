## Testing

* [ ] Eingabe-Validierung **--Arne**
* [ ] Test-Stategie ("Testplan") **--Arne**
* [ ] Tooling (für Django) **--Arne**
* [x] Deployment **--Arne**

## App-Improvements **--Finn**

1. Teilen mit Patienten
2. Dokumente "bearbeiten" (update)
3. Benutzer-Profile mit pers. Daten (Geburtstag, Geschlecht, etc.)
4. Account-Verwaltung (Passwort-Reset, Löschen, Mail-Verifizierung, etc.)
5. (*CASCADING* für *AccessRequests* prüfen)

## Security-Features

* [x] Prüfen von zusammengesetzen Encryption-Keys (für *Documents*)

    **In Doku**: Im Projektumfang nicht verhältnismäßig, allerdings im Produktivbetrieb notwendig da medizinische Daten

* [ ] DB-Backups (automatisiert, verschlüsselt) **--Irina**
* [ ] Upload-Scanning (Viren, etc.) **--Irina**

    <https://github.com/QueraTeam/django-clamav>

# Doku

## Sicherheit

* Session-Länge
* Passwort-Hashing
* DB-Backups
* Upload-Scanning
* Dokument-Verschlüsselung
* ...
