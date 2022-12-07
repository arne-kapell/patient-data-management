[![Run tests and deploy to VPS](https://github.com/arne-kapell/patient-data-management/actions/workflows/deploy.yml/badge.svg)](https://github.com/arne-kapell/patient-data-management/actions/workflows/deploy.yml)
[![gitleaks (Secret Scanner)](https://github.com/arne-kapell/patient-data-management/actions/workflows/gitleaks.yml/badge.svg)](https://github.com/arne-kapell/patient-data-management/actions/workflows/gitleaks.yml)
[![CodeQL](https://github.com/arne-kapell/patient-data-management/actions/workflows/codeql.yml/badge.svg)](https://github.com/arne-kapell/patient-data-management/actions/workflows/codeql.yml)
# Patient Data Management System
Webanwendung zur Verwaltung von persönlichen, medizinischen Daten.

Features:
- Dokumentenverwaltung (Upload, Download, Löschen) inkl. In-Browser-Vorschau
- Zugriffs-Freigabe für Angehörige und Ärzte

## Deployment
---
Die Anwendung ist vollständig containerisiert und kann mit Docker und Docker Compose einfach aufgesetzt werden. Die benötigten Docker-Images werden automatisch von Docker Hub geladen bzw. gebaut.

### Testumgebung
```bash
docker-compose up
```
Die folgenden Services stehen zur Verfügung:
| Service                 | Port |
| ----------------------- | ---- |
| Django (Server + UI)    | 8000 |
| PostgreSQL              | -    |
| adminer (DB-Management) | 8080 |

*Hinweis:* Mails (z.B. für die E-Mail-Verifizierung) werden nicht versendet, sondern in der Konsole (des Django-Servers) ausgegeben.

### Produktivumgebung
```bash
docker-compose -f docker-compose.prod.yml up -d
```
Zusätzlich wird eine lokale traefik-Instanz (als reverse proxy) benötigt, die erforderlichen `labels` für das VPS-Deployment ([cloud.arne-kapell.de](https://cloud.arne-kapell.de)) sind bereits in der `docker-compose.prod.yml` hinterlegt.

*adminer* als leichtgewichtiges DB-Management-Tool wird in der Produktivumgebung nicht gestartet, dafür jedoch ein Backup-Service, der die PostgreSQL-Datenbank automatisch in regelmäßigen Abständen sichert.

## Architektur und Bedrohungsanalyse
---
![](slides/architektur.drawio.svg)

## Präsentationen
---
0. [Anforderungen bzw. Aufgabenstellung](slides/Laborarbeit2022AufgabeSichereSysteme.pdf)
1. [Sicherheitsanforderungen & Bedrohungsanalyse](slides/abgabe01.html)


## Testplan
---
| TestID | Typ                       | Beschreibung                                                                                                                                               | Schritte                                                                                                                       | Erwartetes Ergebnis                                          | Status |
| ------ | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ | ------ |
| T1     | Unit-Tests                | Gesundheits- bzw. persönliche Daten dürfen nur nach erfolgreicher Authentifizierung und nach autorisierung (mit den erforderlichen Rechten) abrufbar sein. | Versuchen, Daten ohne vorherigen Login bzw. mit unautorisiertem Benutzer abzurufen                                             | Blockieren mit Fehlermeldung ohne Daten-Leck                 | ---    |
| T2     | Unit-Tests                | Persönliche Daten dürfen nur für den jeweiligen Nutzer einsichtbar sein.                                                                                   | Versuchen auf die persönlichen Daten eines anderen Benutzers zuzugreifen                                                       | Blockieren mit Fehlermeldung ohne Daten-Leck                 | ---    |
| T3     | Pen-Test / Manueller Test | Dokumente können nicht von Benutzern ohne erteilte Freigabe eingesehen werden                                                                              | Versuchen durch Umgehung der Freigabe-Bestimmung an Dokumente zu gelangen                                                      | Blockieren mit Fehlermeldung                                 | ---    |
| T4     | Transaktion-Test          | Abfangen der Datenübertragung mittels Netzwerkmonitoring Tools                                                                                             | Alle abgefangenen Dateien/Informationen befinden sich in einem verschlüsselten Zustand                                         | ---                                                          |        |
| T5     | Unit-Test und Pentests    | Zugriff auf Daten in der Datenbank durch SQL Abgfragen erlangen                                                                                            | Zugriff auf Datenbank mitells SQL Injection                                                                                    | Abblocken des Angriffs durch Eingabevalidierung              | ---    |
| T6     | Unit-Test                 | Zugriff auf Daten in der Datenbank                                                                                                                         | Verbindungsaufbau zur Datenbank ohne gültigen Benutzer bzw. Benutzer mit nötigen Berechtigungen und Versuch Zugang zu erlangen | Verhindern durch Berechtigungsprüfung                        | ---    |
| T7     | Web-Schwachstellen        |                                                                                                                                                            |                                                                                                                                |                                                              |        |
| T8     | Unit-Test  /DDOS          | Ausfall der Datenbank auslösen                                                                                                                             | Durch erhöhte Anzahl an Anfragen Verbindung zur Datenbank kompromittieren                                                      | ---                                                          | ---    |
| T9     | Unit-Test                 | Zugriff auf Administrator Oberfläche ohne Account mit benötigten Berechtigungen                                                                            | Versuchen an Informationen zu gelangen, die nur für Administratoren gedacht sind                                               | Fehlermeldung wegen fehlenden Berechtigungen für den Zugriff | ---    |
| T10    | Unit-Test                 | Schadecode via Upload Einschleusen                                                                                                                         | Infizierte Datei unter Dokumenten hochladen                                                                                    | Filtern der Datei durch Clam AV                              | --- |