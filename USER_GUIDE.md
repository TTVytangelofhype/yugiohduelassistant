# Windows User Guide — NEXUS Duel AI

NEXUS Duel AI is a **manual Yu-Gi-Oh! Master Duel study assistant**. It is intended for reviewing duels and planning lines in situations where third-party assistance is allowed. It does **not** control the game, access game memory, monitor matches in the background or guarantee legal moves.

## 1. Download and install
1. Open [the repository](https://github.com/TTVytangelofhype/yugiohduelassistant).
2. Select **Code → Download ZIP** and extract the ZIP to a normal Windows folder (for example, Documents\NEXUS-Duel-AI). Do not run scripts inside the compressed ZIP.
3. Install [Python 3.11 or newer](https://www.python.org/downloads/windows/); tick **Add python.exe to PATH** if offered.
4. Double-click **install.bat**. It installs the Python Pillow dependency.
5. Double-click **run.bat** to open the desktop app. If it fails, try `py app.py` from Command Prompt inside the extracted folder.

## 2. Optional local AI (free; no API credentials)
1. Install [Ollama for Windows](https://ollama.com/download/windows).
2. Open Command Prompt and type `ollama --version` to confirm installation.
3. Download an image-capable model: `ollama pull gemma3:4b`. A higher-end 16 GB VRAM PC can try `ollama pull gemma3:12b`.
4. Ensure Ollama is running. From Command Prompt, `ollama list` shows your installed models.
5. In NEXUS Duel AI, set **Ollama model** to exactly the downloaded name (e.g. `gemma3:4b`).
6. Use **Local AI Analysis** with a PNG/JPEG screenshot. Ollama runs on localhost; no paid cloud API key is required.

Note: Downloads need internet and consume disk space. Image interpretation can misread small card text.

## 3. Analyse a duel for study
1. Capture a screenshot of the board with **Win + Shift + S** (or save a PNG/JPEG screenshot).
2. Open the **Board Study** tab.
3. Fill in all **known** card names: hand, field, graveyard, accessible extra-deck cards and opponent's visible/revealed cards. Do not invent hidden cards.
4. Select the correct phase.
5. Choose **Paste Screenshot** (after copying an image) or **Load Screenshot** (saved file).
6. Click **Offline Checklist** for rules reminders that require no AI, or **Local AI Analysis** for tentative candidate plays.
7. Verify each proposed play against card texts, once-per-turn conditions, summon restrictions, chain timing, hidden-information uncertainty and game rules.

## 4. Add any deck (Blue-Eyes, Branded, Snake-Eye, custom, etc.)
1. Go to **Deck Manager**.
2. Give the deck a name.
3. For the Main, Extra and Side tabs, put one card on each line: `Blue-Eyes White Dragon | 3`. Quantity defaults to 1 if you omit `| number`.
4. Press **Check Counts** to see basic zone totals; this is not a banlist or card legality check.
5. Press **Export JSON** to save your deck; later choose **Import JSON** to restore it.

JSON format:
```json
{
  "name": "My Deck",
  "main": {"Blue-Eyes White Dragon": 3},
  "extra": {"Blue-Eyes Ultimate Dragon": 1},
  "side": {}
}
```

Master Duel itself does not use side decks; the side field is for general list compatibility.

## 5. Damage calculator
Open **Damage Calculator**, enter your attacking monster's ATK and the opposing monster's ATK or DEF, choose the opponent's position and select **Calculate**. This is a basic calculator; it does not simulate every battle effect, damage modifier, piercing effect, immunity or special case.

## 6. Hardware and model suggestions

These are **rough, unbenchmarked starting points**, not guaranteed compatibility:

| GPU | Entry recommendation | Better-option guidance |
| --- | --- | --- |
| NVIDIA GeForce RTX | 6–8 GB VRAM and 16 GB system RAM, try `gemma3:4b` | 16 GB VRAM and 32 GB RAM, try `gemma3:12b` |
| AMD Radeon RX | 8 GB VRAM and 16 GB RAM, try `gemma3:4b` if GPU support works | 16 GB VRAM and 32 GB RAM, try `gemma3:12b` |
| Intel Arc | 8 GB VRAM and 16 GB RAM, try `gemma3:4b` if Vulkan works | 16 GB VRAM and 32 GB RAM, try `gemma3:12b` |
| CPU only / integrated graphics | Manual features: 8 GB RAM | Local vision inference may work with 16–32 GB RAM but can be much slower |

The reference developer PC is **NVIDIA GeForce RTX 5060 Ti (16 GB VRAM), 64 GB system RAM**. VRAM, quantization and model context size matter more than GPU brand for choosing a model. CPU-only mode is a fallback, not a performance promise.

### AMD and Intel acceleration
Ollama supports AMD GPUs through supported ROCm configurations and broader hardware through Vulkan. Recent Ollama releases also support Vulkan on Intel graphics. **Not every AMD or Intel model/driver combination is guaranteed** to accelerate; install current GPU drivers and current Ollama, check [Ollama GPU compatibility](https://docs.ollama.com/gpu), and test with `ollama ps` while a model is responding. The `PROCESSOR` column identifies GPU/CPU use. If not accelerated, it may fall back to CPU. Do not assume your dedicated GPU is being used simply because the app launches.

Official references: [Ollama Windows](https://docs.ollama.com/windows), [Ollama GPU support](https://docs.ollama.com/gpu), [Ollama June 2026 Vulkan update](https://ollama.com/blog/improved-performance-and-model-support-with-gguf).

## 7. Troubleshooting

**`py` or Python not recognised:** install Python with PATH/launcher enabled; reopen Command Prompt. Try `python app.py` if the `py` launcher is unavailable.

**`ollama` command not recognised:** finish the Ollama install, reopen Command Prompt and try again.

**Cannot connect to Ollama:** launch Ollama, confirm `ollama list` works, and ensure local port 11434 is not blocked.

**Model not found:** run `ollama pull gemma3:4b` and check the model field matches `ollama list`.

**Slow image analysis / high RAM use:** try `gemma3:4b`, close GPU-heavy apps, check `ollama ps`, and reduce the screenshot size if needed.

**Clipboard paste doesn't work:** save the screenshot as PNG and use **Load Screenshot**.

**Wrong cards detected:** type exact card names in the board fields, use a clearer screenshot, and always verify the result against the actual card text.

## Fair play and privacy
No login or API token is needed. Screenshots are sent only to the locally configured Ollama instance (`127.0.0.1:11434`) by this project. Treat all AI output as potentially incorrect. Follow the game publisher's rules; do not use the project for unauthorized competitive advantage.
