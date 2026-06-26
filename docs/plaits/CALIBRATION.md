# Plaits - Calibration and Flash Settings Guide

This document details how [Plaits](https://github.com/arachnegl/eurorack/tree/master/plaits) manages physical control calibrations and
persistent settings in non-volatile flash memory.

---

## 1. Storage Architecture

All data persistence is handled by the [Settings](https://github.com/arachnegl/eurorack/blob/master/plaits/settings.h) class. It uses the
`stmlib::ChunkStorage` utility, which abstracts flash memory writes across two separate sectors starting at:
- Sector 1 Address: `0x08004000`
- Sector 2 Address: `0x08007000`

It manages two distinct structs saved separately:

### A. Persistent Calibration Data (`PersistentData` Struct)
Stores the physical offset, scale, and normalization probe threshold for each CV ADC input channel.
- **Tag**: `0x494C4143` (`"CALI"`)
- **Key Struct**: [PersistentData](https://github.com/arachnegl/eurorack/blob/master/plaits/settings.h#L48)
- **Members**:
  - `channel_calibration_data`: Array of `ChannelCalibrationData` structures mapping directly to channels defined in
    [CvAdcChannel](https://github.com/arachnegl/eurorack/blob/master/plaits/ui.cc#L420) enum:
    - `CV_ADC_CHANNEL_MODEL`
    - `CV_ADC_CHANNEL_V_OCT`
    - `CV_ADC_CHANNEL_FM`
    - `CV_ADC_CHANNEL_HARMONICS`
    - `CV_ADC_CHANNEL_TIMBRE`
    - `CV_ADC_CHANNEL_MORPH`
    - `CV_ADC_CHANNEL_TRIGGER`
    - `CV_ADC_CHANNEL_LEVEL`

### B. Module State (`State` Struct)
Stores settings altered during module operation:
- **Tag**: `0x54415453` (`"STAT"`)
- **Key Struct**: [State](https://github.com/arachnegl/eurorack/blob/master/plaits/settings.h#L54)
- **Members**:
  - `engine`: Active synthesis model index (0 to 23).
  - `lpg_colour`: LPG resonance color setting.
  - `decay`: Main decay envelope speed.
  - `octave`: Octave offset selection.
  - `color_blind`: UI colorblind LED palette mode flag.
  - `fine_tune`: Fine tuning value.
  - `enable_alt_navigation`: Alternate model browsing navigation.

---

## 2. Transforming ADC Raw Readings

When ADC values are read inside the polling routine [Ui::Poll](https://github.com/arachnegl/eurorack/blob/master/plaits/ui.cc#L450), they are
scaled using the calibration factors:
```cpp
destination[i] = settings_->calibration_data(i).Transform(
    cv_adc_.float_value(CvAdcChannel(i)));
```
The `Transform(x)` function multiplies the raw reading `x` by the calibrated `scale` and adds the `offset`:
`x_scaled = x * scale + offset`.

---

## 3. Normalization Detection

Plaits checks if a socket has a cable plugged in by looking at the `normalization_detection_threshold`.
- During normalization checks in `Ui::DetectNormalization`, a random bit is written to the switch contact logic of the
  plug socket.
- The ADC measures the input. If the ADC reading falls below the `normalization_detection_threshold`, a switch contact
  match is recorded.
- These thresholds are initialized in [Settings::Init](https://github.com/arachnegl/eurorack/blob/master/plaits/settings.cc#L39) and
  refined via factory calibration.
