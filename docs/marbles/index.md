---
title: Marbles - Random Sampler Developer Documentation
description: Technical overview of the Marbles Eurorack module, covering random clock
  generators, CV sequence shift registers, and quantizers.
---
# Marbles Random Sampler Documentation

Marbles is an ARM Cortex-M4 random voltage and gate generator that sequences fluctuating CVs and triggers.

## Document Directory

* **[Architecture](ARCHITECTURE.md)**: Detailed exploration of the Marbles codebase, hardware self-patching 
  detectors, CV slew-rate compensations, Deja Vu loops, and output DAC mappings.
* **[Compiling & Flashing Guide](BUILD_GUIDE.md)**: Steps to setup the toolchain, compile, and flash the module.
* **[Marbles DSP Codebase](https://github.com/arachnegl/eurorack/tree/master/marbles)**: Source directory containing the hardware drivers and random engines.

---

### Random Engines

* **[t Generator](random/t_generator.md)**: Rhythmic gate/trigger generation engine, including 
  complementary Bernoulli coin tosses, clock divider/multipliers, and Markov transition models.
* **[X & Y Generators](random/x_y_generator.md)**: Continuous random voltage generation engine, 
  including Beta distribution sampling, steps/smooth quantization, and lag processors.
* **[Deja Vu Memory](random/deja_vu.md)**: Looping shift-register memory,
  covering mutation probabilities, history buffers, and correlated phase-shifted channel replay.

---

## Core DSP Layout

The random engines of [Marbles](https://github.com/arachnegl/eurorack/tree/master/marbles) are divided into the following layers:
- **System Level**: [marbles.cc](https://github.com/arachnegl/eurorack/blob/master/marbles/marbles.cc) handles the hardware setup, ADC/DAC updates,
  and clock interrupts.
- **UI & Controls**: [ui.cc](https://github.com/arachnegl/eurorack/blob/master/marbles/ui.cc) scans the control inputs, buttons, and manages system state/saving.
- **Random Generators**: Located in the [marbles/random](https://github.com/arachnegl/eurorack/tree/master/marbles/random) directory:
  - [TGenerator](https://github.com/arachnegl/eurorack/blob/master/marbles/random/t_generator.h) generates random clock divisions, multiplications,
    and trigger sequences.
  - [XYGenerator](https://github.com/arachnegl/eurorack/blob/master/marbles/random/x_y_generator.h) produces random control voltages (smooth, stepped,
    or quantized).
  - [RandomSequence](https://github.com/arachnegl/eurorack/blob/master/marbles/random/random_sequence.h) implements shift registers and loop/deja-vu
    sequence buffering.
