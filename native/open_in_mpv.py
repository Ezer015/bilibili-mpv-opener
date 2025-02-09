#!/usr/bin/env python3
"""
Native messaging host for Bilibili MPV Opener browser extension.

This script acts as a bridge between the browser extension and MPV player.
It receives URLs from the browser extension via native messaging protocol
and launches MPV to play the videos.

Compatible with:
- Firefox through mozilla-native-messaging-hosts
- Chrome through chrome-native-messaging
"""

import sys
import json
import struct
import subprocess


def send_message(message):
    """
    Send a message back to the browser extension.

    Uses native messaging protocol:
    - First 4 bytes: message length as unsigned int
    - Remaining bytes: message content as JSON

    Args:
        message: Dictionary to be sent as JSON
    """
    msg = json.dumps(message).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("I", len(msg)))
    sys.stdout.buffer.write(msg)
    sys.stdout.buffer.flush()


def read_message():
    """
    Read a message from the browser extension.

    Native messaging protocol:
    - First 4 bytes: message length as unsigned int
    - Remaining bytes: message content as JSON

    Returns:
        dict: Parsed JSON message from the extension
        None: If the input stream is closed
    """
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    message_length = struct.unpack("I", raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(message)


def handle_message(message):
    """
    Process messages received from the browser extension.

    Supported actions:
    - "open": Launch MPV with the provided URL

    Args:
        message: Dictionary containing the action and parameters
                Expected format: {"action": "open", "url": "video_url"}

    Error handling:
    - Missing URL: Returns error message
    - MPV launch failure: Returns exception details
    """
    try:
        if message.get("action") == "open":
            url = message.get("url")
            if url:
                # Launch MPV in background, suppressing output
                subprocess.Popen(
                    ["mpv", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                send_message({"success": True})
            else:
                send_message({"success": False, "error": "No URL provided"})
    except Exception as e:
        send_message({"success": False, "error": str(e)})


def main():
    """
    Main event loop.

    Continuously reads messages from the browser extension and processes them
    until the input stream is closed (which happens when the browser closes
    or the extension is unloaded).
    """
    while True:
        message = read_message()
        if message is None:  # Input stream closed
            break
        handle_message(message)


if __name__ == "__main__":
    main()
