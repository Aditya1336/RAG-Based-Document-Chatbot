# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token



# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token

import os
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()


BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6f43a7c9-9752-4257-8369-c4b55a40c01a"
FLOW_ID = "3d24b72a-24b2-44a4-8e19-1e90f585729e"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "customer" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}


def run_flow(message: str) -> dict:
    
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = None
    
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()



def main():
    st.title("Chat Interface")

    message = st.text_area("Message",placeholder="Enter your query. ")

    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message. ")
            return
        
        try:
            with st.spinner("Running Flow..."):
                response = run_flow(message)

            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
