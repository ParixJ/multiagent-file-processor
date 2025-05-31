import streamlit as st
import asyncio
from Agents.agent_router import route
from database.db import DatabaseAgent
import httpx

# Streamlit App
st.title("Multi-Agent File Processing System")

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=['pdf', 'json', 'eml', 'msg', 'emlx', 'pst'])

if uploaded_file is not None:
    # Convert Streamlit UploadedFile to a compatible file-like object
    try:
        # Streamlit uploaded_file is in-memory, need to save temporarily or wrap for compatibility
        # Save to a temporary file
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Open the file as a file-like object
        with open(uploaded_file.name, 'r') as file_obj:
            st.write("Processing the uploaded file...")
            try:
                file_data = asyncio.run(route(file_obj))
                if file_data:
                    if 'error' in file_data:
                        st.error(f"Error: {file_data['error']}")
                    else:
                        st.success("File processed successfully!")
                        st.write("Extracted Data:", file_data)

                        # Insert into database
                        st.session_state['file_data'] = file_data
                        dbAgent = DatabaseAgent()
                        dbAgent.insert(data=file_data)

                        # Option to display database content
                        if st.button("Show Stored Data"):
                            df = dbAgent.fetch_data()
                            st.dataframe(df)
                else:
                    st.warning("Filetype not supported. Please upload a valid file.")

            except httpx.ConnectError as e:
                st.error(f"Connection error: {e}. Please check your internet connection.")

            except Exception as e:
                st.error(f"Unexpected error: {e}")

    except Exception as e:
        st.error(f"Error handling the uploaded file: {e}")
else:
    st.info("Please upload a file to get started.")
