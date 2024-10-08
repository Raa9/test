import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/createJira', methods=['POST'])
def createJira():
    data = request.json

    if 'comment' in data and data['comment'].get('body', '').startswith('/jira'):
        JIRA_URL = os.getenv('JIRA_URL')
        API_TOKEN = os.getenv('JIRA_API_TOKEN')
        USER_EMAIL = os.getenv('JIRA_USER_EMAIL')
        PROJECT_KEY = os.getenv('PROJECT_KEY')
        ISSUE_TYPE_ID = os.getenv('ISSUE_TYPE_ID')

        if not all([JIRA_URL, API_TOKEN, USER_EMAIL, PROJECT_KEY, ISSUE_TYPE_ID]):
            return jsonify({"message": "Required environment variables are missing."}), 500

        auth = HTTPBasicAuth(USER_EMAIL, API_TOKEN)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "fields": {
                "description": {
                    "content": [
                        {
                            "content": [
                                {
                                    "text": "first ticket.",
                                    "type": "text"
                                }
                            ],
                            "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                },
                "project": {
                    "key": PROJECT_KEY
                },
                "issuetype": {
                    "id": ISSUE_TYPE_ID
                },
                "summary": "create jira",
            },
            "update": {}
        })

        response = requests.post(
            JIRA_URL,
            data=payload,
            headers=headers,
            auth=auth
        )

        return jsonify(response.json())

    return jsonify({"message": "No JIRA ticket created. Comment does not match trigger."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
