from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import colors

app = Flask(__name__)
CORS(app)
def generate_pdf(content):
    pdf_filename = "output.pdf"
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Add heading
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 30, "QUESTIONS")

    # Add content to PDF
    textobject = c.beginText(50, height - 60)
    textobject.setFont("Helvetica", 12)
    
    for i, question in enumerate(content, start=1):
        for line in question.split('\n'):
            textobject.textLine(line.strip())  # Trim leading/trailing whitespace and add each line separately
        textobject.textLine('')  # Add a blank line after each question

    c.drawText(textobject)
    c.save()

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf_route():
    try:
        data = request.json
        topic = data.get('topic')
        number = int(data.get('number'))

        # Get configuration settings
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
            api_version="2024-02-15-preview"
        )
        
        # Create a system message
        
        system_message = f"""I am a Professor who asks students questions on Various Topics.
Generate me a list of {number} questions related to {topic}. Just generate {number} questions nothing else Your response should start with 1. and the question. """

        # Initialize messages array
        messages_array = [{"role": "system", "content": system_message}]
        
        # Initialize list to store generated text
        generated_text_list = []
        
           
        # Request responses from Azure OpenAI model
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=1.0,
            max_tokens=1200,
            messages=messages_array
        )
        generated_text = response.choices[0].message.content
        generated_text_list.append(generated_text)

        # Generate PDF with generated questions
        generate_pdf(generated_text_list)

        # Return success response
        return jsonify({"message": "PDF generated successfully"}), 200

    except Exception as ex:
        # Return error response
        return jsonify({"error": str(ex)}), 500

if __name__ == '__main__':
    app.run(debug=True)
