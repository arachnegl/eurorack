---
title: Plaits - Macro Oscillator Developer Documentation
description: Technical overview of the Plaits Eurorack module, covering digital synthesis
  models, system clock architectures, and custom engine development.
---
# Plaits Firmware Documentation

Welcome to the developer documentation for the **Plaits** macro oscillator firmware.

## Document Directory

* **[Architecture](ARCHITECTURE.md)**: Explore the system-level design, dynamic memory management (overlap allocations), voice rendering layers, and the engine catalog.
* **[Compiling & Flashing Guide](BUILD_GUIDE.md)**: Step-by-step instructions on setting up the GNU ARM Embedded Toolchain, compiling firmware targets, generating QPSK audio updater files, and flashing via SWD/JTAG.
* **[Calibration & Settings](CALIBRATION.md)**: Insights into ADC calibration tables, physical pot smoothing filters, and the low-pass gate (LPG) state storage system.
* **[Custom Engines Development](CUSTOM_ENGINES.md)**: A boilerplate-to-registration guide on how to implement your own synthesis algorithms inside the Plaits module.
* **[User Data Format](USER_DATA_FORMAT.md)**: Technical overview of the Wavetable and LPC speech data receiver formats, transmission QPSK standards, and flash memory layout.

---

### In-depth Walkthroughs

* **[Additive Engine](dsp/additive_engine.md)**: Additive synthesis with 32 partials (24 integer harmonics and 8 organ harmonics).
* **[Bass Drum Engine](dsp/bass_drum_engine.md)**: TR-808/909-inspired analog and synthetic kick drum modeling.
* **[Chiptune Engine](dsp/chiptune_engine.md)**: 8-bit style multi-voice square/NES-triangle oscillators with arpeggiation.
* **[Chord Engine](dsp/chord_engine.md)**: Dynamic chord/organ voicing with wavetable morphing and chorus.
* **[FM Engine](dsp/fm_engine.md)**: 2-operator frequency/phase modulation synthesis with dynamic morphable feedback.
* **[Grain Engine](dsp/grain_engine.md)**: Granular formant and pitch-shifted Z-oscillator synthesis.
* **[Hi-Hat Engine](dsp/hi_hat_engine.md)**: TR-808/909-inspired analog/synthetic hi-hat models with metallic noise banks.
* **[Modal Engine](dsp/modal_engine.md)**: Modal resonator synthesis for bells, plates, and strings.
* **[Noise Engine](dsp/noise_engine.md)**: Clocked noise, dust, and multi-mode zero-delay state variable filtering.
* **[Particle Engine](dsp/particle_engine.md)**: Poisson-process granular particle clouds with allpass diffusion networks.
* **[Phase Distortion Engine](dsp/phase_distortion_engine.md)**: Synced/free-running virtual analog phase distortion oscillators.
* **[Six Operator FM Engine](dsp/six_op_engine.md)**: Yamaha DX7-style 6-operator FM algorithm rendering with SysEx patches.
* **[Snare Drum Engine](dsp/snare_drum_engine.md)**: TR-808/909-inspired analog and synthetic snare drum modeling.
* **[Speech Engine](dsp/speech_engine.md)**: Vowel formant filters, SAM phase-reset synth, and LPC-10 speech synthesis.
* **[String Engine](dsp/string_engine.md)**: Karplus-Strong string physical modelling with dispersion and buzzing non-linearities.
* **[String Machine Engine](dsp/string_machine_engine.md)**: Divide-down string synthesizer with Solina-style ensemble chorus.
* **[Swarm Engine](dsp/swarm_engine.md)**: Detuned supersaw swarm with grain-modulated amplitude envelopes.
* **[Virtual Analog Engine](dsp/virtual_analog_engine.md)**: Synced multi-waveform virtual analog oscillators with PolyBLEP band-limiting.
* **[Virtual Analog VCF Engine](dsp/virtual_analog_vcf_engine.md)**: Virtual analog waveshaping with dynamic lowpass/bandpass filters.
* **[Wave Terrain Engine](dsp/wave_terrain_engine.md)**: 2D height map coordinate scanning with phase-modulated auxiliary output.
* **[Waveshaping Engine](dsp/waveshaping_engine.md)**: Triangle/slope sources with waveshaper tables and wavefolding.
* **[Wavetable Engine](dsp/wavetable_engine.md)**: Spatial trilinear/hermite interpolation over 2D/3D wavetables with lo-fi bitcrushing.
