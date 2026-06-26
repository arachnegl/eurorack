---
title: Rings - Resonator Developer Documentation
description: Technical overview of the Rings Eurorack module, covering waveguide
  physical modeling, modal resonators, and voice allocators.
---
# Rings Resonator Documentation

Rings is an ARM Cortex-M4 physical modeling resonator module that simulates the vibration of structures 
like strings, tubes, plates, and membranes.

## Document Directory

* **[Architecture](ARCHITECTURE.md)**: Detailed exploration of the Rings codebase, hardware memory mappings
  (CCM SRAM), CV calibration laws, jack normalizations, voice allocation patterns, and resonator models.
* **[Build Guide](BUILD_GUIDE.md)**: Steps to setup the toolchain, compile, and flash the module.
* **[Rings DSP Codebase](https://github.com/arachnegl/eurorack/tree/master/rings)**: Source directory containing the hardware drivers and audio engine.

---

### DSP Resonators

* **[Modal Resonator](dsp/modal_resonator.md)**: Deep dive into modal synthesis principles,
  bandpass filter banks (64 State Variable Filters), and pick-up position simulation via cosine oscillators.
* **[Sympathetic String](dsp/sympathetic_string.md)**: Technical breakdown of coupled
  waveguide models, chord/scale morph tuning tables, and virtual bridge feedback routing.
* **[Inharmonic String](dsp/inharmonic_string.md)**: Analysis of waveguide dispersion
  (string stiffness allpass filtering), sitar-like buzz bridge non-linearities, and bowing/scrape noise inputs.

---

## Core DSP Layout

The synthesis engine of [Rings](https://github.com/arachnegl/eurorack/tree/master/rings) is divided into the following layers:
- **System Level**: [rings.cc](https://github.com/arachnegl/eurorack/blob/master/rings/rings.cc) starts hardware clocks, initializes drivers, and 
  runs the main loop.
- **UI & Control**: [ui.cc](https://github.com/arachnegl/eurorack/blob/master/rings/ui.cc) processes knobs, CV inputs, buttons, and manages the panel settings.
- **DSP Engine**: Located in the [rings/dsp](https://github.com/arachnegl/eurorack/tree/master/rings/dsp) directory:
  - [Part](https://github.com/arachnegl/eurorack/blob/master/rings/dsp/part.h) orchestrates the voices, allocating new excitation signals and resonator nodes.
  - [Resonator](https://github.com/arachnegl/eurorack/blob/master/rings/dsp/resonator.h) simulates the physical resonance using parallel bandpass filter banks.
  - [String](https://github.com/arachnegl/eurorack/blob/master/rings/dsp/string.h) implements waveguide physical modeling.
