import streamlit as st

# HTML and CSS
st.markdown("""
<style>
/* Full page background image */
.stApp {
    background-size: cover;
    background-color: #791cc9; /* Light grey background for contrast */
}

/* Custom styles */
.big-font {
    font-size: 24px !important;
    color: #ff0000; /* Dark blue for professional look */
}



.highlight {
    background-color: ##803ebd; /* Light blue for highlights */
    padding: 10px;
    border-radius: 5px;
    color: ##803ebd; /* Dark blue text for readability */
}
</style>
<div class="big-font">Welcome to the Financial Dashboard</div>
<div class="highlight">Financial analysis insights.</div>
""", unsafe_allow_html=True)

# Define the paths to your Streamlit files
file_paths = {
    "Cognizant": "/Users/pragyan/Desktop/Map.py",
    "Prior Year Tieout": "/Users/pragyan/Desktop/prior.py",
    "Mathematical Accuracy": "/Users/pragyan/Desktop/Accuracy.py",
    "Internal Consistency": "/Users/pragyan/Desktop/Internal.py",
    "Possible Syntactic Errors": "/Users/pragyan/Desktop/grammer.py"
}

def run_file(file_path):
    """Run the selected Streamlit file."""
    with open(file_path, "r") as f:
        code = f.read()
    exec(code, globals())

# Create a dropdown menu for file selection
selected_file = st.selectbox("Select a Service ", options=list(file_paths.keys()))

# Display the selected file's content
if selected_file:
    file_path = file_paths[selected_file]
    st.write(f"Running {selected_file}...")
    run_file(file_path)
