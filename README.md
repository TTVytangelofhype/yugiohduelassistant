# NEXUS Duel AI — All Decks Edition

Free Windows Yu-Gi-Oh! Master Duel **study assistant** with support for arbitrary decks, manual board-state entry, basic damage calculations and optional local screenshot analysis through [Ollama](https://ollama.com/download). **No paid API key needed.**

## Installation
1. Install Python 3.11+ and select “Add Python to PATH”.
2. Download the repository and run `install.bat`, then `run.bat`.
3. Optional image analysis: install Ollama and run `ollama pull gemma3:4b`.
4. Users with 16 GB VRAM can try `ollama pull gemma3:12b` and select `gemma3:12b` in the app.
5. Paste a screenshot taken using Win+Shift+S, or browse to a PNG/JPEG screenshot. Enter known cards and phase for context.

## Estimated system requirements

| Mode | GPU | RAM |
| --- | --- | --- |
| Manual offline study | Integrated graphics | 8 GB |
| Entry screenshot AI — Gemma 3 4B | ~6–8 GB VRAM or slower CPU-only | 16 GB |
| Recommended screenshot AI — Gemma 3 12B | NVIDIA with 16 GB VRAM | 32 GB |
| Developer reference PC | **NVIDIA RTX 5060 Ti 16 GB VRAM** | **64 GB** |

Estimates only, **not benchmarked**; quantization, context, operating system and other GPU usage alter requirements. Ollama model downloads need internet; subsequent local queries do not need a cloud API key.

## Capabilities and limitations
- Deck-agnostic: import/export deck JSON with `name`, `main`, `extra`, and optional `side` objects mapping card names to quantities.
- Conservative offline checklist and simple battle damage calculations.
- Local image AI provides **suggestions, not verified legal moves**. Small card text may be misread; it has no official effect database or current banlist.
- No game injection, memory reading, automatic clicks or background capture.
- For **post-duel analysis or otherwise permitted study only**. Check the game’s competitive rules before using any third-party assistance.
- Independent fan project. Not endorsed by Konami.

## Test
`python -m unittest discover -s tests -v`
