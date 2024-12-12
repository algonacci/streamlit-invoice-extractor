import streamlit as st
from helpers import extract_pdf_text, extract_invoice_details_with_chain

def main():
    st.sidebar.title("PDF Invoice Extractor")
    uploaded_file = st.sidebar.file_uploader("Choose an invoice PDF...", type=["pdf"])
    
    st.title("PDF Invoice Extractor")
    st.write("Upload an invoice PDF to extract data.")

    if uploaded_file is not None:
        with open("uploaded_invoice.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("Processing PDF to extract text...")
        text_data = extract_pdf_text("uploaded_invoice.pdf")
        
        st.write("Extracting invoice details...")
        extracted_details = extract_invoice_details_with_chain(text_data)
        
        st.write("Extracted Invoice Details:")
        st.write(extracted_details)

if __name__ == "__main__":
    main()
