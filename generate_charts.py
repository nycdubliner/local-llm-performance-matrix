#!/usr/bin/env python3
import os
import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Paths
WORKSPACE_DIR = "/home/tdeburca/git/localai"
HISTORY_JSON_PATH = os.path.join(WORKSPACE_DIR, "docs/data/llm_benchmark_history.json")
CHARTS_DIR = os.path.join(WORKSPACE_DIR, "docs/charts")

# Setup style tokens
DARK_BG = "#0f172a"  # Slate 900
CARD_BG = "#1e293b"  # Slate 800
TEXT_MAIN = "#f8fafc"  # Slate 50
TEXT_MUTED = "#94a3b8"  # Slate 400
BORDER_COLOR = "#334155"  # Slate 700

COLOR_MEDIAN = "#3b82f6"  # Blue 500
COLOR_P95 = "#ec4899"     # Pink 500
COLOR_TTFT = "#10b981"    # Emerald 500
COLOR_TPOT = "#f59e0b"    # Amber 500

PLOTLY_LAYOUT_DEFAULTS = dict(
    paper_bgcolor=DARK_BG,
    plot_bgcolor=DARK_BG,
    font=dict(family="Outfit, Inter, sans-serif", color=TEXT_MAIN),
    xaxis=dict(
        gridcolor=BORDER_COLOR,
        linecolor=BORDER_COLOR,
        tickfont=dict(color=TEXT_MUTED),
        title=dict(font=dict(color=TEXT_MAIN))
    ),
    yaxis=dict(
        gridcolor=BORDER_COLOR,
        linecolor=BORDER_COLOR,
        tickfont=dict(color=TEXT_MUTED),
        title=dict(font=dict(color=TEXT_MAIN))
    ),
    legend=dict(
        bgcolor=CARD_BG,
        bordercolor=BORDER_COLOR,
        borderwidth=1,
        font=dict(color=TEXT_MAIN)
    ),
    margin=dict(l=60, r=40, t=80, b=60)
)

def log(msg):
    print(f"[Chart Generator] {msg}", flush=True)

def load_history():
    if not os.path.exists(HISTORY_JSON_PATH):
        log(f"Warning: History file not found at {HISTORY_JSON_PATH}. Creating an empty history dataset for demo generation.")
        return []
    try:
        with open(HISTORY_JSON_PATH) as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        log(f"Error reading history: {e}")
        return []

def generate_snapshot_chart(latest_run):
    if not latest_run:
        log("No data available for snapshot chart.")
        return
        
    results = latest_run.get("results", [])
    success_results = [r for r in results if r.get("status") == "SUCCESS"]
    
    if not success_results:
        log("No successful runs to snapshot. Generating fallback snapshot display.")
        # Create empty placeholder figure
        fig = go.Figure()
        fig.add_annotation(
            text="No successful benchmarks executed yet.<br>Compile and run benchmarks to view the snapshot.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=TEXT_MUTED)
        )
        fig.update_layout(title="Crucible Matrix - Latest Run Snapshot", **PLOTLY_LAYOUT_DEFAULTS)
        fig.write_html(os.path.join(CHARTS_DIR, "snapshot.html"))
        return

    test_ids = [r["test_id"] for r in success_results]
    engines = [r["engine"] for r in success_results]
    quants = [r["quantization"] for r in success_results]
    
    ttft_median = [r["metrics"]["ttft_ms_median"] for r in success_results]
    ttft_p95 = [r["metrics"]["ttft_ms_p95"] for r in success_results]
    tpot_median = [r["metrics"]["tpot_ms_median"] for r in success_results]
    tpot_p95 = [r["metrics"]["tpot_ms_p95"] for r in success_results]
    
    # Custom hover text
    hover_ttft = [
        f"<b>Test ID:</b> {t_id}<br><b>Engine:</b> {eng}<br><b>Quantization:</b> {q}<br><b>TTFT (Median):</b> {med} ms<br><b>TTFT (p95):</b> {p95} ms"
        for t_id, eng, q, med, p95 in zip(test_ids, engines, quants, ttft_median, ttft_p95)
    ]
    
    hover_tpot = [
        f"<b>Test ID:</b> {t_id}<br><b>Engine:</b> {eng}<br><b>Quantization:</b> {q}<br><b>TPOT (Median):</b> {med} ms<br><b>TPOT (p95):</b> {p95} ms"
        for t_id, eng, q, med, p95 in zip(test_ids, engines, quants, tpot_median, tpot_p95)
    ]

    # Subplots side-by-side
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Time to First Token (TTFT)", "Time Per Output Token (TPOT)"))
    
    # TTFT Median & p95
    fig.add_trace(
        go.Bar(
            x=test_ids, y=ttft_median,
            name="TTFT Median",
            marker_color=COLOR_MEDIAN,
            hovertext=hover_ttft,
            hoverinfo="text"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=test_ids, y=ttft_p95,
            name="TTFT p95",
            marker_color=COLOR_P95,
            hovertext=hover_ttft,
            hoverinfo="text",
            opacity=0.7
        ),
        row=1, col=1
    )
    
    # TPOT Median & p95
    fig.add_trace(
        go.Bar(
            x=test_ids, y=tpot_median,
            name="TPOT Median",
            marker_color=COLOR_TTFT,
            hovertext=hover_tpot,
            hoverinfo="text"
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(
            x=test_ids, y=tpot_p95,
            name="TPOT p95",
            marker_color=COLOR_TPOT,
            hovertext=hover_tpot,
            hoverinfo="text",
            opacity=0.7
        ),
        row=1, col=2
    )

    # Layout styling
    layout = PLOTLY_LAYOUT_DEFAULTS.copy()
    layout.update(
        title={
            "text": "Crucible Matrix - Performance Snapshot (Lower is Better)",
            "x": 0.5, "xanchor": "center", "y": 0.95
        },
        barmode="group",
        height=550,
        showlegend=True,
    )
    fig.update_layout(layout)
    
    # Label Y axes
    fig.update_yaxes(title_text="Latency (ms)", row=1, col=1)
    fig.update_yaxes(title_text="Latency (ms/token)", row=1, col=2)
    
    # Update title styling of subplots
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=14, color=TEXT_MAIN)
        
    os.makedirs(CHARTS_DIR, exist_ok=True)
    fig.write_html(os.path.join(CHARTS_DIR, "snapshot.html"))
    log("Saved snapshot chart to docs/charts/snapshot.html")

def generate_trends_chart(history):
    if not history:
        log("No data available for longitudinal trends chart.")
        return
        
    # We want to track Control Models over time: CTRL-01-LLAMA3-VLLM and CTRL-02-LLAMA3-CPP
    control_ids = ["CTRL-01-LLAMA3-VLLM", "CTRL-02-LLAMA3-CPP"]
    
    # Extract timeseries data
    runs_sorted = sorted(history, key=lambda x: x.get("timestamp", ""))
    
    fig = go.Figure()
    
    for ctrl_id in control_ids:
        dates = []
        throughputs = []
        commits = []
        hw_configs = []
        
        for run in runs_sorted:
            run_date = run.get("timestamp", "Unknown Date").split("T")[0]
            hw = run.get("metadata", {}).get("gpu_topology", "Unknown GPU Topology")
            results = run.get("results", [])
            
            # Find the result matching ctrl_id
            for res in results:
                if res["test_id"] == ctrl_id and res["status"] == "SUCCESS":
                    dates.append(run_date)
                    tps = res["metrics"]["throughput_tps_median"]
                    throughputs.append(tps)
                    commits.append(res.get("git_commit", "unknown"))
                    hw_configs.append(hw)
                    break
        
        if dates:
            # Add line trace for this control
            hover_text = [
                f"<b>Date:</b> {d}<br><b>Throughput:</b> {tps} t/s<br><b>Git Commit:</b> {git}<br><b>Hardware:</b> {hw}"
                for d, tps, git, hw in zip(dates, throughputs, commits, hw_configs)
            ]
            
            fig.add_trace(
                go.Scatter(
                    x=dates, y=throughputs,
                    mode="lines+markers",
                    name=ctrl_id,
                    line=dict(width=3),
                    marker=dict(size=8),
                    hovertext=hover_text,
                    hoverinfo="text"
                )
            )
            
    if not fig.data:
        log("No successful control runs found in history to trend. Generating fallback trends display.")
        fig.add_annotation(
            text="No successful control runs to track trend.<br>Check compiler logs or run baseline control benchmarks.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=TEXT_MUTED)
        )
        fig.update_layout(title="Crucible Matrix - Control Models Longitudinal Performance Trend", **PLOTLY_LAYOUT_DEFAULTS)
        fig.write_html(os.path.join(CHARTS_DIR, "trends.html"))
        return

    # Update layout
    layout = PLOTLY_LAYOUT_DEFAULTS.copy()
    layout.update(
        title={
            "text": "Control Models Longitudinal Performance Trend (Higher is Better)",
            "x": 0.5, "xanchor": "center", "y": 0.95
        },
        height=550,
        showlegend=True,
    )
    fig.update_layout(layout)
    fig.update_yaxes(title_text="Generation Throughput (Tokens/Second)")
    fig.update_xaxes(title_text="Execution Date")
    
    os.makedirs(CHARTS_DIR, exist_ok=True)
    fig.write_html(os.path.join(CHARTS_DIR, "trends.html"))
    log("Saved trends chart to docs/charts/trends.html")

def main():
    log("Starting visualization engine...")
    history = load_history()
    
    latest_run = history[-1] if history else None
    generate_snapshot_chart(latest_run)
    generate_trends_chart(history)
    log("Visualizations updated successfully.")

if __name__ == "__main__":
    main()
