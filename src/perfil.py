import gradio as gr

p1 = "Cual es tu Nombre?"
p2 = "Que edad tienes?"
p3 = "Que profesion tienes?"
p4 = "Cuantos ingresos tienes?"


def save_data(r1, r2, r3, r4):
    with open(f"../perfiles/{r1}.txt", "w") as file:
        file.write(f"{p1}:{r1}\n{p2}:{r2}\n{p3}:{r3}\n{p4}:{r4}\n")
    return "Data saved successfully."


with gr.Blocks() as demo:
    gr.Markdown("## Perfil")
    resp1 = gr.Textbox(label=p1)
    resp2 = gr.Textbox(label=p2)
    resp3 = gr.Textbox(label=p3)
    resp4 = gr.Textbox(label=p4)
    send = gr.Button("Submit")
    confirmacion = gr.Markdown()
    send.click(save_data, inputs=[resp1, resp2, resp3, resp4], outputs=confirmacion)


demo.launch()
