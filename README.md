<div align="center">  
  
# CSZ Tools Plus – Cave Story PSP Modding Suite
---

<img width="270" height="272" alt="imagecsz" src="https://github.com/user-attachments/assets/a6f7c036-42ec-4bb3-88d4-313fce86f20d" />

---
[![GitHub release](https://img.shields.io/github/v/release/edwarly999plus/CSZ-Tools-Plus)](https://github.com/edwarly999plus/CSZ-Tools-Plus/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete graphical tool to **extract, modify, and repack** the game data of **Cave Story for PSP**. Work with `data.csz` archives, edit `EBOOT.PBP`, change the game title, apply patches, and restore original files – all in one place.

## CSZ Tools Plus GUI
<img width="709" height="641" alt="image" src="https://github.com/user-attachments/assets/b19303fe-47c1-401f-84ab-e6309ee3efc9" />

<div align="left">
  
## ✨ Features

- **Extract `data.csz`** – Full (with (1)/(2) suffixes), English only, or Japanese only.
- **Compress** – Turn a `data` folder back into a `data.csz` archive.
- **Restore original `data.csz`** – From a ZIP‑file backup.
- **Apply patch/mod** – Replace the `data.csz` inside the PSP executable (`EBOOT.PBP`) with a modified one.
- **Extract `EBOOT.PBP`** – Get all internal sections (PARAM.SFO, ICON0.PNG, DATA.PSP, …) as individual files.
- **Compress `EBOOT.PBP`** – Rebuild a PSP executable from an extracted folder.
- **Edit `PARAM.SFO`** – Quickly change the game title that appears on the PSP XMB.
- **Restore original `EBOOT.PBP`** – From a ZIP‑file backup (CRC‑checked).
- **Multi‑language UI** – Automatically detects your system language (English, Spanish, Japanese) – you can also switch manually.
- **Progress bar & read‑only log** – With copy and clear buttons.
- **Built‑in FAQ** – Answers to common questions.

## 📦 Requirements

- **Windows** (the tool is primarily designed for Windows; Python version works on any OS)
- **Python 3.6+** (if running from source)
- **No extra libraries** – only the Python standard library and `tkinter` (usually pre‑installed).

## 🚀 Download & Run

### Option 1: Use the pre‑compiled executable (recommended)

1. Go to the [Releases](https://github.com/edwarly999plus/CSZ-Tools-Plus/releases) page.
2. Download `CSZ Tools+ Windows.zip`.
3. Extract it in an empty folder.
4. Double‑click to run – no installation required.

### Option 2: Run from Python source

```bash
git clone https://github.com/edwarly999plus/CSZ-Tools-Plus.git
cd CSZ-Tools-Plus
python main.py
```

## 🧰 How to Use

### 📁 Working with data.csz
Utiliza estas funciones para manipular el contenedor principal de archivos del juego.

| Button | Action |
| :--- | :--- |
| **Extract All** | Extracts every file (both languages) and adds (1)/(2) suffixes to distinguish English and Japanese. |
| **Extract English** | Extracts only neutral + English files (no suffixes). |
| **Extract Japanese** | Extracts only neutral + Japanese files (no suffixes). |
| **Compress** | Takes the `data` folder (created by any extractor) and builds a new `data.csz`. |
| **Restore original data.csz** | Replaces the current `data.csz` with the one from `data_original.zip`. |

---

### 🛠️ Typical Workflow for English‑only Mods
Sigue estos pasos para crear una traducción o mod en inglés de manera efectiva:

1. **Extract English:** Extrae los archivos base desde un `data.csz` limpio.
2. **Modify:** Edita los archivos dentro de la carpeta `/data` generada.
3. **Compress:** Genera el nuevo `data.csz` (Tamaño aproximado: ~1.36 MB).
4. **Apply Patch:** Usa la función *Apply Patch/Mod* apuntando a tu `EBOOT.PBP` y selecciona tu nuevo `data.csz`.

---

## ❓ Frequently Asked Questions

<details> <summary>1. What can I do with this tool?</summary> Extract, mod, and repack data.csz and EBOOT.PBP for Cave Story PSP. Apply patches, edit the game title, restore backups. </details><details> <summary>2. How do I extract the game files?</summary> Use "Extract All" (adds (1)/(2) suffixes), "Extract English", or "Extract Japanese". A `data` folder is created. </details><details> <summary>3. How do I repack after editing?</summary> Press **Compress** – a new `data.csz` will be created from the `data` folder. </details><details> <summary>4. The game crashes / black screen after repacking</summary> Make sure you extracted the correct language (e.g., English‑only for an English mod). If you used "Extract All", the resulting `data.csz` contains both languages – that is the safest for the original game. </details><details> <summary>5. How do I apply a mod (patch) to the PSP game?</summary> Use **Apply Patch/Mod to Cave Story PSP**. - First, select your `EBOOT.PBP` (it will be auto‑selected if in the same folder). - Then, select the **modified** `data.csz` (the one you just compressed). - The tool replaces the `data.csz` inside the EBOOT folder. </details><details> <summary>6. Why do I get "The process cannot access the file"?</summary> This happens when the file you are trying to overwrite is being used by another program. Common causes: the game/emulator (PPSSPP) is still running, File Explorer is previewing the file, or your antivirus scans it. Also: **do not try to patch using the same `data.csz` file as source and destination** – always use a different file. </details><details> <summary>7. How do I change the game name on the PSP XMB?</summary> - Extract `EBOOT.PBP` (use **Extract EBOOT.PBP**). - Click **Edit PARAM.SFO**, change the title, save. - Click **Compress EBOOT.PBP** to rebuild the modified executable. </details><details> <summary>8. Can I restore the original EBOOT?</summary> Yes, with **Restore Original EBOOT.PBP**. Place an `original_eboot.zip` (containing the original `EBOOT.PBP`) in the tool’s folder. The tool will verify the CRC32 before restoring. </details><details> <summary>9. Do extracted files keep the (1) and (2) suffixes?</summary> Only **Extract All** adds the suffixes (for both languages). **Extract English** and **Extract Japanese** do not – they give you clean filenames for direct editing. </details><details> <summary>10. Does the tool modify original files without asking?</summary> No. Every operation that overwrites something requires a confirmation dialog. Always make backups before experimenting. </details>

## 🔧 Troubleshooting

- Missing DLLs / Tkinter – Use a full Python installation (not the embedded version).

- Antivirus false positive – The tool is open source and safe. Add the executable to your antivirus exception list if needed.

## 📝 Credits

- Original CSZ tools code by andwhyisit/ufo_z

- Python port and additional features by EdwarlyGamer999+

- Cave Story PSP by ufo_z

## 📝 More Info

- Thread – [CSZ Tools on Cave Story Forum](https://forum.cavestory.one/threads/csz-tools.18220/)

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

## Happy modding! 🎮
If you encounter any issues, open an issue on GitHub or post in the forum thread.
