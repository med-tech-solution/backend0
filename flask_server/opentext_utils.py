import os
import requests
import json

def send_email(admin_mail, body):
    # Fetch credentials from environment variables
    organization_id = os.getenv("ORGANIZATION_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    client_public_id = os.getenv("CLIENT_PUBLIC_ID")
    app_id = os.getenv("APP_ID")
    app_client = os.getenv("APP_CLIENT")
    app_confidential_client = os.getenv("APP_CONFIDENTIAL_CLIENT")
    app_secret = os.getenv("APP_SECRET")
    tenancy = os.getenv("TENANCY")

    # Email request payload
    payload = {
        "options": {
            "message_id": "unique_message_id",
            "billing_code": "billing_code_example",
            "customer_reference": "customer_ref_example",
            "email_options": {
                "subject": "Sample Email Subject",
                "from_display_name": "Sample Display Name",
                "forward_reply": admin_mail,
                "charset": "UTF-8",
                "pull_password": "123456",
                "html_open_tracking": "top",
                "expiration_days": 14,
                "display_to": admin_mail
            }
        },
        "destinations": [
            {
                "ref": "ref001",
                "email": admin_mail,
                "inserts": [
                    {
                        "id": 1,
                        "value": "destination_insert_value"
                    }
                ]
            }
        ],
        "body": [
            {
                "name": "content.txt",
                "type": "text",
                "charset": "UTF-8",
                "data": body
            }
        ]
    }

    # Request headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client_secret}'  # Assuming client_secret is used as a token
    }

    # Make the POST request
    response = requests.post(
        'https://t2api.us.cloudmessaging.opentext.com/mra/v1/outbound/emails',
        headers=headers,
        data=json.dumps(payload)
    )

    # Check the response status
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

# Example usage:
# Ensure environment variables are set, then call the function
# send_email('admin@example.com', 'VGhpcyBpcyBzYW1wbGUgdGV4dCBkYXRh')
