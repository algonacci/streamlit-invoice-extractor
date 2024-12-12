from langchain_community.document_loaders import PyMuPDFLoader
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)

def extract_pdf_text(file_path):
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    text_data = ""
    for doc in documents:
        text_data += doc.page_content

    return text_data

def format_documents(text_data):
    formatted_text = text_data.replace('\n', ' ')  
    return formatted_text

invoice_extraction_prompt = """
You are an AI designed to extract specific details from an invoice. From the following invoice text, extract the following fields:
- Shipper
- Shipper Address
- Consignee
- Consignee Address
- Invoice Date
- Invoice No
- Currency
- Trade Term
- Trans Mode
- PIC (Person In Charge)
- PIC Phone No
- Description Of Goods List (Items 1 - 15)

Please extract each of these fields and return them in a clear, structured format:

Text: 
{text}
"""

def extract_invoice_details_with_chain(text_data):
    formatted_text = format_documents(text_data)

    prompt = PromptTemplate(input_variables=["text"], template=invoice_extraction_prompt)

    chain = (
        {"text": RunnablePassthrough()}  
        | prompt
        | llm
        | StrOutputParser()
    )

    result = chain.invoke({"text": formatted_text})

    return result
