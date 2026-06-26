Mutable Instruments' Eurorack Modules.

* [Marbles](http://mutable-instruments.net/modules/marbles): Random sampler.
* [Plaits](http://mutable-instruments.net/modules/plaits): Macro oscillator.
* [Rings](http://mutable-instruments.net/modules/rings): Resonator.

Dependencies
============

The STM32F-based modules (Plaits, Rings, Marbles) depend on the following library directories:
- **stmlib**: Contains STM32F peripheral templates, DSP utilities, and the common makefile build rules
  (stmlib/makefile.inc).
- **stm_audio_bootloader**: Contains QPSK/FSK audio bootloader source code and the Python wav encoder script
  (stm_audio_bootloader/qpsk/encoder.py) used to compile firmware binaries into audio update files.

Microcontroller Overview
========================

The active modules in this repository run on the following microcontrollers:

| Module | MCU Model | Core | Clock Speed | Flash / RAM | Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Plaits** | STM32F373CCT6 | ARM Cortex-M4 | 72 MHz | 256 KB / 32 KB | [ST Docs][F373] |
| **Rings** | STM32F405RGT6 | ARM Cortex-M4 | 168 MHz | 1 MB / 192 KB | [ST Docs][F405] |
| **Marbles**| STM32F405RGT6 | ARM Cortex-M4 | 168 MHz | 1 MB / 192 KB | [ST Docs][F405] |

[F373]: https://www.st.com/en/microcontrollers-microprocessors/stm32f373cc.html
[F405]: https://www.st.com/en/microcontrollers-microprocessors/stm32f405rg.html

Documentation & GitHub Pages
============================

The project documentation is located in the [docs](docs) folder and is hosted via GitHub Pages:
- **Site URL**: `https://arachnegl.github.io/eurorack/`
- **Source**: Configured to build from the `/docs` directory on the `master` branch.
- **Rendering engine**: Jekyll (using `jekyll-theme-minimal` specified in `docs/_config.yml`).
- **Diagrams & Math**: Automatically renders Mermaid flowcharts and LaTeX mathematical formulas (via KaTeX).

### Tracking Deployments

To track Pages builds and publishing jobs:
1. **GitHub CLI**: Check the latest build status:
   `gh api repos/arachnegl/eurorack/pages/builds --jq '.[0] | {status: .status, commit: .commit}'`
2. **GitHub Web**: Visit Settings -> Pages, or look under the "github-pages" environment on the homepage.

License
=======

Code (AVR projects): GPL3.0.

Code (STM32F projects): MIT license.

Hardware: cc-by-sa-3.0

By: Emilie Gillet (emilie.o.gillet@gmail.com)

Guidelines for derivative works
===============================

**Mutable Instruments is a registered trademark.**

The name "Mutable Instruments" should not be used on any of the derivative works you create from these files.

We do not recommend you to keep the original name of the Mutable Instruments module for your derivative works.

For example, your 5U adaptation of Mutable Instruments Clouds can be called "Foobar Modular - Particle Generator".
