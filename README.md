# Local LLM Performance Testing Framework (2 x 16GB AMD GPUs)

This repository contains the performance testing matrix and configuration guidelines for benchmarking local LLM inference on a split dual-GPU configuration.

## Features
- Optimized for **2 x 16GB AMD Radeon RX 7800 XT** GPUs.
- Tailored for a **PCIe Gen 4 x8/x8** topology.
- Focuses on **Pipeline Parallelism / Sequential Layer Splitting** to bypass PCIe bandwidth bottlenecks.
- Benchmarks bleeding-edge open weights models (including Gemma 4, Qwen 3.6, Llama 4, and DeepSeek-R1 Distillations).

## Documents
- [Comprehensive Performance Testing Matrix](performance_testing_matrix.md)
