import gradio as gr
import openai, config, subprocess
openai.api_key = config.OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are a music recommender, please respond with a list of 5 songs based on my heart rate in bpm which is currently '}]

def transcribe(heartrate):
    global messages

    transcript = heartrate

    messages.append({"role": "user", "content": heartrate})

    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"
    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs="text", outputs="text").launch()
ui.launch()
