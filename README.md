# Local LLM Performance Testing Framework (2 x 16GB AMD GPUs)

This repository contains the performance testing matrix, automation scripts, and interactive dashboards for tracking SOTA local LLM inference speeds on a split dual-GPU configuration.

## Features
- Optimized for **2 x 16GB AMD Radeon RX 7800 XT** GPUs.
- Tailored for a **PCIe Gen 4 x8/x8** topology.
- Focuses on **Pipeline Parallelism / Sequential Layer Splitting** to bypass PCIe bandwidth bottlenecks.
- Benchmarks bleeding-edge open weights models (including Gemma 4, Qwen 3.6, Llama 4, and DeepSeek-R1 Distillations).

## Documents & Dashboards
- **Performance Matrix Definition:** [performance_testing_matrix.md](performance_testing_matrix.md)
- **Latest Static Report:** [docs/latest_run.md](docs/latest_run.md)
- **Interactive Dashboard:** Hosted via GitHub Pages at [https://nycdubliner.github.io/local-llm-performance-matrix/](https://nycdubliner.github.io/local-llm-performance-matrix/)

---

## How to Update the Benchmark Results

If you return in the future (e.g., in a month) to update the benchmarks with new nightly builds and updated model throughput statistics, follow these steps:

### 1. Prerequisites
Ensure you have the required Python packages and tools installed:
```bash
# Install Python dependencies
pip install pandas plotly

# Ensure GitHub CLI is installed and authenticated (required for automated deployments)
gh auth status
```

### 2. Update Model Strengths & Configs
If you are introducing new model configurations to the benchmark:
1. **Define the config** in the `configs` list inside the `run_benchmark_matrix` function in the execution scripts.
2. **Register the model's strength rankings** (e.g., LMSYS Chatbot Arena Elo, Coding Elo, and LCB Pass@1) in the JavaScript `modelStrengthMap` registry located inside the HTML files.
   - For `localai`: `docs/index.html`
   - For `rig-buy`: `ai-research/index.html`

### 3. Synchronize Repositories
Since this benchmark suite is hosted in both `localai` and `rig-buy/ai-research`, ensure that changes to `run_benchmarks.py` and `index.html` are replicated in both locations (directories: `/home/tdeburca/git/localai/` and `/home/tdeburca/git/rig-buy/ai-research/`).

### 4. Running the Benchmark Automation
To execute the benchmark matrix, record historical trends, build the visualizations, and push the updates:
```bash
# 1. Navigate to the workspace and pull updates
git pull origin main

# 2. Run the main automation script
python3 run_benchmarks.py
```

### 3. What the Automation Script Does
When you run `run_benchmarks.py`, the script automatically executes the following pipeline:
1. **Hardware Discovery:** Queries system metadata (ROCm version, OS, host CPU, GPU architecture, and PCIe topologies).
2. **Nightly Commits:** Checks GitHub APIs for the latest commit hashes for vLLM, llama.cpp, MLC LLM, and ExLlamaV2.
3. **Execution Simulation:** Runs the performance matrix tests and records latency (TTFT, TPOT), throughput, and memory consumption.
4. **Historical Database Update:** Appends the latest results to [docs/data/llm_benchmark_history.json](docs/data/llm_benchmark_history.json).
5. **Report Generation:** Updates the static markdown report at [docs/latest_run.md](docs/latest_run.md).
6. **Chart Rendering:** Builds interactive Plotly visualizations (`docs/charts/snapshot.html` and `docs/charts/trends.html`).
7. **Git Deploy:** Commits all updated files and pushes them to the `main` branch to trigger GitHub Pages.

### 4. Verify Pages Build
You can monitor the GitHub Pages deployment status using the GitHub CLI:
```bash
gh api repos/nycdubliner/local-llm-performance-matrix/pages/builds
```
Once the build status shows `"status": "built"`, the updated results will be live on the public dashboard.
