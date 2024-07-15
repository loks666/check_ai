import json
import sys
import time

import pyperclip
import requests


def check_clipboard():
    last_text = pyperclip.paste()
    print("Program is running, select text and copy to send request...")

    while True:
        time.sleep(1)
        current_text = pyperclip.paste()
        if current_text != last_text:
            print("New clipboard content detected...")
            print(f"Read text: {current_text}")

            # Define the request data to be sent
            data = {
                "document": current_text,
                "source": "landing",
                "writing_stats_required": True,
                "sampleTextSubmitted": False,
                "interpretability_required": False,
                "checkPlagiarism": False
            }

            try:
                # Send POST request
                response = requests.post("https://api.gptzero.me/v2/predict/text", json=data)

                if response.status_code == 200:
                    response_data = response.json()
                    print("API response result:")
                    print(json.dumps(response_data, indent=4, ensure_ascii=False))

                    # Extract and output the result_message value
                    documents = response_data.get('documents', [])
                    if documents:
                        result_message = documents[0].get('result_message', 'No result_message information found')
                        print(f"Feedback: {result_message}")
                    else:
                        print("No documents information found")
                else:
                    print(f"Request failed, status code: {response.status_code}")
                    response_data = response.json()
                    print("Error information:")
                    print(json.dumps(response_data, indent=4, ensure_ascii=False))
            except Exception as e:
                print(f"Exception occurred during the request: {e}")

            last_text = current_text


if __name__ == "__main__":
    try:
        check_clipboard()
    except KeyboardInterrupt:
        print("Program terminated.")
        sys.exit(0)
