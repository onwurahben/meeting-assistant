import gradio as gr


def process(audio):
    return "Transcript", "Summary", None

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    audio_input = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Upload Meeting Audio")
    txt = gr.Textbox()
    summ = gr.Markdown()
    file = gr.File()
    btn = gr.Button("Run")
    btn.click(process, inputs=[audio_input], outputs=[txt, summ, file])

if __name__ == "__main__":
    print("Launching complex gradio app...")
    demo.launch(server_name="127.0.0.1", server_port=7861)

