print("Importing gradio...")
try:
    import gradio
    print("SUCCESS: gradio imported.")
except Exception as e:
    print(f"FAILURE: gradio import failed. {e}")
except ImportError as e:
    print(f"FAILURE: gradio ImportError. {e}")
