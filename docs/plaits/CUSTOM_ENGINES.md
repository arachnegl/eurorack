# Plaits - Custom Engine Development Guide

This guide describes how to implement and register a custom digital synthesis model (engine) inside the
[Plaits](https://github.com/arachnegl/eurorack/tree/master/plaits) framework.

---

## 1. Engine Interface Overview

All digital synthesizers in Plaits are classes that implement the [Engine](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/engine/engine.h)
interface:

```cpp
class Engine {
 public:
  virtual void Init(stmlib::BufferAllocator* allocator) = 0;
  virtual void Reset() = 0;
  virtual void LoadUserData(const uint8_t* user_data) = 0;
  virtual void Render(
      const EngineParameters& parameters,
      float* out,
      float* aux,
      size_t size,
      bool* already_enveloped) = 0;
  PostProcessingSettings post_processing_settings;
};
```

---

## 2. Step-by-Step Implementation

### Step A: Declare the Engine Class
Create your class header file (e.g., `plaits/dsp/engine/my_engine.h`). If you require workspace buffers (for delay
lines, tables, etc.), declare them as pointers rather than arrays.

```cpp
#ifndef PLAITS_DSP_ENGINE_MY_ENGINE_H_
#define PLAITS_DSP_ENGINE_MY_ENGINE_H_

#include "plaits/dsp/engine/engine.h"

namespace plaits {

class MyEngine : public Engine {
 public:
  MyEngine() { }
  ~MyEngine() { }

  virtual void Init(stmlib::BufferAllocator* allocator) {
    // 1. Allocate dynamic workspace buffers from the shared memory block.
    // Example: allocate 512 floats for a custom lookup table
    my_buffer_ = allocator->Allocate<float>(512);
  }

  virtual void Reset() {
    // 2. Initialize or clear state parameters.
    phase_ = 0.0f;
  }

  virtual void LoadUserData(const uint8_t* user_data) {
    // 3. Optional: Parse wavetables/custom presets if supported.
  }

  virtual void Render(
      const EngineParameters& parameters,
      float* out,
      float* aux,
      size_t size,
      bool* already_enveloped) {
    // 4. Generate audio blocks of size 'size' (typically 12 samples)
    float frequency = NoteToFrequency(parameters.note);

    for (size_t i = 0; i < size; ++i) {
      phase_ += frequency;
      if (phase_ >= 1.0f) phase_ -= 1.0f;

      // Render a simple sine wave to out, phase to aux
      out[i] = sinf(phase_ * 2.0f * M_PI) * parameters.accent;
      aux[i] = (phase_ * 2.0f - 1.0f) * parameters.accent;
    }
  }

 private:
  float* my_buffer_;
  float phase_;
};

}  // namespace plaits
#endif
```

### Step B: Allocate Memory Safely
Memory in Plaits is shared. The [BufferAllocator](https://github.com/arachnegl/eurorack/blob/master/stmlib/utils/buffer_allocator.h) passed
into `Init` points to a 16 KB scratch buffer. Calling `Allocate<T>(N)` moves the allocation pointer.
Ensure the total bytes allocated across your engine does not exceed `16384` bytes.

### Step C: Register the Engine
To activate your new engine, register it in the Voice layer:
1. Include your header in [voice.h](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.h).
2. Instantiate your class as a private member of `Voice` inside [voice.h](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.h#L205).
3. In [voice.cc](https://github.com/arachnegl/eurorack/blob/master/plaits/dsp/voice.cc#L37), register your instance inside `Voice::Init()`:
   ```cpp
   engines_.RegisterInstance(&my_engine_, false, 1.0f, 1.0f);
   ```
   * The first parameter is the address of your engine instance.
   * The second parameter `already_enveloped` dictates if the LPG is bypassed (set to `true` for drum/decay sounds).
   * The third and fourth parameters scale the default output levels for the `out` and `aux` channels.
