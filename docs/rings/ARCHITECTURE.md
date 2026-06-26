# Rings Architecture

This document details the firmware and DSP architecture of the [Rings](https://github.com/arachnegl/eurorack/tree/master/rings) resonator module.
It outlines system-level initialization, CV scaling, trigger/strumming logic, voice allocation, and the
available resonator models.

---

## 1. System Level & Hardware Integration

The firmware entry point is in [rings.cc](https://github.com/arachnegl/eurorack/blob/master/rings/rings.cc). At startup:
1. System clocks, GPIOs, and peripheral timers are initialized via the `System` class.
2. The core audio codec is started with `FillBuffer` acting as the stereo audio callback.
3. The main thread enters an infinite loop, executing UI updates (`ui.DoEvents()`) asynchronously.

### CCM SRAM Allocation
Due to the high memory demands of physical modeling delay lines and stereo reverberation, Rings allocates its
reverb buffer (`reverb_buffer`) inside the **CCM (Core Coupled Memory) SRAM** section (`.ccmdata`). 
CCM memory is accessed directly by the ARM Cortex-M4 CPU D-bus without sharing access with the DMA controller,
allowing zero-wait-state memory execution and eliminating bus contention with peripheral tasks.

### Strumming & Trigger Logic
Rings determines when to pluck or strum the resonator using the [Strummer](https://github.com/arachnegl/eurorack/blob/master/rings/dsp/strummer.h) class. 
Strumming triggers are processed as follows:
- **External Trigger**: When a jack is patched to the STRUM input, a trigger directly instigates a strum.
- **V/Oct Transposition Strum**: If no trigger jack is patched, but a cable is connected to the V/Oct pitch input,
  Rings automatically triggers a strum when the input pitch changes by more than 0.4 semitones.
- **Audio/Exciter Transient Strum**: If only the exciter input is connected, the
  [OnsetDetector](https://github.com/arachnegl/eurorack/blob/master/rings/dsp/onset_detector.h) analyzes the incoming audio. When a transient is
  detected, it triggers a strum.

---

## 2. Control Rate & CV Processing

All potentiometer, CV, and attenuverter inputs are read, scaled, and calibrated by [CvScaler](https://github.com/arachnegl/eurorack/blob/master/rings/cv_scaler.h).

### Input Calibration & Laws
CV inputs are filtered using first-order low-pass filters with specific transfer curves (`Law`):
- **Linear**: Used for frequency, structure, brightness, damping, and position.
- **Quadratic Bipolar / Quartic Bipolar**: Applied to the attenuverters to allow fine-grained precision around the
  center detent, while allowing full-range sweeps at the extremes.

### Jack Normalization Detection
To determine if CV inputs are patched, Rings uses a hardware-assisted random-bit probing system:
1. The [NormalizationProbe](https://github.com/arachnegl/eurorack/blob/master/rings/drivers/normalization_probe.h) injects a pseudo-random binary sequence
   onto the normalization contacts of the jacks.
2. The [NormalizationDetector](https://github.com/arachnegl/eurorack/blob/master/rings/cv_scaler.h#L58) monitors whether this bitstream is read back by the
   corresponding GPIOs/ADCs.
3. If the injected random sequence matches the read signal, the jack is open (normalized). If the sequence is
   broken (due to a patch cable grounding the contact), it detects a jack insertion.

### Easter Egg Gesture
Rings hides a polyphonic **String Synth** easter egg. It is unlocked when the pots and attenuverters are placed
in a specific, highly detailed geometric gesture (as checked by `CvScaler::easter_egg()`):
- **FREQUENCY** pot < 10%, **Attenuverter** > 100% (fully CW)
- **STRUCTURE** pot > 90%, **Attenuverter** > 100% (fully CW)
- **BRIGHTNESS** pot < 10%, **Attenuverter** < -100% (fully CCW)
- **POSITION** pot > 90%, **Attenuverter** < -100% (fully CCW)
- **DAMPING** pot centered (~50%), **Attenuverter** < -100% (fully CCW)

---

## 3. Voice Allocation & Polyphony

Rings can operate in monophonic, duophonic, or quadraphonic modes (`polyphony_ = 1, 2, or 4`).

### Dynamic Resolution Scaling
Because physical modeling is computationally expensive, Rings scales the resolution (the number of partials
or filter nodes) dynamically to fit within the CPU cycle budget:
- **Polyphony = 1**: 60 modes/partials per voice.
- **Polyphony = 2**: 28 modes/partials per voice.
- **Polyphony = 4**: 12 modes/partials per voice.

### Pitch Allocation
When a strum is received, the target pitch is filtered by the `NoteFilter` class and assigned to a voice:
- In monophonic mode, voice 0 is updated.
- In odd-numbered polyphony (polyphony = 3 in custom systems), a ping-pong spatial allocation pattern is used
  (`{1, 0, 2, 1, 0, 2, 1, 0}`) to cycle voices across the stereo field.
- In even-numbered polyphony (polyphony = 2 or 4), it cycles sequentially: `(active_voice_ + 1) % polyphony_`.

### Output Mixing & Stereo Dispatch
- **Monophonic Mode**: The main and auxiliary outputs dispatch the two distinct resonator pickups (odd and
  even harmonics) directly to Left and Right channels.
- **Polyphonic Mode**: Dispatches odd-numbered voices to the Right channel (`aux`) and even-numbered voices to
  the Left channel (`out`), creating spatial panning across voices.

---

## 4. Resonator Models

Rings features three standard resonator models and three corresponding bonus/easter egg models.

### Standard Resonator Models
1. **Modal Resonator** (`RESONATOR_MODEL_MODAL`):
   Simulates plates, membranes, or bars using parallel bandpass filter banks (resonator modes) excited by a short
   synthesized trigger pulse or an external signal.
2. **Sympathetic String** (`RESONATOR_MODEL_SYMPATHETIC_STRING`):
   Simulates virtual strings coupled to a soundboard. The notes of the virtual strings are continuously morphed
   across chordal/modal scales based on the `STRUCTURE` parameter.
3. **Inharmonic String** (`RESONATOR_MODEL_STRING`):
   A waveguide string model with dispersion (stiffness) and decay time controls.

### Bonus / Easter Egg Resonator Models
1. **2-Op FM Voice** (`RESONATOR_MODEL_FM_VOICE`):
   A dual-operator frequency modulation synthesis engine with internal envelopes.
2. **Quantized Sympathetic String** (`RESONATOR_MODEL_SYMPATHETIC_STRING_QUANTIZED`):
   Same as the sympathetic string model, but restricts pitches of the vibrating strings strictly to the quantized
   chords table based on the selected polyphony.
3. **String & Reverb** (`RESONATOR_MODEL_STRING_AND_REVERB`):
   Waveguide strings routed directly through a high-density built-in digital reverberation algorithm.

---

## 5. The Easter Egg: String Synth (`StringSynthPart`)

When the easter egg gesture is detected, the audio loop routes process blocks to the
[StringSynthPart](https://github.com/arachnegl/eurorack/blob/master/rings/dsp/string_synth_part.h) rather than the resonator:
- **12-Voice Polyphony**: Synthesizes full, lush chords using string waveforms.
- **Formant & FX Section**: Passes the raw strings through formant filters (simulating vocal tract resonances)
  and built-in chorus/ensemble/reverb effects before reaching the outputs.
- **Envelope Control**: Uses a dedicated envelope generator per voice group to control articulation and release.

---

<!-- KaTeX support for mathematical formulas -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ]
        });"></script>
