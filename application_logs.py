import random
from utils import random_ip, random_user, random_request_id
from datetime import datetime, timezone

GOOD_RATIO = 0.65


def web_log(malicious=False):
    methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    good_paths = [
        "/", "/login", "/logout", "/dashboard", "/api/data",
        "/profile", "/settings", "/search?q=test",
        "/reports/2024", "/health"
    ]

    bad_paths = [
        "/login?u=admin'--",
        "/?id=1 OR 1=1",
        "/<script>alert(1)</script>",
        "/../../etc/passwd",
        "/admin.php",
        "/wp-admin",
        "/api/data?debug=true",
        "/cgi-bin/test.cgi"
    ]

    status_good = [200, 200, 200, 302, 304]
    status_bad = [400, 401, 403, 404, 500, 502]

    timestamp = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S +0000")

    path = random.choice(bad_paths if malicious else good_paths)
    status = random.choice(status_bad if malicious else status_good)

    return (
        f'{random_ip()} - {random_user()} '
        f'[{timestamp}] '
        f'"{random.choice(methods)} {path} HTTP/1.1" '
        f'{status} {random.randint(200,6000)}'
    )


def api_log(malicious=False):
    good_messages = [
        "Request processed successfully",
        "Token validated",
        "Cache hit",
        "User session refreshed",
        "Configuration loaded",
        "Rate limit OK"
    ]

    bad_messages = [
        "Broken authentication attempt",
        "API rate limit exceeded",
        "Excessive requests detected",
        "Invalid token signature",
        "Unauthorized access attempt",
        "Malformed request payload"
    ]

    level = "WARN" if malicious else "INFO"
    message = random.choice(bad_messages if malicious else good_messages)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        f"{timestamp} {level} API - {message} "
        f"user={random_user()} ip={random_ip()} "
        f"request_id={random_request_id()}"
    )


def file_upload_log(malicious=False):
    good_files = [
        "report.pdf", "image.png", "data.csv", "avatar.jpg",
        "invoice.xlsx", "presentation.pptx", "notes.txt"
    ]

    bad_files = [
        "shell.php", "payload.jsp", "backdoor.py", "cmd.aspx",
        "webshell.jsp", "rev.ps1", "dropper.exe"
    ]

    file = random.choice(bad_files if malicious else good_files)
    level = "WARN" if malicious else "INFO"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        f"{timestamp} {level} App - File uploaded "
        f"file={file} user={random_user()} "
        f"request_id={random_request_id()}"
    )


def exception_log(malicious=False):
    common_exceptions = [
        "TypeError",
        "ValueError",
        "TimeoutError",
        "KeyError",
        "ConnectionError"
    ]

    severe_exceptions = [
        "DatabaseTimeoutException",
        "UnauthorizedAccessException",
        "IntegrityConstraintViolation",
        "RemoteCodeExecutionException"
    ]

    level = "ERROR" if malicious else "WARN"
    exception = random.choice(severe_exceptions if malicious else common_exceptions)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        f"{timestamp} {level} App - Unhandled exception "
        f"{exception} user={random_user()} "
        f"request_id={random_request_id()}"
    )


_generator_index = 0

def generate():
    global _generator_index

    malicious = random.random() > GOOD_RATIO

    generators = [
        lambda: web_log(malicious),
        lambda: api_log(malicious),
        lambda: file_upload_log(malicious),
        lambda: exception_log(malicious)
    ]

    log = generators[_generator_index]()
    _generator_index = (_generator_index + 1) % len(generators)

    return log