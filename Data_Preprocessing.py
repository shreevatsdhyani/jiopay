import json
import pickle
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import pandas as pd


# Cell 4: Data Processing Functions
def process_jio_data(input_file):
    with open(input_file, "r", encoding="utf-8") as f:  # Specify UTF-8 encoding
        data = json.load(f)
    

    documents = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    for url, content in data.items():
        # Extract FAQs
        if 'help_center' in content and 'faqs' in content['help_center']:
            for section in content['help_center']['faqs']:
                for qna in section.get('questions', []):
                    # ✅ Debug: Print to check data format
                    if not isinstance(qna, dict):
                        print(f"Skipping invalid FAQ entry: {qna}")
                        continue

                    question = qna.get('question', "Unknown Question")
                    answer = qna.get('answer', "Unknown Answer")

                    text = f"Q: {question}\nA: {answer}"
                    chunks = text_splitter.split_text(text)
                    for chunk in chunks:
                        documents.append({
                            "text": chunk,
                            "metadata": {
                                "source_url": url,
                                "section_type": "FAQ",
                                "section_title": section.get('section', 'Unknown Section')
                            }
                        })

        # Extract General Content
        if 'description' in content:
            chunks = text_splitter.split_text(content['description'])
            for chunk in chunks:
                documents.append({
                    "text": chunk,
                    "metadata": {
                        "source_url": url,
                        "section_type": "General",
                        "section_title": "Description"
                    }
                })

    return documents


# Cell 5: Run Processing
if os.path.exists("./faq.json"):
    documents = process_jio_data("./faq.json")

    # Save processed data
    with open('processed_docs.pkl', 'wb') as f:
        pickle.dump(documents, f)

    # Download processed data
    # files.download('processed_docs.pkl')
    # print("Processing complete! File downloaded as 'processed_docs.pkl'.")
else:
    print("Error: File processing failed due to missing input file.")



df = pd.DataFrame(documents)
print(df.head())  # Show first few rows
