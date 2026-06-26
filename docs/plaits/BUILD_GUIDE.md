# Plaits - Compiling & Flashing Guide

This document describes how to compile the firmware for [Plaits](https://github.com/arachnegl/eurorack/tree/master/plaits) and flash it onto
the STM32F373 microcontroller.

---

## 1. Prerequisites & Toolchain Setup

The build system relies on the **GNU ARM Embedded Toolchain** (specifically GCC version 4.8.3 or similar) and standard
GNU make utilities.

1. **Install Toolchain**: Download and unpack the `gcc-arm-none-eabi` compiler.
2. **Define Compiler Path**: Define the `TOOLCHAIN_PATH` variable pointing to the compiler binary directory inside the
   [makefile](https://github.com/arachnegl/eurorack/blob/master/plaits/makefile#L57):
   ```makefile
   TOOLCHAIN_PATH ?= /usr/local/arm-none-eabi/
   ```
3. **Firmware Dependencies**: Ensure `stmlib` subdirectories are populated as they provide system startup, peripheral
   abstraction, and DSP math headers.

---

## 2. Compilation Targets

Compilation commands are run from the project root or the `plaits` directory:

### A. Build standard binary
Generates build output binaries inside the `build/plaits` folder:
```bash
make
```

### B. Generate Audio Firmware Update WAV File
Plaits can be flashed by playing a modulated audio file into its Model/CV input. To build this WAV file:
```bash
make wav
```
This runs the Python script [encoder.py](https://github.com/arachnegl/eurorack/blob/master/stm_audio_bootloader/qpsk/encoder.py):
```bash
python stm_audio_bootloader/qpsk/encoder.py \
    -t stm32f3 -k -s 48000 -b 12000 -c 6000 -p 256 \
    build/plaits/plaits.bin
```
It outputs `plaits.wav`, which uses QPSK (Quadrature Phase-Shift Keying) modulation to transmit data.

---

## 3. Hardware Flashing

If you have a hardware debugger (ST-Link, J-Link, or Olimex JTAG adapter) connected to the module's SWD/JTAG debug header:

### A. Direct JTAG/SWD Programming
```bash
make upload
```
This invokes `openocd` (configured via `stmlib/makefile.inc`) to erase the flash sectors and write the compiled ELF binary.

### B. Dump User Wavetable Flash Data
To extract the custom user data from address `0x08007000` (4 KB):
```bash
make user_data_image
```
This dumps `plaits_user_data.bin` containing the active custom wavetables or speech frames.
