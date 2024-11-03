import gradio as gr

def greet(name):
    return f"Hello, {name}!"

with gr.Blocks() as demo:
    with gr.Row().style(equal_height=False):
        name = gr.Textbox(label="Name")
        submit = gr.Button("Greet")
    output = gr.Textbox(label="Greeting")
    
    submit.click(fn=greet, inputs=name, outputs=output)

if __name__ == "__main__":
    demo.launch()
