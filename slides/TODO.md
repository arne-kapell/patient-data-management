## Testing
1. Eingabe-Validierung **--Arne**
2. Test-Stategie ("Testplan") **--Arne**
3. Tooling (für Django) **--Arne**

## App-Improvements **--Finn**
1. Teilen mit Patienten
2. Dokumente "bearbeiten" (update)
3. Benutzer-Profile mit pers. Daten (Geburtstag, Geschlecht, etc.)
4. Account-Verwaltung (Passwort-Reset, Löschen, Mail-Verifizierung, etc.)
5. (*CASCADING* für *AccessRequests* prüfen)

## Security-Features
1. Prüfen von zusammengesetzen Encryption-Keys (für *Documents*)

    **In Doku**: Im Projektumfang nicht verhältnismäßig, allerdings im Produktivbetrieb notwendig da medizinische Daten

2. DB-Backups (automatisiert, verschlüsselt) **--Irina**
3. Upload-Scanning (Viren, etc.) **--Irina**


# Doku
## Sicherheit
- Session-Länge
- Passwort-Hashing
- DB-Backups
- Upload-Scanning
- Dokument-Verschlüsselung
- ...