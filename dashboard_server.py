from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import mimetypes

from agents.memory import load_memory
from agents.pipeline import RUN_HISTORY_PATH, run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parent
WEB_ROOT = PROJECT_ROOT / "web"


def load_history():
    if not RUN_HISTORY_PATH.exists():
        return []

    try:
        return json.loads(RUN_HISTORY_PATH.read_text())
    except json.JSONDecodeError:
        return []


class DashboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path):
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return

        content = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/health":
            self._send_json({"status": "ok"})
            return

        if path == "/api/history":
            self._send_json({"history": load_history()[-20:]})
            return

        if path == "/api/memory":
            self._send_json({"memory": load_memory()[-20:]})
            return

        if path == "/":
            self._send_file(WEB_ROOT / "index.html")
            return

        requested = (WEB_ROOT / path.lstrip("/")).resolve()

        if WEB_ROOT.resolve() not in requested.parents and requested != WEB_ROOT.resolve():
            self.send_error(403)
            return

        self._send_file(requested)

    def do_POST(self):
        path = urlparse(self.path).path

        if path not in ("/api/run", "/pipeline/run"):
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(content_length) or b"{}")
            query = str(payload.get("query", "")).strip()
            max_rounds = int(payload.get("rounds", 2))
            target_score = int(payload.get("target", 90))
            use_memory = bool(payload.get("use_memory", True))
            demo_mode = bool(payload.get("demo_mode", False))
            source_paths = payload.get("source_paths", [])

            if isinstance(source_paths, str):
                source_paths = [path.strip() for path in source_paths.splitlines() if path.strip()]

            if not query:
                self._send_json({"error": "Query is required."}, status=400)
                return

            max_rounds = max(1, min(5, max_rounds))
            target_score = max(1, min(100, target_score))

            result = run_pipeline(
                query,
                max_rounds=max_rounds,
                target_score=target_score,
                use_memory=use_memory,
                source_paths=source_paths,
                demo_mode=demo_mode
            )
            self._send_json({"result": result})
        except Exception as error:
            self._send_json({"error": str(error)}, status=500)

    def log_message(self, format, *args):
        return


def main():
    parser = argparse.ArgumentParser(description="Run the Aerulias AI dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Aerulias AI dashboard running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
