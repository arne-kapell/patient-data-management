## Testing

* [x] Eingabe-Validierung **--Arne**
* [ ] Test-Stategie ("Testplan") **--Irina**
* [x] Tooling (für Django) **--Arne**
* [x] Deployment **--Arne**

## App-Improvements **--Finn**

* [ ] Teilen mit Patienten
* [ ] Dokumente "bearbeiten" (update)
* [-] Benutzer-Profile mit pers. Daten (Geburtstag, Geschlecht, etc.)
* [-] Account-Verwaltung (Passwort-Reset, Löschen, Mail-Verifizierung, etc.)
* [ ] (*CASCADING* für *AccessRequests* prüfen)

## Security-Features

* [x] Prüfen von zusammengesetzen Encryption-Keys (für *Documents*)

    **In Doku**: Im Projektumfang nicht verhältnismäßig, allerdings im Produktivbetrieb notwendig da medizinische Daten

* [x] DB-Backups (automatisiert, verschlüsselt) **--Irina**
* [-] Upload-Scanning (Viren, etc.) **--Irina**

    <https://github.com/QueraTeam/django-clamav>

# Doku

## Sicherheit

* Session-Länge
* Passwort-Hashing
* DB-Backups
* Upload-Scanning
* Dokument-Verschlüsselung
* ...
