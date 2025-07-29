# auth.py

import requests
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# Replace these with your actual values
CLIENT_KEY = 'aw7zaowmp078p7qv'
CLIENT_SECRET = 'GHLhtQJ0OmljhSkGXmiQH97kDY51DkvV'
REDIRECT_URI = 'http://localhost:8000/callback'
SCOPES = 'user.info.basic,video.list,video.data,business.basic,business.video.list,business.video.data
'

# Step 1: Build the authorization URL
def build_auth_url():
    base_url = "https://open.tiktokapis.com/v2/platform/oauth/connect/"
    params = {
        "client_key": CLIENT_KEY,
        "scope": SCOPES,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": "your_custom_state"
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

# Step 2: Create a local server to catch the redirect
class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful. You can close this window.")
            auth_code = params["code"][0]
            print("Authorization code:", auth_code)
            get_access_token(auth_code)

# Step 3: Exchange code for access token
def get_access_token(auth_code):
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        print("Access token:", token_data.get("access_token"))
        print("Refresh token:", token_data.get("refresh_token"))
    else:
        print("Failed to get token:", response.text)

# Step 4: Run the full flow
def run_auth_flow():
    print("Opening browser for TikTok authorization...")
    auth_url = build_auth_url()
    webbrowser.open(auth_url)
    print("Listening for redirect on http://localhost:8000/callback")
    server = HTTPServer(('localhost', 8000), RedirectHandler)
    server.handle_request()

if __name__ == "__main__":
    run_auth_flow()
