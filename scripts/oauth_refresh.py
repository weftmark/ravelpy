#!/usr/bin/env python3
"""Refresh a Ravelry OAuth 2.0 access token without re-authorizing in the browser.

Requires a refresh token — only available when the 'offline' scope was requested
during the original authorization (oauth_login.py).  Overwrites .oauth_tokens.json
with the new token data.

Usage:
    python scripts/oauth_refresh.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent

load_dotenv(ROOT / ".env.oauth")

CLIENT_ID = os.environ.get("RAVELRY_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("RAVELRY_OAUTH_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get("RAVELRY_OAUTH_REDIRECT_URI", "http://localhost:8080/callback")

if not CLIENT_ID or not CLIENT_SECRET:
    sys.exit("RAVELRY_OAUTH_CLIENT_ID and RAVELRY_OAUTH_CLIENT_SECRET must be set in .env.oauth")

token_path = ROOT / ".oauth_tokens.json"
if not token_path.exists():
    sys.exit(f"No tokens found at {token_path}. Run scripts/oauth_login.py first.")

from ravelpy.oauth import OAuthClient, load_tokens, save_tokens

current = load_tokens(token_path)
if not current.refresh_token:
    sys.exit(
        "No refresh token in .oauth_tokens.json.\n"
        "Re-run scripts/oauth_login.py with the 'offline' scope to get one."
    )

oauth = OAuthClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
new_tokens = oauth.refresh(current.refresh_token)
save_tokens(new_tokens, token_path)

hours = new_tokens.expires_in // 3600
minutes = (new_tokens.expires_in % 3600) // 60

print(f"Token refreshed. New access token expires in: {hours}h {minutes}m")
print(f"Tokens saved to {token_path}")
