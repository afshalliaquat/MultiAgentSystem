from __future__ import annotations

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs
import re
import webbrowser

from pipeline import research_pipeline

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "index.html"
STYLE_PATH = BASE_DIR / "static" / "style.css"


def load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def load_style() -> str:
    return STYLE_PATH.read_text(encoding="utf-8")


def to_text(value) -> str:
    if isinstance(value, str):
        return value
    if hasattr(value, "content"):
        content = value.content
        if isinstance(content, str):
            return content
        return str(content)
    return str(value)


# ── NEW ──────────────────────────────────────────────────────────────────────
def extract_score(feedback: str) -> str:
    match = re.search(r'Score:\s*(\d+\.?\d*/10)', feedback)
    return match.group(1) if match else "N/A"
# ─────────────────────────────────────────────────────────────────────────────


def render_page(topic: str = "", state: dict | None = None, error: str = "") -> str:
    template = load_template()
    state = state or {}

    urls = state.get("urls", []) or []
    urls_html = "".join(
        f'<li><a href="{escape(url, quote=True)}" target="_blank" rel="noreferrer">{escape(url)}</a></li>'
        for url in urls
    ) or "<li>No URLs extracted.</li>"

    feedback_text = to_text(state.get("feedback", "") or "")

    replacements = {
        "{{TOPIC}}": escape(topic),
        "{{TOPIC_VALUE}}": escape(topic, quote=True),
        "{{ERROR}}": f'<div class="alert">{escape(error)}</div>' if error else "",
        "{{DETAIL_VISIBLE}}": "grid" if state else "none",
        "{{URLS}}": urls_html,
        "{{SEARCH_RESULTS}}": escape(to_text(state.get("search_results", "") or "")) or "No search summary available.",
        "{{REPORT}}": escape(to_text(state.get("report", "") or "")) or "No report available.",
        "{{FEEDBACK}}": escape(feedback_text) or "No feedback available.",
        "{{SCORE}}": extract_score(feedback_text),
    }

    for token, value in replacements.items():
        template = template.replace(token, value)

    return template


class ResearchUIHandler(BaseHTTPRequestHandler):
    def _send_html(self, html_text: str) -> None:
        payload = html_text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        if self.path == "/style.css":
            payload = load_style().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        self._send_html(render_page())

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(body)
        topic = form_data.get("topic", [""])[0].strip()

        if not topic:
            self._send_html(render_page(error="Please enter a research topic."))
            return

        try:
            state = research_pipeline(topic)
        except Exception as exc:
            self._send_html(render_page(topic=topic, error=f"Research run failed: {exc}"))
            return

        self._send_html(render_page(topic=topic, state=state))

    def log_message(self, format: str, *args) -> None:
        return


def run_ui(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), ResearchUIHandler)
    url = f"http://{host}:{port}"
    print(f"Research UI running at {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    server.serve_forever()


if __name__ == "__main__":
    run_ui()