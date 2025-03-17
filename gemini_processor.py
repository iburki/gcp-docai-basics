import google.generativeai as genai
import os

def get_summary(file):

    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)

    
    sample_pdf = genai.upload_file(path="PDF Path", display_name="file")

    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    
    response = model.generate_content(
        contents=[sample_pdf, "Give me a summary of this pdf file." ]
    )
    print(response.text)

    return response.text
