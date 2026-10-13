import re
from urllib.parse import urlparse

SUSPICIOUS_TLDS = {"xyz", "top", "zip", "work", "click", "country", "gq", "tk", "ml", "cf"}
URL_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "rb.gy", "cutt.ly", "is.gd"}
SUSPICIOUS_KEYWORDS = ["login", "verify", "secure", "account", "update", "confirm", "banking", "signin"]
RISKY_FILE_EXTENSIONS = {".exe", ".scr", ".js", ".vbs", ".bat", ".cmd", ".jar", ".hta", ".ps1"}


def analyze_url(url):
    """Returns (risk_score 0-100, classification, list of indicator strings)."""
    indicators = []
    score = 0

    parsed = urlparse(url)
    host = parsed.netloc.lower()

    # Scheme check
    if parsed.scheme != "https":
        indicators.append("URL does not use HTTPS")
        score += 10

    # IP address as hostname
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host.split(":")[0]):
        indicators.append("Hostname is a raw IP address instead of a domain name")
        score += 25

    # Excessive length
    if len(url) > 100:
        indicators.append(f"URL is unusually long ({len(url)} characters)")
        score += 10

    # Excessive subdomains
    subdomain_count = host.count(".")
    if subdomain_count > 3:
        indicators.append(f"URL has an unusually high number of subdomains ({subdomain_count})")
        score += 15

    # '@' symbol trick (browser ignores everything before @)
    if "@" in url:
        indicators.append("URL contains '@', which can be used to disguise the real destination")
        score += 20

    # Punycode / IDN homograph risk
    if "xn--" in host:
        indicators.append("Domain uses punycode encoding (possible lookalike/IDN homograph attack)")
        score += 20

    # URL shorteners
    if host in URL_SHORTENERS:
        indicators.append(f"URL uses a known shortening service ({host}), hiding the real destination")
        score += 15

    # Suspicious TLD
    tld = host.split(".")[-1] if "." in host else ""
    if tld in SUSPICIOUS_TLDS:
        indicators.append(f"Domain uses a commonly-abused top-level domain (.{tld})")
        score += 10

    # Suspicious keywords in the path/query
    full_lower = url.lower()
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in full_lower]
    if found_keywords:
        indicators.append(f"URL contains suspicious keywords: {', '.join(found_keywords[:3])}")
        score += 10

    # Unusual port
    if parsed.port and parsed.port not in (80, 443):
        indicators.append(f"URL uses a non-standard port ({parsed.port})")
        score += 10

    # Encoded characters (possible obfuscation)
    if "%" in url:
        indicators.append("URL contains percent-encoded characters, which can obscure its real content")
        score += 5

    score = min(score, 100)
    classification = classify(score)

    return score, classification, indicators


def analyze_file(filename, file_size_bytes, file_hash_sha256, vt_result=None):
    """Returns (risk_score 0-100, classification, list of indicator strings)."""
    indicators = []
    score = 0

    name_lower = filename.lower()
    ext = "." + name_lower.rsplit(".", 1)[-1] if "." in name_lower else ""

    if ext in RISKY_FILE_EXTENSIONS:
        indicators.append(f"File has a high-risk executable extension ({ext})")
        score += 30

    # Double extension trick, e.g. "invoice.pdf.exe"
    parts = name_lower.split(".")
    if len(parts) > 2 and parts[-1] in {"exe", "scr", "js", "bat", "cmd"}:
        indicators.append(f"Filename uses a double extension, often used to disguise executables ({filename})")
        score += 25

    if file_size_bytes is not None and file_size_bytes < 1024:
        indicators.append("File is unusually small, which can indicate a dropper or stub payload")
        score += 10

    if vt_result:
        malicious_count = vt_result.get("malicious", 0)
        if malicious_count > 0:
            indicators.append(f"Flagged as malicious by {malicious_count} security vendors on VirusTotal")
            score += min(malicious_count * 10, 60)
        else:
            indicators.append("Not flagged by any security vendor on VirusTotal")

    score = min(score, 100)
    classification = classify(score)

    return score, classification, indicators


def classify(score):
    if score >= 50:
        return "High Risk"
    elif score >= 20:
        return "Suspicious"
    else:
        return "Safe"