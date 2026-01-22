# 🛡️ SpecterPanel — Advanced C2 Framework

> **Dynamic Code Injection with AI & Mutating Payload Architecture**

SpecterPanel is a modular, high-resilience Command and Control (C2) platform engineered for stealth, automation, and distributed operations. By integrating **Dynamic Code Injection with AI**, the platform moves beyond static malware signatures, allowing red teams to generate unique, environment-aware payloads that evade modern EDR and AV solutions.

---

## 🚀 Evolutionary Features

### 🧠 Dynamic Code Injection with AI

SpecterPanel leverages a proprietary **AI-Orchestration Engine** (via OpenRouter) to automate payload development.

* **Just-In-Time Mutation:** Generates unique Python logic at the moment of execution, ensuring no two payloads share the same file signature.
* **EDR Bypass via LLM:** Intelligently rewrites execution logic to avoid known behavioral hooks.
* **Reflective Memory Execution:** Pushes AI-generated instructions directly into the **PhantomGate** memory space via `exec()` loops, avoiding disk-based detection.

### 🔐 Military-Grade Stealth

* **AES-256 EAX Cryptography:** All agent-to-server traffic is protected by authenticated encryption, ensuring total confidentiality and preventing MitM command tampering.
* **Anti-Analysis & VM Evasion:** PhantomGate interrogation modules detect sandboxes (Docker, LXC, VirtualBox) by checking DMI strings and cgroup artifacts before activation.
* **Adaptive Rate Control:** Smart UDP flood modules monitor host network health to maintain stability during high-volume stress testing.

### 🌐 Scalable Orchestration

* **Distributed Agent Management:** A robust SQLAlchemy backend tracks thousands of global targets with real-time status monitoring.
* **Interactive Web-Terminal:** Low-latency browser-based interface for direct shell access and remote file management.

---

## 📁 Architecture Overview

```text
SpecterPanel/
├── api/                # AES-Encrypted API & Handshake logic
├── ai_api.py           # The AI Mutation Engine (Claude-3/GPT-4)
├── PhantomGate.py      # Stealth Agent with Situational Awareness
├── view/               # Orchestration Blueprints (Botnet/Web-Terminal)
├── db/                 # ORM Models (SQLAlchemy / SQLite)
└── utility/            # Cryptographic & Processing Helpers

```

---

## ⚙️ Installation & Deployment

### 1. Requirements

* Python 3.10+
* OpenRouter API Key (required for AI Mutation)
* Linux (Ubuntu/Debian recommended for Server)

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/omerKkemal/oh-tool-v2.git
cd oh-tool-v2

# Install dependencies
pip install -r requirements.txt

# Configure security variables
# Edit utility/setting.py and set your encryption keys

```

### 3. Initialize the Hive

```bash
python initial_db.py  # Prepare SQLAlchemy database
flask run             # Start the C2 Orchestrator

```

---

## 🛠️ Modules & Components

| Component | Technical Specialization |
| --- | --- |
| **PhantomGate** | Multi-platform agent (Windows/Linux/Android) with persistence. |
| **Specter API** | Secure gateway for target registration and instruction polling. |
| **Injection Panel** | Direct-to-memory code deployment interface. |
| **BotNet Manager** | Real-time tracking and task coordination for remote assets. |

---

## 📸 Interface Preview

| Security Dashboard | Dynamic AI Injection | Secure Web Terminal |
| --- | --- | --- |
|  |  |  |

---

## 📜 Legal Notice & Disclaimer

**SpecterPanel is for authorized security testing and educational purposes only.** Unauthorized access to computer systems is illegal. The developer (Omer Kemal) assumes no liability for misuse of this software. By downloading this tool, you agree to use it in compliance with all local and international laws.

---

**Author:** [Omer Kemal](https://github.com/omerKkemal)

**License:** Proprietary - All Rights Reserved © 2025
