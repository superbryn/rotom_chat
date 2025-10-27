# ⚡️ ROTOM Chat - PYTHON

ROTOM is a simple Terminal based LAN Chat App. Made Using Python Sockets. It helps you chat with someone on same network without accessing the Internet. Might be helpful for CSLabs where phones and internet isn’t useable. 

## 🚀  Features

- Real Time Messaging using TCP sockets
- Broadcast Notification when users join and leave
- No message overlapping

## 🧐  How It Works

ROTOM uses Python’s built-in `socket` and `threading` modules to handle multiple clients.
Each connected client gets its own thread for receiving and sending messages.