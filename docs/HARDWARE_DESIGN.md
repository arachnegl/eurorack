---
title: Eurorack Modules Hardware Design and Sourcing Guide
description: High-level overview of schematic, layout, and front-panel manufacturing files
  for Plaits, Rings, and Marbles open-source hardware.
---
# Eurorack Modules - Hardware Design Guide

This document provides a high-level overview of the hardware design files included in this repository 
for [Plaits](https://github.com/arachnegl/eurorack/tree/master/plaits/hardware_design),
[Rings](https://github.com/arachnegl/eurorack/tree/master/rings/hardware_design), and 
[Marbles](https://github.com/arachnegl/eurorack/tree/master/marbles/hardware_design). 
It explains the purpose of each file format and the software tools required to open, edit, 
or manufacture them.

---

## 1. Directory Structure

Each module contains a `hardware_design` directory organized consistently:
* **Bill of Materials (BOM)**: Located in the root of the folder as an Excel spreadsheet (e.g. `Plaits.xlsx`).
* **PCB Schematics & Layouts**: Located in the `pcb/` sub-folder.
* **Front Panel Graphics & Mechanicals**: Located in the `panel/` sub-folder.

---

## 2. File Formats & Required Software

| File Format | Purpose | Core Software | Free / Open-Source Alternative |
| :--- | :--- | :--- | :--- |
| **`.sch`** | Schematic circuit connections | **Autodesk EAGLE** | **KiCad** (v6+ importer) |
| **`.brd`** | PCB layout and footprints | **Autodesk EAGLE** | **KiCad** (v6+ importer) |
| **`.dwg`** | Mechanical cutouts & slots | **Autodesk AutoCAD** | **QCad** / **LibreCAD** |
| **`.ai`** | Front panel vector artwork | **Adobe Illustrator** | **Inkscape** |
| **`.xlsx`** | BOM sourcing part list | **Microsoft Excel** | **LibreOffice Calc** |

### A. Schematic & PCB Design (`pcb/` directory)
The circuit board layouts and schematics are designed using **Autodesk EAGLE CAD**.
* **`.sch` (Schematic)**: 
  * *Purpose*: The electrical diagram detailing how all components (MCU, Codec, Op-amps, Pots, Jacks) connect.
  * *Software*: Autodesk EAGLE CAD (version 6.x or newer). Can also be imported into **KiCad**
    (v6+ has direct imports).
* **`.brd` (Board Layout)**:
  * *Purpose*: The physical layout of the printed circuit board, including copper traces, component placements, 
    vias, and ground planes. Used to generate Gerber files (RS-274X) for PCB manufacturing.
  * *Software*: Autodesk EAGLE CAD (version 6.x or newer).

### B. Front Panel Design (`panel/` directory)
The mechanical dimensions and graphics for the eurorack faceplates.
* **`.dwg` (AutoCAD Drawing)**:
  * *Purpose*: The mechanical layout containing precise physical dimensions, hole center coordinates, and cutout 
    zones for jacks, pots, LEDs, and mounting screws in standard Eurorack HP widths. Used for CNC
    milling or PCB-panel routing.
  * *Software*: Autodesk AutoCAD, **QCad** (free/open-source alternative), or **LibreCAD**.
* **`.ai` (Adobe Illustrator)**:
  * *Purpose*: Vector art containing faceplate graphics, legends, labels, and color blocks. Used for screen-printing 
    or UV printing.
  * *Software*: Adobe Illustrator, **Inkscape** (free/open-source vector editor), or CorelDRAW.

### C. Bill of Materials (`.xlsx` spreadsheet)
* *Purpose*: The list of all electronic parts, quantities, reference designators (e.g. R1, C1), package sizes 
  (typically 0603 for passive components), and suggested manufacturer/supplier parts.
* *Software*: Microsoft Excel, **LibreOffice Calc** (free), or Google Sheets.

---

## 3. Hardware Design Reference Links

* **[Plaits Hardware Design Files](https://github.com/arachnegl/eurorack/tree/master/plaits/hardware_design)**
* **[Rings Hardware Design Files](https://github.com/arachnegl/eurorack/tree/master/rings/hardware_design)**
* **[Marbles Hardware Design Files](https://github.com/arachnegl/eurorack/tree/master/marbles/hardware_design)**
