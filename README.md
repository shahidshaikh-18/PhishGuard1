🛡️ PhishGuard — Phishing Detection & URL Security Scanner

PhishGuard is a Python web application project for analyzing URLs and supporting phishing awareness. It provides account authentication, a scanner interface, scan results, scan history, insights, and profile pages through a modular Flask-style application.

> **Important:** Detection results are indicators, not a guarantee that a URL is safe or malicious. Use the tool as a defensive aid, not as a substitute for independent verification.

## ✨ Features

- **URL Scanning:** Submit a URL for analysis using the detection logic implemented in the scanner module.
- **Scan Results:** View the outcome of a scan.
- **Scan History:** Review previously recorded scans, if enabled in the configured database.
- **Insights Dashboard:** View security insights exposed by the application.
- **User Authentication:** Login and signup routes.
- **Profile Page:** User profile interface.
- **File Scanning Interface:** A page for file-based scanning, subject to the formats and checks implemented by the application.
- **Modular Architecture:** Separate modules for authentication, dashboard, history, profile, and scanner functionality.
- **Web Interface:** Shared base template with HTML templates and static CSS/JavaScript assets.

## 🧰 Technology Stack

- **Language:** Python
- **Web framework:** Flask (verify against the imports in your project)
- **Frontend:** HTML, CSS, JavaScript
- **Database layer:** See `app/models.py` and `app/config.py` for the database and configuration actually used
- **HTTP/URL analysis:** Depends on the implementation in `app/scanner/engine.py`

## 📁 Project Structure

```text
PhishGuard/
├── app/
│   ├── auth/
│   │   └── routes.py
│   ├── dashboard/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── history/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── profile/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── routes.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── history.html
│       ├── insights.html
│       ├── login.html
│       ├── profile.html
│       ├── scan_file.html
│       ├── scan_result.html
│       ├── scanner.html
│       └── signup.html
├── instance/
├── .env
├── requirements.txt
└── run.py
```

This structure is based on the supplied screenshots. Adjust it if your local files differ.

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/shahidshaikh-18/PhishGuard.git
cd PhishGuard
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

**Linux / Kali Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file with the variables required by your application. Never commit real secret keys, credentials, or tokens.

### 5. Start the application

```bash
python run.py
```

Open the local address shown in the terminal. If your app uses a different startup command, follow the entry point defined by your code.

## 🧪 Suggested Tests

- Submit valid, malformed, and suspicious-looking URLs.
- Confirm the scanner returns understandable results and handles errors safely.
- Check that scan history displays only the current user's permitted records.
- Test login, signup, logout, and access control.
- Test file-scanning validation with harmless test files only.
- Confirm secrets and passwords are not exposed in logs or error messages.

## 🔐 Security & Privacy

- Do not enter real account passwords into a URL scanner.
- Use secure password hashing for user accounts.
- Validate URL schemes and inputs before making network requests.
- Protect against server-side request forgery (SSRF) if the scanner fetches submitted URLs; restrict loopback, private, link-local, and other sensitive destinations, including redirects.
- Limit file size and validate file types if file uploads are supported.
- Keep `.env`, virtual environments, local databases, and sensitive logs out of version control.
- Only scan URLs and files you are authorized to analyze.

## 🚀 Possible Improvements

- Clear explanations for individual URL-risk indicators.
- Threat-intelligence or reputation service integration.
- Exportable scan reports.
- Scan history filtering and pagination.
- Automated tests and rate limiting.
- Improved audit logging and deployment documentation.

## 👨‍💻 Author

**Shahid Shaikh**  
Aspiring Cybersecurity Analyst | VAPT & Penetration Testing Enthusiast
"""
