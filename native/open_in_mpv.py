#!/usr/bin/env python3
import sys
import json
import struct
import subprocess
import os
from threading import Thread

def send_message(message):
    """Send message to Firefox."""
    msg = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('I', len(msg)))
    sys.stdout.buffer.write(msg)
    sys.stdout.buffer.flush()

def read_message():
    """Read message from Firefox."""
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    message_length = struct.unpack('I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def handle_message(message):
    """Handle incoming message."""
    try:
        if message.get('action') == 'open':
            url = message.get('url')
            if url:
                # Run mpv in the background
                subprocess.Popen(['mpv', url], 
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
                send_message({"success": True})
            else:
                send_message({"success": False, "error": "No URL provided"})
    except Exception as e:
        send_message({"success": False, "error": str(e)})

def main():
    """Main loop."""
    while True:
        message = read_message()
        if message is None:
            break
        handle_message(message)

if __name__ == '__main__':
    main()
