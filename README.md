**ROTOM Chat** is a lightweight, **Textual-powered** LAN chat application built using **Python sockets**.

It enables users on the same local network to communicate **without internet access**, featuring a nostalgic **server finder** similar to classic LAN games like Counter-Strike.

Ideal for **CS labs**, **offline setups**, or any place where local collaboration matters more than connectivity.

---

## ✨ Features

- **Real-time messaging** — Instant text communication using TCP sockets.
- **Server Finder (UDP)** — Scans the local network for active ROTOM servers and lists them for users to join.
- **Textual-powered TUI** — Clean, modern text interface built with the [Textual](https://github.com/Textualize/textual) framework.
- **Multi-user support** — Handles multiple clients simultaneously via Python threading.
- **Join/Leave notifications** — Informs all users when someone connects or disconnects.
- **No message overlap** — Clear, organized chat flow for all users.
- **Secure by design** — No message storage or logging; all communication stays in-memory.
- **Completely offline** — Works without internet or external dependencies.

---

## 🧩 How It Works

ROTOM combines **TCP for messaging**, **UDP for server discovery**, and **Textual** for its terminal interface:

1. **Server:**
    - Hosts a chat room over TCP.
    - Periodically broadcasts its presence using UDP packets.
2. **Client:**
    - Scans the local network for available ROTOM servers.
    - Displays discovered servers in a list (like classic LAN lobbies).
    - User selects a server, enters a username, and joins the chat.
3. **Messaging:**
    - Each client connection runs on a separate thread.
    - The server broadcasts messages to all connected clients in real time.
4. **Privacy:**
    - ROTOM does not store any logs or messages — everything is ephemeral.