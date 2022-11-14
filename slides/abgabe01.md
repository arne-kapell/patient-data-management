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
<!-- Arne -->
Projekt: Security by Design (Semester 5)

# Patient Data Management System

## Sicherheitsanforderungen & Bedrohungsanalyse

*Irina Jörg, Finn Callies, Arne Kapell*

---
<!-- _paginate: false -->
<!--
Arne
Trust-Boundaries
-->
# Threat Modeling

![bg right:70% contain](architektur.drawio.svg)

---
<!-- Irina -->
# Schutzziele

| Asset                      | Vertraulichkeit | Integrität | Verfügbarkeit |
| :------------------------- | :-------------: | :--------: | :-----------: |
| **A01**: Gesundheits-Daten |      X(1)       |    X(1)    |     X(2)      |
| **A02**: Persönl. Daten    |      X(1)       |    X(2)    |     X(3)      |
| **A03**: Anmelde-Daten     |      X(1)       |    X(2)    |     X(3)      |
| **A04**: Session-Daten     |      X(1)       |    X(3)    |     X(2)      |
| **A05**: Log-Daten         |      X(2)       |    X(1)    |     X(3)      |

---
<!-- Irina -->
# Technologie-Stack

- Django (Python) für Frontend und Backend
  - integriertes Admin-Interface
- Datei-basierte Datenbank (SQLite)
![bg vertical right:60%](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmertcangokgoz.com%2Fwp-content%2Fuploads%2Fdjango-python-grosel.png&f=1&nofb=1&ipt=f4fa7ec45ecb575921c4c1424ef6c24dc6c5bbdfdedf635893cf8ba8a5be6242&ipo=images)
![bg](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fportalzine.de%2Fwp-content%2Fuploads%2Fsites%2F3%2F2017%2F08%2Fsqllite.jpg&f=1&nofb=1&ipt=059865215eea28d3d7159e051e543a91e862b954437ac9d36aec4d13c0e554dc&ipo=images)

---
<!-- _class: lead -->
<!-- Finn -->
# Risiko-Register

---
<!-- Finn -->
# Risiko-Register (1/4)

![width:5000](r6.png)

---
<!-- Finn -->
# Risiko-Register (2/4)

![width:5000](r7.png)

---
<!-- Finn -->
# Risiko-Register (3/4)

![width:5000](r8.png)

---
<!-- Finn -->
# Risiko-Register (4/4)

![width:5000](r9.png)

---
<!-- Finn -->
<!-- 
_class: lead
paginate: false
-->
# Vielen Dank fürs Zuhören

Fragen?
