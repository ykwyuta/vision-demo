import gradio as gr
import base64
from io import BytesIO

from openai import OpenAI

client = OpenAI()

def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    imgbase64 = base64.b64encode(buffer.getvalue()).decode("ascii")
    return imgbase64

def image_mod(image):
    imgbase64 = pil_to_base64(image)
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{imgbase64}",
                "detail": "high"
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )
    return response.choices[0].message.content

with gr.Blocks() as demo:
    inp = gr.Image(type="pil", sources=["upload", "clipboard"])
    out = gr.Markdown()
    inp.change(image_mod, inp, out)

if __name__ == "__main__":
    demo.launch()