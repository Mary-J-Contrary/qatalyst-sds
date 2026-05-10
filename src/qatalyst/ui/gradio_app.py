import json
import os
from datetime import datetime

import gradio as gr

from qatalyst.apex.tick import run_qatalyst_tick


CUSTOM_CSS = """
#qatalyst-root {
    max-width: 1180px;
    margin: 0 auto;
}

.q-hero {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 28px 30px;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(2, 6, 23, 0.98));
    box-shadow: 0 18px 60px rgba(0,0,0,0.35);
}

.q-eyebrow {
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #93c5fd;
    font-size: 0.78rem;
    font-weight: 700;
}

.q-title {
    font-size: 2.35rem;
    line-height: 1.1;
    font-weight: 800;
    margin: 0.35rem 0 0.6rem 0;
}

.q-subtitle {
    font-size: 1rem;
    color: #cbd5e1;
    max-width: 880px;
}

.q-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 18px;
}

.q-card {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 14px 16px;
    background: rgba(15,23,42,0.75);
}

.q-card strong {
    color: #f8fafc;
}

.q-muted {
    color: #94a3b8;
}

.q-callout {
    border-left: 4px solid #60a5fa;
    background: rgba(96,165,250,0.10);
    padding: 12px 14px;
    border-radius: 10px;
    margin-top: 16px;
}

.q-output {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 18px;
    background: rgba(15,23,42,0.85);
}

button.primary {
    border-radius: 12px !important;
    font-weight: 800 !important;
    min-height: 48px !important;
}

@media (max-width: 800px) {
    .q-grid {
        grid-template-columns: 1fr;
    }
    .q-title {
        font-size: 1.8rem;
    }
}
"""


def simulate_tick(temp, tension):
    try:
        return run_qatalyst_tick(temp, tension)
    except Exception as e:
        return f"**System fault:** `{e}`"


def read_ledger():
    ledger_path = "cognitive_ledger.jsonl"
    if not os.path.exists(ledger_path):
        return "[]"

    with open(ledger_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    records = []
    for line in reversed(lines[-10:]):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            records.append({"raw": line.strip()})

    return json.dumps(records, indent=2)


with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "Arial", "sans-serif"],
    ),
    css=CUSTOM_CSS,
) as demo:
    with gr.Column(elem_id="qatalyst-root"):
        gr.HTML(
            """
            <section class="q-hero">
                <div class="q-eyebrow">AMD Developer Hackathon 2026 · Track 1: AI Agents</div>
                <h1 class="q-title">🛡️ QATALYST SDS</h1>
                <p class="q-subtitle">
                    A deterministic safety demonstration for autonomous AI workflows.
                    The demo shows how an agent request can be allowed under stable
                    operating conditions or blocked before execution when telemetry
                    crosses a defined safety boundary.
                </p>

                <div class="q-grid">
                    <div class="q-card">
                        <strong>1. Stable Path</strong><br>
                        <span class="q-muted">Set temperature to 50°C and tension to 0.40.
                        Expected: EXECUTED / STABLE CORE.</span>
                    </div>
                    <div class="q-card">
                        <strong>2. Safety Path</strong><br>
                        <span class="q-muted">Set temperature to 95°C and tension to 0.95.
                        Expected: ANNIHILATED / NULL SPACE.</span>
                    </div>
                    <div class="q-card">
                        <strong>3. Audit Path</strong><br>
                        <span class="q-muted">Open the ledger tab to inspect the last
                        recorded decisions.</span>
                    </div>
                </div>

                <div class="q-callout">
                    <strong>Tagline:</strong> Annihilation is not a crash — it is the vault door locking.
                </div>
            </section>
            """
        )

        with gr.Tabs():
            with gr.TabItem("Control Demo"):
                gr.Markdown(
                    "Adjust the telemetry inputs, then trigger the agent request to observe the deterministic verdict."
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Telemetry Inputs")
                        temp_slider = gr.Slider(
                            minimum=20.0,
                            maximum=100.0,
                            value=45.0,
                            step=1.0,
                            label="Thermal Load (°C)",
                        )
                        tension_slider = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.30,
                            step=0.05,
                            label="Substrate Tension",
                        )
                        run_btn = gr.Button(
                            "Trigger APEX Agent",
                            variant="primary",
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### Verdict")
                        output_display = gr.Markdown(
                            """
<div class="q-output">
System ready. Set telemetry values and trigger the agent.
</div>
"""
                        )

                run_btn.click(
                    fn=simulate_tick,
                    inputs=[temp_slider, tension_slider],
                    outputs=output_display,
                )

            with gr.TabItem("Decision Ledger"):
                gr.Markdown(
                    "Review the latest recorded state transitions from this running demo session."
                )
                refresh_btn = gr.Button("Sync Ledger", variant="secondary")
                ledger_display = gr.Code(language="json", interactive=False)

                refresh_btn.click(fn=read_ledger, inputs=[], outputs=ledger_display)
                demo.load(fn=read_ledger, inputs=[], outputs=ledger_display)


if __name__ == "__main__":
    demo.launch()
