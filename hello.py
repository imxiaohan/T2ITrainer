import gradio as gr

css_code = """
.my-file-upload {
    height: 120px !important;
    font-size: smaller !important;
}
.download-link {
    display: none !important;
}
"""

def handle_file(file_obj):
    file_path = file_obj.name
    print(file_path)
    return file_path

with gr.Blocks(css=css_code) as demo:
    gr.Markdown("# Hello World")

    with gr.Column():
        file_upload = gr.File(file_types=[".json"], label="Config File Path", file_count="single", scale=1, elem_classes="my-file-upload")
        output = gr.Textbox(label="实际保存路径")

        with gr.Row():
            save_btn = gr.Button("Load", variant="primary")
            refresh_btn = gr.Button("Download", variant="secondary")
    
    # 文件上传
    file_upload.change(
        fn=handle_file,
        inputs=file_upload,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()