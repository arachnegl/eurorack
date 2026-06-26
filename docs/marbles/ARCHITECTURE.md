# Marbles Architecture

This document details the firmware and DSP architecture of the [Marbles](https://github.com/arachnegl/eurorack/tree/master/marbles) random sampler module.
It outlines system-level execution, CV reading, the Deja Vu memory loop, and the output generators.

---

## 1. System Level & Hardware Integration

The firmware entry point is in [marbles.cc](https://github.com/arachnegl/eurorack/blob/master/marbles/marbles.cc). At startup:
1. The hardware system, DAC/ADC drivers, and gate inputs/outputs are initialized.
2. The internal STM32 random number generator (RNG) is started to populate the entropy stream.
3. The block processing loop `Process()` is invoked at 32 kHz.

### Self-Patching Detection
Marbles can dynamically detect if its clock inputs are patched from its own gate outputs (T1, T2, or T3). 
The [ClockSelfPatchingDetector](https://github.com/arachnegl/eurorack/blob/master/marbles/clock_self_patching_detector.h) analyzes gate transitions:
- If a rising edge on the clock input matches a trigger generated on one of the T outputs, Marbles marks
  the input as "self-patched".
- This automatically adapts the internal timing and clock divider ratios to respond locally rather than
  treating the connection as a generic external clock.

### Slew-Rate Compensation
To capture external CV values cleanly on rising clock edges without recording slew-rate artifacts (e.g. from slow
external sequencers), Marbles implements a **2ms reacquisition window** (`kNumReacquisitions = 20` samples):
- When a trigger fires, the shift register acquires the initial CV.
- Over the next 2ms, the input CV is tracked and updated dynamically (`RewriteValue()`) until it stabilizes,
  ensuring the final, correct voltage is stored.

---

## 2. Control Rate & CV Processing

Inputs are read and calibrated by the [CvReader](https://github.com/arachnegl/eurorack/blob/master/marbles/cv_reader.h) class.

### Scale Recorder
The [ScaleRecorder](https://github.com/arachnegl/eurorack/blob/master/marbles/scale_recorder.h) enables recording custom user scales:
- It tracks incoming CV voltages when the module is in scale recording mode.
- Users patch a keyboard or sequencer to record notes, and Marbles builds a histogram of notes to define 
  quantization bins.

### Discrete Length Quantization
Knobs like DEJA VU length are quantized to musical lengths (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16 steps) using the
`HysteresisQuantizer2` class. Hysteresis prevents value flickering when a knob sits on the boundary.

---

## 3. Deja Vu Memory & Loop Buffer

The Deja Vu loop is managed by the [RandomSequence](https://github.com/arachnegl/eurorack/blob/master/marbles/random/random_sequence.h) class.

### Loop Buffer
Each random channel features a `loop_` array that buffers up to 16 values.
- `deja_vu_` controls the probability of repeating the loop vs. mutating:
  - `deja_vu = 0.5` (center): Loops repeat perfectly.
  - `deja_vu = 0.0` (CCW): Infinite, non-repeating random values are generated.
  - `deja_vu = 1.0` (CW): Loop values are replayed, but the playback head jumps randomly.
- **Mutation Probability**: Formulated as $p = (2d - 1)^2$ where $d$ is the Deja Vu knob value.

### Channel Sync & Locking
- Multiple channels (e.g., X1, X2, X3) can be locked to the *same* random sequence to generate correlated
  voltages.
- The channels use `ReplayPseudoRandom(hash)` or `ReplayShifted(shift)` to read from the master history buffer
  with fixed phase offsets or pseudo-random mutations.

---

## 4. Output Generators

Marbles features two main random generators: the `t` generator (Gates) and the `X/Y` generator (Voltages).

### t Generator (Gates)
Located in [TGenerator](https://github.com/arachnegl/eurorack/blob/master/marbles/random/t_generator.h), it supports:
- **Complementary Bernoulli**: Coin tosses determining if T1 or T3 fires.
- **Clock Dividers**: Divides or multiplies the T2 clock.
- **Markov State Chains**: Simulates rhythmic state transitions based on past streaks.

### X/Y Generator (Voltages)
Located in [XYGenerator](https://github.com/arachnegl/eurorack/blob/master/marbles/random/x_y_generator.h), it supports:
- **Beta Distribution Sampling**: Continuous probability shaping from Gaussian to uniform to binary.
- **Steps & Smooth Quantization**: Maps continuous voltages to quantized scale divisions or slewed walks.
- **Gate Delay Alignment**: Gate outputs are delayed by 2 samples (`kGateDelay`) to align with DAC settling times.

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
