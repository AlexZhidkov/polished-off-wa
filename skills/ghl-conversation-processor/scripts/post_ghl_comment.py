#!/usr/bin/env python3
"""
Post internal comments to GoHighLevel conversations.

Usage:
    python post_ghl_comment.py --contact-id <id> --message <text>
    python post_ghl_comment.py --payload-file <path>
"""

import argparse
import json
import logging
import os
import sys
from typing import Any, Optional

import requests

GHL_API_BASE = "https://services.leadconnectorhq.com"
GHL_API_VERSION = "2021-04-15"
DEFAULT_TIMEOUT_SECONDS = 20

logging.basicConfig(
    level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def _get_nested(payload: dict[str, Any], path: list[str], default: str = "") -> str:
    current: Any = payload
    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    if current is None:
        return default
    return str(current)


def _get_first(payload: dict[str, Any], paths: list[list[str]], default: str = "") -> str:
    for path in paths:
        value = _get_nested(payload, path, "")
        if value:
            return value
    return default


def extract_conversation_id(payload: dict[str, Any]) -> str:
    return _get_first(payload, [["conversationId"], ["conversation_id"], ["conversation", "id"]])


def extract_contact_id(payload: dict[str, Any]) -> str:
    return _get_first(payload, [["contact_id"], ["contactId"], ["contact", "id"], ["id"]])


def build_internal_message(payload: dict[str, Any]) -> str:
    contact_name = _get_first(payload, [["full_name"], ["contact", "name"]], "Unknown")
    contact_email = _get_first(payload, [["email"], ["contact", "email"]], "N/A")
    contact_phone = _get_first(payload, [["phone"], ["contact", "phone"]], "N/A")
    message_body = _get_first(payload, [["Message"], ["message", "body"]], "")
    when_required = _get_first(payload, [["When required"]], "Not specified")
    job_size = _get_first(payload, [["Job Size"]], "Not specified")
    contact_source = _get_first(payload, [["contact_source"]], "Not specified")
    full_address = _get_first(payload, [["full_address"]], "Not specified")
    date_created = _get_first(payload, [["date_created"]], "Not specified")

    return f"""INTERNAL: New lead from {contact_name}

--- CUSTOMER INFO ---
Name: {contact_name}
Email: {contact_email}
Phone: {contact_phone}

--- FORM DETAILS ---
Message: {message_body or 'N/A'}
When required: {when_required}
Job Size: {job_size}
Contact Source: {contact_source}
Address: {full_address}
Date Created: {date_created}

--- ACTION REQUIRED ---
Draft reply and send via GHL."""


def post_internal_comment(
    contact_id: str,
    message: str,
    api_token: Optional[str] = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict:
    token = (api_token or os.environ.get("GHL_API_TOKEN") or "").strip()
    if not token:
        raise ValueError("GHL_API_TOKEN not provided via argument or environment variable")
    if not contact_id or not contact_id.strip():
        raise ValueError("contact_id is required")
    if not message or not message.strip():
        raise ValueError("message is required")

    response = requests.post(
        f"{GHL_API_BASE}/conversations/messages",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Version": GHL_API_VERSION,
        },
        json={
            "contactId": contact_id.strip(),
            "type": "InternalComment",
            "status": "delivered",
            "message": message.strip(),
        },
        timeout=timeout_seconds,
    )
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        return {"ok": True, "statusCode": response.status_code, "body": response.text}


def process_webhook_payload(
    payload: dict[str, Any],
    api_token: Optional[str] = None,
    conversation_id_override: Optional[str] = None,
    contact_id_override: Optional[str] = None,
    dry_run: bool = False,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict:
    conversation_id = (conversation_id_override or "").strip() or extract_conversation_id(payload)
    contact_id = (contact_id_override or "").strip() or extract_contact_id(payload)

    if not contact_id:
        raise ValueError(
            "Missing contact id in payload. Provide --contact-id or include one of: contact_id, contactId, contact.id, id"
        )

    internal_message = build_internal_message(payload)

    if dry_run:
        return {
            "ok": True,
            "dryRun": True,
            "conversationId": conversation_id,
            "contactId": contact_id,
            "message": internal_message,
        }

    if not conversation_id:
        logger.warning("No conversation_id found in payload; posting with contactId only")

    return post_internal_comment(contact_id, internal_message, api_token, timeout_seconds)


def main():
    parser = argparse.ArgumentParser(description="Post internal comments to GHL conversations")
    parser.add_argument("--contact-id", help="GHL contact ID")
    parser.add_argument("--conversation-id", help="GHL conversation ID used for logging/debug context")
    parser.add_argument("--message", help="Internal comment message text")
    parser.add_argument("--payload-file", help="Path to JSON file containing webhook payload")
    parser.add_argument("--dry-run", action="store_true", help="Build payload without posting")
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--api-token", help="GHL API token")

    args = parser.parse_args()

    try:
        if args.payload_file:
            with open(args.payload_file, "r", encoding="utf-8") as file_handle:
                payload = json.load(file_handle)
            if not isinstance(payload, dict):
                raise ValueError("Payload file must contain a JSON object")
            result = process_webhook_payload(
                payload,
                args.api_token,
                conversation_id_override=args.conversation_id,
                contact_id_override=args.contact_id,
                dry_run=args.dry_run,
                timeout_seconds=args.timeout_seconds,
            )
        elif args.contact_id and args.message:
            result = post_internal_comment(args.contact_id, args.message, args.api_token, args.timeout_seconds)
        else:
            parser.print_help()
            sys.exit(1)

        print(json.dumps(result, indent=2))
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as error:
        print(f"API Error: {error}", file=sys.stderr)
        if error.response:
            print(f"Response: {error.response.text}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()