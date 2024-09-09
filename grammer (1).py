import streamlit as st
import PyPDF2
import re

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    text = ''
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() or ''
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

# Function to preprocess the extracted text
def preprocess_text(text):
    pattern = r'(?P<currency>[$€£¥₹])\s?(?P<amount>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d{3})*(?:,\d+)?)'
    matches = re.finditer(pattern, text)
    results = []
    for match in matches:
        currency = match.group("currency")
        amount = match.group("amount").replace(",", "").replace(" ", "")
        if amount:
            results.append((currency, amount))
    return results

# Function to filter and flag potential currency errors
def filter_and_flag(matches, expected_currency="$"):
    flagged_items = []
    for currency, amount in matches:
        if currency != expected_currency:
            flagged_items.append(f"Potential error: {amount} {currency}")
    return flagged_items

# Streamlit app
def main():
    st.title("PDF Currency Error Scanner")

    if 'error_history' not in st.session_state:
        st.session_state.error_history = []

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        if not text:
            st.write("No text extracted from the PDF.")
            return
        
        matches = preprocess_text(text)
        if not matches:
            st.write("No currency matches found.")
            return
        
        flagged_items = filter_and_flag(matches)
        if not flagged_items:
            st.write("No potential errors found.")
        else:
            st.write("Potential errors detected:")
            for item in flagged_items:
                st.write(item)
            st.session_state.error_history.append({
                'file_name': uploaded_file.name,
                'errors': flagged_items
            })

    if st.session_state.error_history:
        st.write("Error History:")
        for entry in st.session_state.error_history:
            st.write(f"File: {entry['file_name']}")
            for error in entry['errors']:
                st.write(f" - {error}")

    if st.button('Clear History'):
        st.session_state.error_history = []
        st.write("Error history cleared.")

if __name__ == "__main__":
    main()
