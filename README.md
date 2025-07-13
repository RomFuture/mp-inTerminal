# Terminal Beats

> A minimalist MP3‑player that turns your Windows terminal into an ASCII jukebox.

<p align="center">
  <img src="https://github.com/RomFuture/mp-inTerminal/releases/download/ReadmeTag/0713.gif" width="640"/>
</p>

---

## ✨ Features

| | |
|---|---|
| 🎛 **ASCII interface** | Retro‑style logo, playlist pane and bar‑graph visualizer rendered right in the terminal. |
| ⏯ **Essential controls** | **Next ▶️** · **Stop ⏹** · **Previous ⏮** · **Exit ❌** — all keyboard‑driven. |
| 📜 **Now‑playing info** | Displays the current file name plus elapsed / remaining time. |
| 🗂 **Folder memory** | Remembers the music directory you chose on first launch. |

---

## 🚀 Installation

1. **Download the executable**  
   Grab the latest [`TerminalBeats.exe`](https://github.com/RomFuture/mp-inTerminal/releases/tag/ReadmeTag/TerminalBeats.exe) from the **Releases** page.

2. **Run it**  
   Double‑click the file — no additional dependencies are required.

3. **Pick your music folder**  
   On first launch you’ll be prompted to select a directory containing your `.mp3` files.  
   (You can change this later by editing `config.json` or relaunching with a new path.)

4. **Enjoy the beats!**  
   Use the on‑screen keys to skip tracks, stop playback, or exit.

---

## 📝 Configuration
A tiny `config.json` lives next to the executable and stores:

```json
{
  "music_dir": "C:/Users/You/Music",
}
```

Feel free to tweak it manually.
