import os
import openai
import markdown2
from flask import (Flask, render_template, request)

app = Flask(__name__)

# Azure OpenAI Configuration using environment variables
os.environ["AZURE_OPENAI_API_KEY"] = "your_api_key_here"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://awopenai.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2025-01-01-preview"

# Initialize Azure OpenAI client
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Define the model deployment name
deployment_name = "gpt-4o-mini"  # Replace with your model deployment name

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        try:
            print(f"Sending request to Azure OpenAI with deployment: {deployment_name}")
            print(f"User input: {user_input}")
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Always format your responses in markdown."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1000
            )
            response_text = response["choices"][0]["message"]["content"]
            print(f"Received response: {response_text}")
            # Convert markdown to HTML
            html_response = markdown2.markdown(response_text)
            return render_template('azure_openai.html', response=html_response)
        except Exception as e:
            print(f"Error details: {str(e)}")
            print(f"Error type: {type(e)}")
            return render_template('azure_openai.html', response=f"Error: {str(e)}")
    return render_template('azure_openai.html')

if __name__ == '__main__':
   app.run(port=5002, debug=True)
