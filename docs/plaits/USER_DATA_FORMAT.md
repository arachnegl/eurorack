# Plaits - User Data Format & Audio Transfer Protocol

This document details how custom user wavetable, speech, or configuration patch data is transferred over the audio
input and stored in the microcontroller flash memory of [Plaits](https://github.com/arachnegl/eurorack/tree/master/plaits).

---

## 1. Storage Layout in Flash

User data is written directly to the microcontroller's Flash memory using the [UserData](https://github.com/arachnegl/eurorack/blob/master/plaits/user_data.h) class:
- **Base Flash Address**: `0x08007000`
- **Total Workspace Size**: `4096` bytes (`0x1000` bytes / 4 KB)
- **Sector Alignment**: Flash page erasure occurs in `PAGE_SIZE = 2048` byte blocks (two pages are erased starting at
  `0x08007000` and `0x08007800`).

### Slot Identification Tag
Because user data overrides presets on a specific active synthesis engine, the data must be associated with the
correct engine slot index. Plaits tags the data by reserving the last two bytes of the 4096-byte workspace:
- **`data[4094]`**: Constrained to ASCII `'U'`.
- **`data[4095]`**: Constrained to ASCII `' ' + slot` (where `slot` is the target engine index, e.g. slot 13 for
  wavetable model or 15 for speech model).

---

## 2. Audio Transmission & Demodulation

User data is streamed into the module's TIMBRE signal input in the form of high-frequency audio pulses.
Processing is performed by [UserDataReceiver](https://github.com/arachnegl/eurorack/blob/master/plaits/user_data_receiver.h).

### A. Demodulation Method
The demodulator parses FSK (Frequency-Shift Keying) signal cycles:
- **Demodulator configuration**: `Demodulator<9, 5, 2>`
- **Phase transition classification**:
  - `Zero Symbol`: Short transition duration (around 2 samples).
  - `One Symbol`: Mid transition duration (around 5 samples).
  - `Pause/Sync Symbol`: Long transition duration (around 9 samples).
- An adaptive threshold filter ([AdaptiveThreshold](https://github.com/arachnegl/eurorack/blob/master/plaits/user_data_receiver.h#L37))
  removes DC offset and normalizes input volume levels to process incoming signals reliably.

### B. Packet Decoding
The FSK demodulator translates symbols into structured data packets:
1. When a packet is fully read, it is verified via CRC (Cyclic Redundancy Check).
2. On success (`PACKET_DECODER_STATE_OK`), packet bytes are copied to the staging buffer:
   `rx_buffer_ + received_` inside [UserDataReceiver::Process](https://github.com/arachnegl/eurorack/blob/master/plaits/user_data_receiver.cc#L51).
3. Once all blocks are received (`UserDataReceiver::progress() == 1.0f`), the sector is flashed using
   `UserData::Save` and the target engine's database is updated via `voice.ReloadUserData()`.
