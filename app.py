import gradio as gr
from logic import process_meeting, send_email


# Build Gradio UI
with gr.Blocks(theme=gr.themes.Soft(), title="AI Meeting Assistant") as demo:
    gr.Markdown("# 🎧 AI Meeting Assistant")
    gr.Markdown("Upload your meeting audio to get an automated transcript, professional summary, and downloadable PDF report.")
    
    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Upload Meeting Audio")
            process_btn = gr.Button("Transcribe & Summarize", variant="primary")
            pdf_output = gr.File(label="Download PDF Report")
            
            # Email sending section
            gr.Markdown("---")
            gr.Markdown("### 📧 Email Report (Optional)")
            email_input = gr.Textbox(
                label="Recipient Email", 
                placeholder="example@email.com",
                info="Enter email to send the report"
            )
            send_email_btn = gr.Button("Send Email", variant="secondary")
            email_status = gr.Markdown(label="Email Status")
            
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.TabItem("Summary"):
                    summary_output = gr.Markdown(label="Meeting Summary")
                with gr.TabItem("Full Transcript"):
                    transcript_output = gr.Textbox(label="Transcript", lines=15, interactive=False)

    # Event binding
    process_btn.click(
        fn=process_meeting,
        inputs=[audio_input],
        outputs=[transcript_output, summary_output, pdf_output, email_status]
    )
    
    send_email_btn.click(
        fn=send_email,
        inputs=[email_input],
        outputs=[email_status]
    )
    
    gr.Markdown("---")
    gr.Markdown("*Powered by Groq (Whisper-v3 & LLaMA-3.3)*")

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)

