# Eurorack Modules - Documentation Process Manual

This directory contains the developer documentation portal for the [Mutable Instruments Eurorack modules](https://github.com/arachnegl/eurorack).
It is compiled and published automatically via GitHub Pages.

---

## 1. Directory Structure

* **Root Portal (`index.md`)**: The grid-based card entry point for the site.
* **Module Indexes (`index.md`)**: Main landing pages for Plaits, Rings, and Marbles.
* **Architecture Deep Dives (`ARCHITECTURE.md`)**: Hardware memory and logic mappings.
* **Build Guides (`BUILD_GUIDE.md`)**: Toolchain variables, make targets, and flashing processes.
* **DSP / Random Code Engines (`dsp/` or `random/`)**: Architectural case studies of core engines.
* **Style Overrides (`assets/css/style.scss`)**: Custom Sass containing dark-mode, glassmorphism, and button styling.

---

## 2. Link Integrity & Path Handling

On the live GitHub Pages website (`https://arachnegl.github.io/eurorack/`), only the `/docs` directory is served. 

To prevent broken links:
1. **Internal Documentation Links**: Use relative Markdown links pointing to the target `.md` files. Jekyll converts 
   these to `.html` during compilation.
2. **Source Code References**: Any link referencing C++ source files or folders outside of the `/docs` directory must 
   use absolute GitHub repository viewer URLs (`https://github.com/arachnegl/eurorack/blob/master/...` or 
   `.../tree/master/...`).
3. **Liquid/HTML Tags**: Inside raw HTML tags (like portal cards), use `.html` file extensions directly instead of 
   `.md`, as Jekyll does not parse Markdown references inside raw HTML tags.

---

## 3. Math & Diagram Rendering

 Documentation files contain LaTeX equations and Mermaid flowcharts. Because GitHub Pages does not
 render these natively, scripts are appended to the bottom of the Markdown documents:
* **KaTeX (Math)**: Injected stylesheet and defer scripts compile inline `$math$` and block `$$math$$` elements.
* **Mermaid (Flowcharts)**: The script queries `.language-mermaid` code blocks, replaces them with target divs, 
  and initializes a **Click-to-Zoom Lightbox** that overlays high-resolution vector SVGs on click.

---

## 4. Pre-commit Enforcements (Lefthook)

To guarantee that no broken links are committed:
* **Verifier Script**: [scripts/check_links.py](https://github.com/arachnegl/eurorack/blob/master/scripts/check_links.py) is a standalone Python utility that 
  scans all documentation files. It skips external URLs but verifies all local relative and absolute files on disk, 
  gracefully ignoring unpopulated submodules (`stmlib` and `stm_audio_bootloader`).
* **Lefthook Hooks**: Configured in [lefthook.yml](https://github.com/arachnegl/eurorack/blob/master/lefthook.yml) to block commits if the Python verifier 
  exits with a non-zero status.

### Manual Verification Commands:
* Run the link checker:
  ```bash
  python3 scripts/check_links.py
  ```
* Run the pre-commit hook manually:
  ```bash
  lefthook run pre-commit
  ```
