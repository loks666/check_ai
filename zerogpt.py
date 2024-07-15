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
                "input_text": current_text
            }

            try:
                # Send POST request
                response = requests.post("https://api.zerogpt.com/api/detect/detectText", json=data)

                if response.status_code == 200:
                    response_data = response.json()
                    print("API response result:")
                    print(json.dumps(response_data, indent=4, ensure_ascii=False))

                    # Extract and output feedback value
                    feedback = response_data.get('data', {})
                    if feedback is None:
                        print("No feedback information found")
                    else:
                        feedback = feedback.get('feedback', 'No feedback information found')
                        print(f"Feedback: {feedback}")
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
