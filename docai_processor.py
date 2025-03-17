from google.cloud import documentai
import os

def process_document(file):
    try:
        # Initialize Document AI client
        client = documentai.DocumentProcessorServiceClient()
        
        # Configure processor path
        LOCATION = 'us'  # Format is 'us' or 'eu'
        PROJECT_ID = os.getenv('PROJECT_ID')
        PROCESSOR_ID = os.getenv('PROCESSOR_ID')
        
        if not PROJECT_ID or not PROCESSOR_ID:
            raise ValueError("PROJECT_ID and PROCESSOR_ID must be set in .env file")
        
        PROCESSOR_PATH = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
        print(f"Using processor path: {PROCESSOR_PATH}")
        
        # Read file content
        file_content = file.read()
        print(f"Read file content, size: {len(file_content)} bytes")
        
        # Configure the process request
        raw_document = documentai.RawDocument(
            content=file_content,
            mime_type="application/pdf"
        )
        
        # Process the document
        request = documentai.ProcessRequest(
            name=PROCESSOR_PATH,
            raw_document=raw_document
        )
        
        print("Sending request to Doc AI...")
        result = client.process_document(request=request)
        print("Received response from Doc AI")
        
        document = result.document
        
        # Extract entities from the processed document
        extracted_data = {}
        for entity in document.entities:
            extracted_data[entity.type_] = entity.mention_text
            
        print(f"Extracted {len(extracted_data)} entities")
        return extracted_data
        
    except Exception as e:
        print(f"Error in process_document: {str(e)}")
        raise