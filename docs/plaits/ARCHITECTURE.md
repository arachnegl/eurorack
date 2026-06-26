# Plaits Architecture

This document covers the firmware architecture of [Plaits](https://github.com/arachnegl/eurorack/tree/master/plaits).
It describes how the hardware drivers, user interface, voice layer, and synthesis engines are organized and how
they interact to perform real-time, low-latency DSP synthesis.

---

## 1. System Level & Hardware Integration

The firmware entry point is in [plaits.cc](https://github.com/arachnegl/eurorack/blob/master/plaits/plaits.cc). At startup:
1. System clocks and peripherals are configured.
2. The core synthesis classes ([Voice](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.h) and drivers) are initialized.
3. The DMA-driven I2S audio driver is started with [FillBuffer](https://github.com/arachnegl/eurorack/blob/master/plaits/plaits.cc#L74)
   acting as the callback.
4. The main thread enters an infinite loop, executing no-op cycles, while the hardware watchdog is kicked and UI events
   are processed asynchronously in interrupt and DMA contexts.

### Normalization Detection
Plaits detects whether patch cables are inserted into its CV inputs (like FREQ, TIMBRE, MORPH) by injecting a
pseudo-random bit sequence onto the normalization contacts of the inputs. The function
[Ui::DetectNormalization](https://github.com/arachnegl/eurorack/blob/master/plaits/ui.cc#L425) evaluates whether the ADC reads the same
sequence (meaning the contact is closed and no jack is inserted) or if the sequence is broken (meaning a jack is
inserted). This determines whether the internal LPG and decay envelope are activated.

### Input Latency Compensation
Because sequencers or MIDI-to-CV converters often exhibit a small lag between CV transitions and gate transitions,
Plaits buffers the trigger input through a delay line ([trigger_delay_](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.cc#L87))
to shift trigger events by 1ms. This aligns transient triggers with pitch transitions, avoiding clicky/detuned offsets.

---

## 2. Dynamic Memory Management

Due to the limited 32 KB SRAM of the STM32F373 MCU, allocating static memory buffers for all 24 synthesis engines
simultaneously is impossible. Instead, Plaits uses an overlap allocation pattern:

1. A single shared array `shared_buffer` (16,384 bytes) is declared in [plaits.cc](https://github.com/arachnegl/eurorack/blob/master/plaits/plaits.cc#L56).
2. An explicit [BufferAllocator](https://github.com/arachnegl/eurorack/blob/master/stmlib/utils/buffer_allocator.h) manages this space.
3. During startup, inside `Voice::Init`, the allocator is reset (`allocator->Free()`) before initializing each engine:
   ```cpp
   for (int i = 0; i < engines_.size(); ++i) {
     allocator->Free();
     engines_.get(i)->Init(allocator);
   }
   ```
4. Each engine's `Init()` requests its workspace memory starting at the beginning of the buffer. Because only one
   engine renders audio at any time, this overlap is completely safe and maximizes memory usage.

---

## 3. The Voice Layer (`Voice` Class)

The [Voice](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.h) class orchestrates the synth engine. Its central method
is [Voice::Render](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.cc#L90), which processes a single block of audio:

- **Decay & LPG Envelopes**: Processes the internal decay envelopes and LPG frequency/amplitude envelopes.
- **Engine Selection**: Determines the current active engine index based on patch options and CV inputs using
  `engine_quantizer_`.
- **User Data Loading**: If the engine changed, it loads wavetable or LPC data using `e->LoadUserData(...)`.
- **Modulation Routing**: Blends raw parameters with CV, envelope levels, and internal decay outputs using the
  `ApplyModulations` utility.
- **Rendering**: Calls `e->Render(p, out_buffer_, aux_buffer_, size, &already_enveloped)`. The engine can dynamically
  flag if its current model already includes an envelope (`already_enveloped`).
- **Post Processing**: Passes the main and auxiliary output buffers through [ChannelPostProcessor](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.h#L73)
  which applies the Low-Pass Gate (LPG) envelope, limiting (if gain is negative), and converts the output to 16-bit PCM.

---

## 4. The Engine Layer

All digital oscillators inherit from the base [Engine](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/engine/engine.h) class
and are registered in [EngineRegistry](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/engine/engine.h#L95).

### Engine Catalog (24 Models)

The engines are divided into three groups of eight models:

1. **Classic Synthesis Bank**:
   - `VirtualAnalogEngine`: Classic waveforms (saw, pulse, triangle) with wavefolding and sync.
   - `WaveshapingEngine`: Asymmetrical triangle shaping and fold parameters.
   - `FMEngine`: Two-operator FM with feedback.
   - `GrainEngine`: Granular pitch-shifter/formant synthesizer.
   - `AdditiveEngine`: Harmonic additive oscillator.
   - `WavetableEngine`: Interpolated wavetable lookup.
   - `ChordEngine`: Chord organ simulator.
   - `SpeechEngine`: LPC vocal synthesizer and formant filters.

2. **Noise, Drums, & Resonators Bank**:
   - `SwarmEngine`: Super-saw cluster.
   - `NoiseEngine`: Clocked digital noise with filter banks.
   - `ParticleEngine`: Granular particle rain.
   - `StringEngine`: Waveguide physical modeling string.
   - `ModalEngine`: Modal drum physical modeling.
   - `BassDrumEngine`: Analog kick drum model.
   - `SnareDrumEngine`: Analog snare drum model.
   - `HiHatEngine`: Analog hi-hat model.

3. **Alternative Synthesis Bank**:
   - `VirtualAnalogVCFEngine`: Virtual analog waves passing through a resonant low-pass filter.
   - `PhaseDistortionEngine`: Phase-distortion synthesizer.
   - `SixOpEngine` (3 instances): Six-operator FM engine loading DX7 patches.
   - `WaveTerrainEngine`: 2D wave terrain slider.
   - `StringMachineEngine`: String ensemble synth chords.
   - `ChiptuneEngine`: Retro computer sound generator.

---

## 5. Coding Idioms & DSP Principles

When reading or modifying code in Plaits, keep the following design constraints in mind:

- **No Heap Allocation**: Standard template containers and dynamic allocations (`new`/`delete`) are banned. All memory
  must pass through the stack, static allocations, or the custom `BufferAllocator`.
- **Deterministic Block Size**: The DSP operates on block boundaries of 12 samples (`kBlockSize`). Keep loops simple to
  encourage compilation vectorization.
- **Clock Dividers & Sample Rate**: The sample rate is strictly corrected to `47,872.34 Hz` in calculations to adjust
  for the lack of fractional PLL dividers on the hardware, avoiding pitch shifts.

---

## 6. Case Study: FM Engine

A detailed developer analysis of the FM synthesis engine has been moved to a separate file:
- [FM Engine](dsp/fm_engine.md)
