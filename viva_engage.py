"""Publish summaries to Viva Engage (Microsoft) via Yammer API."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()


def publish_to_viva_engage(summary: str, group_id: str = None) -> dict:
    """Post the AI news summary to Viva Engage.

    Args:
        summary: The formatted summary text to post.
        group_id: Optional Viva Engage group/community ID.
                  If not provided, posts to the user's default feed.

    Returns:
        API response dict.
    """
    token = os.getenv("VIVA_ENGAGE_TOKEN")
    if not token:
        raise ValueError(
            "VIVA_ENGAGE_TOKEN not set in .env\n"
            "To get your token:\n"
            "1. Go to https://www.yammer.com/client_applications\n"
            "2. Register a new app (or use existing)\n"
            "3. Click 'Generate a developer token'\n"
            "4. Copy the token to your .env file"
        )

    url = "https://www.yammer.com/api/v1/messages.json"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "body": summary,
        "message_type": "update",
    }

    # If a group ID is specified, post to that group/community
    if group_id:
        payload["group_id"] = group_id
    else:
        # Check if there's a default group configured
        default_group = os.getenv("VIVA_ENGAGE_GROUP_ID")
        if default_group:
            payload["group_id"] = default_group

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()
