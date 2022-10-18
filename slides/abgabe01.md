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
| Schutzobjekt | Vertraulichkeit | Integrität | Verfügbarkeit | Anmerkungen |
| :----------- | :-------------- | :--------- | :------------ | :---------- |
| **A01**      | X(1)            | X(1)       | X(2)          |             |
| **A02**      | X(1)            | X(2)       | X(3)          |             |
| **A03**      | X(1)            | X(2)       | X(3)          |             |

