---
marp: true
theme: anhembi
# class: invert
paginate: true
footer: 'PDM System | Security by Design'
---
<!-- 
_paginate: false 
_class:
    - lead
-->
Projekt: Security by Design (Semester 5)
# Patient Data Management System

## Sicherheitsanforderungen & Bedrohungsanalyse

*Irina Jörg, Finn Callies, Arne Kapell*
<!-- Notes... -->

---
# Agenda

1. Thread Modeling

---
# Thread Modeling
![bg right:70% contain](architektur.drawio.svg)

---
# Schutzziele
| Schutzobjekt | Vertraulichkeit | Integrität | Verfügbarkeit |
| :----------- | :-------------- | :--------- | :------------ |
| **A01**      | X(1)            | X(1)       | X(2)          |
| **A02**      | X(1)            | X(2)       | X(3)          |
| **A03**      | X(1)            | X(2)       | X(3)          |
| **A04**      | X(1)            | X(3)       | X(2)          |

---
<!-- _class: lead -->
# Sicherheitsanforderungen

---
# Sicherheitsanforderungen (1/4)
| Schutzobjekt  | Schutzziele                 | Anforderungen                                                                                                           |
| :------------ | :-------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| Benutzerdaten | Vertraulichkeit, Integrität | - Schutz der beim Erstellen eines Accounts angegebenen Daten<br/>- Einhaltung der gesetzlichen Datenschutz-Bestimmungen |

---
# Sicherheitsanforderungen (2/4)
Upload von Daten

---
# Sicherheitsanforderungen (2/4)
Zugriff auf Daten

---
# Sicherheitsanforderungen (2/4)
Manipulation von Daten

---
# Technologie-Stack
- Django (Python) für Frontend und Backend
  - integriertes Admin-Interface
- Datei-Basierte Datenbank (SQLite)
![bg right:60% cover](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmertcangokgoz.com%2Fwp-content%2Fuploads%2Fdjango-python-grosel.png&f=1&nofb=1&ipt=f4fa7ec45ecb575921c4c1424ef6c24dc6c5bbdfdedf635893cf8ba8a5be6242&ipo=images)

---
# Risk-Register (5 Szenarien)

1. Unbefugter Zufriff auf Gesundheits-Daten
2. Manipulation von gespeicherten Gesundheits-Daten
3. Verfügbarkeits-Ausfall von Datenbank und Dokumenten-Speicher
4. Unsichere Datenübertragung
5. Unbefugter Zugriff auf System-Administration