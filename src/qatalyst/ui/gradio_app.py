import gradio as gr
import os
from qatalyst.apex.tick import run_qatalyst_tick


def simulate_tick(temp, tension):
    try:
        return run_qatalyst_tick(temp, tension)
    except Exception as e:
        return f"**[!] SYSTEM FAULT:** {e}"


def read_ledger():
    ledger_path = "cognitive_ledger.jsonl"
    if not os.path.exists(ledger_path):
        return "[]"
    with open(ledger_path, "r") as f:
        lines = f.readlines()
    # Format the last 10 ticks, reversed so the newest is at the top
    formatted = (
        "[\n  " + ",\n  ".join([l.strip() for l in reversed(lines[-10:])]) + "\n]"
    )
    return formatted


with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🛡️ QATALYST SDS: Apex Command Center")

    with gr.Tabs():
        with gr.TabItem("Sovereign Vault Control"):
            gr.Markdown(
                "Adjust telemetry to observe Z3 Formal Verification guardrails in real-time."
            )
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🎛️ Telemetry Inputs")
                    temp_slider = gr.Slider(
                        0.0, 100.0, 45.0, step=1.0, label="Substrate Temperature (°C)"
                    )
                    tension_slider = gr.Slider(
                        0.0, 1.0, 0.3, step=0.05, label="Network Tension (E)"
                    )
                    run_btn = gr.Button("Execute Apex Tick", variant="primary")
                with gr.Column():
                    gr.Markdown("### 📡 Tick Output")
                    output_display = gr.Markdown(
                        "> System Ready. Awaiting telemetry..."
                    )

            run_btn.click(
                fn=simulate_tick,
                inputs=[temp_slider, tension_slider],
                outputs=output_display,
            )

        with gr.TabItem("Cognitive Ledger Audit"):
            gr.Markdown(
                "Immutable record of system state transitions (Showing last 10 events)."
            )
            refresh_btn = gr.Button("🔄 Sync Ledger", variant="secondary")
            ledger_display = gr.Code(language="json", interactive=False)

            # Update ledger when button is clicked OR when the UI first loads
            refresh_btn.click(fn=read_ledger, inputs=[], outputs=ledger_display)
            demo.load(fn=read_ledger, inputs=[], outputs=ledger_display)

if __name__ == "__main__":
    print("[*] Launching Upgraded Command Center...")
    demo.launch(server_name="127.0.0.1", server_port=7860, quiet=True)
