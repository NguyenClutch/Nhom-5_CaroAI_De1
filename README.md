# Caro_AI

The Caro AI game with a strong heuristic AI built on minimax and alpha-beta pruning. The codebase has grown from a compact student project into a version with deeper search, optional native acceleration, benchmark tooling, and configurable difficulty.

---

## For people who just want to play


## Project layout

| Path | Role |
|------|------|
| `main.py` | Thin entry: run `python main.py` from the repo root. |
| `caro_ai/` | Python package containing the board, AI, CLI app, and support modules. |
| `caro_ai/app.py` | Command-line game loop for human-vs-AI, developer, and benchmark modes. |
| `caro_ai/ai/` | Minimax and Alpha-Beta search implementation. |
| `caro_ai/game/` | Board rules and game-state helpers. |
| `caro_ai/ui/` | UI widget placeholders for the refactored layout. |
| `caro_ai/modes.py` | `GameMode` enum (`NORMAL`, `DEVELOPER`, `BENCHMARK`). |
| `config/` | External JSON settings (`dev_mode.json`, `benchmark_config.json`). |
| `assets/` | Images and icons for the UI. |
| `benchmarks/results/` | Benchmark outputs (summary and board `.txt` files). |
| `extensions/` | Cython sources (`*.pyx`) for optional acceleration. |
| `notebooks/` | Analysis notebooks such as `benchmark_analysis.ipynb`. |
| `docs/` | Extra notes and static pages. |
| `dist/` | Packaged executables for Windows and Linux. |

---

## Version note

### Original baseline (early README / classic behavior)

- Core AI: **minimax** with **alpha-beta pruning**.
- Run the game with **Python** and **Pygame** after installing dependencies from `requirements.txt`.
- Entry point: `main.py`.
- Packaged release was described as a downloadable archive; development setup used `pip install pygame` (and optional Tk on Linux for some environments).

### Current version (what is new)

This repository is now organized as a package under `caro_ai/`, with `main.py` acting as the only root-level entry point.

Search and evaluation:

- **Move ordering** so alpha-beta cuts branches earlier.
- **Transposition table** with **Zobrist hashing** to reuse scores for repeated positions.
- **Beam search / forward pruning** (configurable beam widths).
- **Incremental evaluation** to update heuristic locally instead of rescanning the board.
- **Iterative deepening** with reuse of prior principal variation for ordering.
- **Threat-oriented search** (VCF-style tactical layer) and related options, configurable per agent.
- **Time budget per move** (`move_time_budget_sec`); search can stop between completed depths and keep the last fully finished result.
- **Adaptive depth / beam** by game stage where enabled.

Performance:

- Optional **Cython extensions**: heuristic acceleration (`agent_accel`) and a compiled minimax path (`search_accel`). Build with `setup_cython.py` (see below).
- Optional **lazy SMP** (parallel root helpers) where configured.
- **AI move computation in a worker process** so the Pygame loop stays responsive while the agent thinks.

Gameplay and UI:

- **Resizable window** with layout that scales the board and controls.
- **Single turn timer** for the active side; timer stops when the game ends.
- **Player vs AI** and **AI vs AI (developer mode)** with Start / Pause (dev and benchmark), Undo, Replay.
- **Player vs AI difficulty** is no longer “depth only”: **Easy / Medium / Hard** map to full **preset configs** (`PLAYER_VS_AI_PRESETS` near the top of `caro_ai/app.py`: depth plus all relevant `Agent` options).

Benchmarking and analysis:

- **Benchmark mode** (`python main.py --benchmark`) runs scheduled matchups from **`config/benchmark_config.json`** (merged over inline `benchmark_setup` defaults in `caro_ai/app.py`).
- Results append incrementally under **`benchmarks/results/`**:
  - `benchmark_results_summary.txt` — structured fields per game.
  - `benchmark_results_boards.txt` — ASCII board, agents, outcome per side.
- **Resume**: on a fresh program start, benchmark mode can advance to the **next** matchup/game based on the last valid `match_id` in the summary file (entries that do not match the current config are ignored).
- **`notebooks/benchmark_analysis.ipynb`**: parse the text outputs and plot win rates, timings, Elo-style summaries, heatmaps, etc.

---

## How to use (current project)

### 1. Choose the mode on the command line

```text
python main.py               # Pygame UI, human vs AI (default)
python main.py --dev         # Console AI vs AI; uses the developer mode path
python main.py --benchmark   # Benchmark runner; reads config/benchmark_config.json
```

Options:

- `--depth N` — search depth used by the console developer mode.

`--dev` and `--benchmark` are mutually exclusive. Run `python main.py -h` for full help.

**Human vs AI:** run `python main.py` and play on the Pygame board. Click a cell to place `X`; the AI responds as `O`.

### 2. Human vs AI game loop

The current Pygame UI is intentionally minimal. It shows a 9x9 board, accepts mouse clicks for `X`, and uses Alpha-Beta for the AI response. This keeps the layout clean while preserving the core gameplay path.

### 3. Developer mode (AI vs AI)

Run `python main.py --dev` for a console AI-vs-AI match. Use `--depth` to control search depth.

The current refactor keeps this path simple and deterministic; it is a direct smoke-test route for the search code.

### 4. Benchmark mode

Run `python main.py --benchmark` to execute the benchmark driver.

- Edit **`config/benchmark_config.json`**. The file can define a `boards` array with board layouts and depths, plus `matchups` metadata for future extension.
- Benchmark output is printed to the terminal for now.
- Results are designed to be easy to redirect or capture into the `benchmarks/results/` folder later.

### 5. Analysis notebook

Open **`notebooks/benchmark_analysis.ipynb`** in Jupyter, ensure the summary and boards text files are present under `benchmarks/results/`, and run the cells to regenerate tables and plots.

### 6. Dependency setup

Install dependencies with:

```text
pip install -r requirements.txt
```

The current runtime expects `numpy` and `pygame`.

---