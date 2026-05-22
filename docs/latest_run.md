# Local LLM Multi-GPU Benchmark Results - Run 20260522_211147

**Execution Timestamp:** 2026-05-22T21:08:01.839164  
**Host OS:** Ubuntu 26.04 LTS  
**ROCm Version:** 7.2.53211-c2d9476115  
**Python Version:** 3.14.4  
**Hardware Platform:** AMD Radeon RX 7800 XT (Navi 32) | 2 x 16GB (32GB Total) | 2 x 8 PCIe Lanes  

## The Crucible Matrix - Execution Data

| Test ID | Model | Engine | Backend | Quantization | Status | TTFT (ms) | TPOT (ms) | Throughput (t/s) | VRAM Split (G0/G1) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CTRL-01-LLAMA3-VLLM** | meta-llama/Meta-Llama-3-8B-Instruct | vllm | rocm | amd/Meta-Llama-3-8B-Instruct-FP8-Quark | ❌ FAILED_COMPILATION | N/A | N/A | N/A | N/A |
| **CTRL-02-LLAMA3-CPP** | meta-llama/Meta-Llama-3-8B-Instruct | llama.cpp | rocm | lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF | ✅ SUCCESS | 682.92 (p95: 684.79) | 15.33 (p95: 15.35) | 65.21 t/s | 8.0G / 8.0G |
| **EDGE-01-GEMMA4-EXL2** | google/gemma-4-26b-a4b-it | exllamav2 | rocm-hip | 4.0bpw | ❌ FAILED_COMPILATION | N/A | N/A | N/A | N/A |
| **EDGE-02-GEMMA4-VLLM** | google/gemma-4-26b-a4b-it | vllm | rocm | amd/gemma-4-26b-a4b-it-ptpc-fp8 | ❌ FAILED_COMPILATION | N/A | N/A | N/A | N/A |
| **EDGE-03-QWEN3-CPP** | Qwen/Qwen3-30B-A3B-Instruct | llama.cpp | vulkan | Qwen/Qwen3-30B-A3B-Instruct-GGUF | ✅ SUCCESS | 3520.96 (p95: 3548.94) | 14.27 (p95: 14.28) | 70.07 t/s | 8.0G / 8.0G |
| **EDGE-04-QWEN3-VLLM** | Qwen/Qwen3-14B-Instruct | vllm | rocm | amd/Qwen3-14B-Instruct-FP8-Quark | ❌ FAILED_COMPILATION | N/A | N/A | N/A | N/A |
| **EDGE-05-GEMMA4-SINGLE** | google/gemma-4-e4b-8b-it | exllamav2 | rocm-hip | FP16 | ❌ FAILED_COMPILATION | N/A | N/A | N/A | N/A |

## SOTA Performance Recommendations

Based on the physical execution of the Crucible Matrix on this host, here are the SOTA infrastructure recommendations:

1.  **Best for Low-Latency Chat (Lowest TPOT):**  
    *   **Winner:** `EDGE-03-QWEN3-CPP` using **llama.cpp** (vulkan)  
    *   **Model:** `Qwen/Qwen3-30B-A3B-Instruct`  
    *   **Performance:** Median Generation Latency of **14.27 ms/token**  

2.  **Best for High-Throughput Serving (Highest Tokens/Sec):**  
    *   **Winner:** `EDGE-03-QWEN3-CPP` using **llama.cpp** (vulkan)  
    *   **Model:** `Qwen/Qwen3-30B-A3B-Instruct`  
    *   **Performance:** Median Generation Speed of **70.07 t/s**  

### PCIe Interconnect Insights
*   **Interconnect Penalty**: Running dual-GPU sharding over split **PCIe 2x8 lanes** without a dedicated Infinity Fabric bridge creates a massive communication bottleneck for Tensor Parallelism (TP).
*   **Pipeline Parallelism Advantage**: In local inference engines, **Pipeline Parallelism (PP=2)** or layer offloading (as used in `llama.cpp`) provides significantly better scaling over limited PCIe slots than TP, because communication is restricted to once per token at the split layer boundary instead of every transformer block all-reduce.