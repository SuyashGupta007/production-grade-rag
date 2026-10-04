
import gradio as gr

from agent import get_agent_response


# Custom styling
css = """
#chatbot {
    height: 600px;
}

.message {
    font-size: 16px;
}
"""


# Create Gradio application
def create_app():

    with gr.Blocks(
        title="🤖 AI Chatbot",
        css=css
    ) as demo:

        # Application heading
        gr.Markdown(
            """
            # 🤖 AI Chatbot
            ### Amazon Knowledge Base + Google Gemini

            Ask questions about companies and their financial data.
            """
        )

        # Chat history
        chatbot = gr.Chatbot(
            elem_id="chatbot",
            height=600,
            type="messages"
        )

        # User input
        message = gr.Textbox(
            placeholder="Ask a question...",
            label="Your Question",
            lines=2
        )

        # Buttons
        with gr.Row():
            send = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear")

        # Handle chat
        async def chat(user_message, history):

            if not user_message.strip():
                return "", history

            history = history or []

            response = await get_agent_response(
                user_message,
                history
            )

            history.append({
                "role": "user",
                "content": user_message
            })

            history.append({
                "role": "assistant",
                "content": response
            })

            return "", history

        # Clear chat
        def clear_chat():
            return [], ""

        # Send button
        send.click(
            chat,
            inputs=[message, chatbot],
            outputs=[message, chatbot]
        )

        # Enter key
        message.submit(
            chat,
            inputs=[message, chatbot],
            outputs=[message, chatbot]
        )

        # Clear button
        clear.click(
            clear_chat,
            outputs=[chatbot, message]
        )

    return demo


# Start application
if __name__ == "__main__":

    app = create_app()

    app.launch(
        server_name="0.0.0.0",
        server_port=8080,
        share=False
    )