#!/usr/bin/env python
import sys
import warnings
import gradio as gr
import time
from PyPDF2 import PdfReader
import docx2txt

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

sys.path.append("src/legal_mate_ai")
from run_crew import summarize

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# Gradio UI Development
def extract_text_from_files(files):
    if not files:
        return ""

    all_text = ""

    for file in files:
        file_path = file.name
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                all_text += page.extract_text() or ""
        elif file_path.endswith(".docx"):
            all_text += docx2txt.process(file_path)
    
    return all_text.strip()

def validate_and_store(text_input, file_input):
    if not text_input and not file_input:
        raise gr.Error("⚠️ Please enter contract text or upload a file.")

    final_text = text_input.strip()
    # if not final_text and file_input:
    #     final_text = extract_text_from_files(file_input)
    if file_input:
        final_text += '\n' + extract_text_from_files(file_input)

    if not final_text:
        raise gr.Error("⚠️ The uploaded file appears empty or unsupported.")

    return (
        final_text, 
        gr.update(visible=True),                 # spinner
        gr.update(visible=False),                # output_md
        gr.update(interactive=False),            # submit_btn (disable)
        gr.update(interactive=False)             # clear_btn (disable)
    )

def summarize_contract(contract_text):
    if not contract_text.strip():
        # No action if input is empty (after clear)
        return (
            gr.update(visible=False),     # output_md
            gr.update(visible=False),     # spinner
            gr.update(interactive=True),  # submit_btn
            gr.update(interactive=True)   # clear_btn
        )

    try:
        result = summarize(contract_text)
        return (
            gr.update(value=result, visible=True),  # output_md
            gr.update(visible=False),               # spinner
            gr.update(interactive=True),            # submit_btn
            gr.update(interactive=True)             # clear_btn
        )
    except Exception as e:
        error_msg = f"❌ Contract Summarization failed: {e}"
        return (
            gr.update(value=error_msg, visible=True),  # show in output_md as error text
            gr.update(visible=False),
            gr.update(interactive=True),
            gr.update(interactive=True)
        )
    

def clear_form():
    return "", None, "", gr.update(visible=False), gr.update(value="", visible=False), gr.update(value="", visible=False)

with gr.Blocks(title="LegalMateAI") as demo:
    gr.Markdown("# 🤖 LegalMateAI\nYour Contract Review Assistant")

    with gr.Row():
        text_input = gr.Textbox(label="📜 Contract Text", lines=8, placeholder="Enter or Paste your contract text here...")
        file_input = gr.File(label="📁 Upload Contract Files(PDF/DOC/DOCX)", file_types=[".pdf", '.doc', ".docx"], file_count="multiple")

    with gr.Row():
        submit_btn = gr.Button("🔍 Analyze", variant="primary")
        clear_btn = gr.Button("🧹 Clear")

    job_text_state = gr.State()

    spinner = gr.HTML("""
        <div id="loader" style="display: flex; justify-content: center; margin: 20px;">
            <div style="border: 6px solid #f3f3f3; border-top: 6px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite;"></div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    """, visible=False)

    output_md = gr.Markdown("", visible=False)

    # Step 1: Validate input and set state
    submit_btn.click(
        fn=validate_and_store,
        inputs=[text_input, file_input],
        outputs=[job_text_state, spinner, output_md, submit_btn, clear_btn]
    )

    # Step 2: Trigger generate only if state is set
    job_text_state.change(
        fn=summarize_contract,
        inputs=[job_text_state],
        outputs=[output_md, spinner, submit_btn, clear_btn]
    )

    # Clear button
    clear_btn.click(
        fn=clear_form,
        inputs=[],
        outputs=[text_input, file_input, job_text_state, spinner, output_md]
    )
# Used by app.py
# Used by app.py
__all__ = ["demo"]

if __name__ == "__main__":
    demo.launch()

    # demo.launch(share=True)