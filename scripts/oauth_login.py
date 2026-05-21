#!/usr/bin/env python3
"""Obtain a Ravelry OAuth 2.0 access token via the browser authorization code flow.

Reads OAuth client credentials from .env.oauth (or flags), opens the user's browser
to Ravelry's authorization page, captures the callback on localhost, and saves
the resulting tokens to .oauth_tokens.json.

Prerequisites:
  1. Register http://localhost:8080/callback as a redirect URI in the Ravelry
     developer portal for your app.
  2. Fill in .env.oauth with your client ID and secret.

Usage:
    python scripts/oauth_login.py
    python scripts/oauth_login.py --env-file .env.oauth
    python scripts/oauth_login.py --oauth-clientid your_id --oauth-secret your_secret

.env.oauth format:
    RAVELRY_OAUTH_CLIENT_ID=your_client_id
    RAVELRY_OAUTH_CLIENT_SECRET=your_client_secret
    RAVELRY_OAUTH_REDIRECT_URI=http://localhost:8080/callback  # optional
    RAVELRY_OAUTH_SCOPES=offline                               # optional, space-separated
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ravelry OAuth 2.0 login")
    p.add_argument(
        "--env-file",
        metavar="FILE",
        default=str(ROOT / ".env.oauth"),
        help="Env file to load OAuth credentials from (default: .env.oauth)",
    )
    p.add_argument("--oauth-clientid", metavar="ID",     help="OAuth client ID (overrides env file)")
    p.add_argument("--oauth-secret",   metavar="SECRET", help="OAuth client secret (overrides env file)")
    return p.parse_args()


args = _parse_args()
load_dotenv(Path(args.env_file))

CLIENT_ID = args.oauth_clientid or os.environ.get("RAVELRY_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = args.oauth_secret or os.environ.get("RAVELRY_OAUTH_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get("RAVELRY_OAUTH_REDIRECT_URI", "http://localhost:8080/callback")
SCOPES = os.environ.get("RAVELRY_OAUTH_SCOPES", "offline").split()

if not CLIENT_ID or not CLIENT_SECRET:
    sys.exit(
        f"OAuth credentials required: set RAVELRY_OAUTH_CLIENT_ID/RAVELRY_OAUTH_CLIENT_SECRET in {args.env_file}\n"
        "or pass --oauth-clientid/--oauth-secret. See .env.example for the full format."
    )

from ravelpy.oauth import OAuthClient, save_tokens

oauth = OAuthClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

print(f"Requesting scopes: {' '.join(SCOPES)}")
print(f"Redirect URI: {REDIRECT_URI}")
print()

tokens = oauth.local_flow(SCOPES)

token_path = ROOT / ".oauth_tokens.json"
save_tokens(tokens, token_path)

hours = tokens.expires_in // 3600
minutes = (tokens.expires_in % 3600) // 60

print()
print(f"Tokens saved to {token_path}")
print(f"Access token expires in: {hours}h {minutes}m")
if tokens.refresh_token:
    print("Refresh token received — run this script again when the token expires,")
    print("or use scripts/oauth_refresh.py to refresh without re-authorizing.")
else:
    print("No refresh token (request the 'offline' scope to get one).")
