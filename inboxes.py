import requests
import re

class Inboxes:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_host = "inboxes-com.p.rapidapi.com"
        self.base_url = f"https://inboxes-com.p.rapidapi.com"

    def _send_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        response = requests.request(method, url, headers=headers, **kwargs)
        return response.json()

    def activate_inbox(self, email):
        return self._send_request("POST", f"/inboxes/{email}")

    def get_all_messages(self, email):
        return self._send_request("GET", f"/inboxes/{email}")

    def get_message_content(self, uid):
        return self._send_request("GET", f"/messages/{uid}")
    
    @staticmethod
    def get_code(html_content):
     pattern = r"<p>(\d{4})<\/p>"
     match = re.search(pattern, html_content)
     if match:
         return match.group(1)  # Return the entire match as a string
     else:
         return None 
