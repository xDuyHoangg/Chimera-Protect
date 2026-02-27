# 🧬 Chimera-Protect
### Advanced Bio-Digital Encryption Architecture

> **Secure • Authenticated • Obfuscated**  
> Next-gen hybrid AES + DNA obfuscation engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/Version-5.0-violet?style=flat-square)

---

## 🔗 Quick Links

- 👨‍💻 **Creator**: Nguyễn Duy Hoàng  
- 🌐 Facebook: [facebook.com/User.DuyHoangg](https://www.facebook.com/User.DuyHoangg)  
- 📩 Telegram: [t.me/Tcp_API](https://t.me/Tcp_API)  
- ⭐ **Star this repo** nếu bạn thấy hay!

---

## 📌 Table of Contents

- [Overview](#-overview--giới-thiệu)
- [Architecture](#-project-structure--cấu-trúc-dự-án)
- [Encryption Flow](#-encryption-workflow--quy-trình-mã-hóa)
- [Installation](#-installation--cài-đặt)
- [Environment Setup](#-environment-configuration--cấu-hình-môi-trường)
- [Running Server](#-running-the-server--chạy-server)
- [API Documentation](#-api-documentation--tài-liệu-api)
- [Security](#-security-notes--lưu-ý-bảo-mật)
- [License](#-license)

---

## 🚀 Overview | Giới thiệu

**Chimera-Protect** là lõi mã hóa bảo mật cao sử dụng:

- 🔐 AES-256-GCM (NIST Standard)
- 🔑 PBKDF2-HMAC-SHA256 (100,000 iterations)
- 🧂 Random Salt mỗi request
- 🧬 DNA Transformation Layer (Obfuscation)
- 🌍 REST API bằng Flask

Designed for secure API payload protection and encrypted communication systems.

---

## 🏗 Project Structure | Cấu trúc dự án

```bash
chimera-engine/
├── core/
│   ├── __init__.py
│   └── sequencer.py
├── app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 Encryption Workflow | Quy trình mã hóa

<details>
<summary><strong>Click để xem chi tiết</strong></summary>

1️⃣ Generate 16-byte random salt  
2️⃣ Derive 256-bit key via PBKDF2  
3️⃣ Encrypt using AES-256-GCM  
4️⃣ Pack: `Nonce + AuthTag + Ciphertext`  
5️⃣ Convert to DNA sequence  

### 🧬 DNA Mapping

| Bits | DNA |
|------|-----|
| 00 | A |
| 01 | T |
| 10 | G |
| 11 | C |

</details>

---

## 💻 Installation | Cài đặt

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/Chimera-Protect.git
cd Chimera-Protect
```

### 2️⃣ Create Virtual Environment

Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙ Environment Configuration | Cấu hình môi trường

Create `.env` file:

```env
CHIMERA_MASTER_KEY=your-very-secure-random-master-key
```

⚠ Never commit your master key.

---

## ▶ Running the Server | Chạy server

### Development

```bash
python app.py
```

### Production (Recommended)

```bash
gunicorn app:app -b 0.0.0.0:8080
```

Deploy behind **Nginx + HTTPS**.

---

## 📡 API Documentation | Tài liệu API

### 🔐 Encode

`POST /v1/sequencer/encode`

```json
{
  "input_stream": "Hello Chimera"
}
```

Response:

```json
{
  "status": "integrated",
  "genome_packet": {
    "sequence": "ATGCCGT...",
    "metadata": {
      "locus": "salt_hex_here",
      "protocol": "CHIMERA-PROTECT"
    }
  }
}
```

---

### 🔓 Decode

`POST /v1/sequencer/decode`

```json
{
  "genome_packet": {
    "sequence": "ATGCCGT...",
    "metadata": {
      "locus": "salt_hex_here",
      "protocol": "CHIMERA-PROTECT"
    }
  }
}
```

Success:

```json
{
  "status": "resolved",
  "output_stream": "Hello Chimera"
}
```

Failure:

```json
{
  "status": "rejection",
  "code": 403
}
```

---

## 🛡 Security Notes | Lưu ý bảo mật

- Always set strong `CHIMERA_MASTER_KEY`
- Use HTTPS in production
- Never expose Flask dev server publicly
- Rotate keys periodically
- Monitor logs

---

## 📜 License

MIT License  
Free to use, modify, distribute.

---

## 🧾 Intellectual Property & Legal

© 2026 Chimera-Protect. All rights reserved.

This software and its underlying cryptographic architecture are protected under international intellectual property laws.

Unauthorized reproduction, redistribution, reverse engineering, or commercial exploitation without explicit permission is strictly prohibited.

Chimera-Protect is an independent bio-digital encryption framework designed for research, security development, and enterprise integration.

---

## 🔐 Security Commitment

Chimera-Protect follows modern cryptographic standards including:

- AES-256-GCM authenticated encryption
- PBKDF2-HMAC-SHA256 key derivation
- Secure random salt generation
- Integrity verification via authentication tag

Any modification to core cryptographic logic may compromise system security.

---

### 🧬 Chimera-Protect
> Advanced Bio-Digital Encryption Framework | Secure by Design

Made with ❤️ by Nguyễn Duy Hoàng
