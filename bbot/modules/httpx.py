import json
import subprocess

from .base import BaseModule


class httpx(BaseModule):

    watched_events = ["OPEN_TCP_PORT", "URL_UNVERIFIED"]
    produced_events = ["URL", "HTTP_RESPONSE"]
    flags = ["active"]
    batch_size = 100
    options = {"in_scope_only": True, "version": "1.2.1", "max_response_size": 5242880}
    options_desc = {
        "in_scope_only": "Only visit web resources that are in scope.",
        "version": "httpx version",
        "max_response_size": "Max response size in bytes",
    }
    deps_ansible = [
        {
            "name": "Download httpx",
            "unarchive": {
                "src": "https://github.com/projectdiscovery/httpx/releases/download/v{BBOT_MODULES_HTTPX_VERSION}/httpx_{BBOT_MODULES_HTTPX_VERSION}_linux_amd64.zip",
                "include": "httpx",
                "dest": "{BBOT_TOOLS}",
                "remote_src": True,
            },
        }
    ]

    def setup(self):
        self.timeout = self.scan.config.get("httpx_timeout", 5)
        self.max_response_size = self.config.get("max_response_size", 5242880)
        return True

    def filter_event(self, event):
        # scope filtering
        in_scope_only = self.config.get("in_scope_only", True)
        if in_scope_only and not self.scan.in_scope(event):
            return False
        # reject base URLs to avoid visiting a resource twice
        # note: speculate makes open ports from
        return True

    def handle_batch(self, *events):

        stdin = []
        for e in events:
            if e.type == "URL_UNVERIFIED":
                if not "spider-danger" in e.tags:
                    # we NEED the port, otherwise httpx will try HTTPS even for HTTP URLs
                    stdin.append(e.with_port().geturl())
            else:
                stdin.append(str(e.data))

        command = [
            "httpx",
            "-silent",
            "-json",
            "-include-response",
            "-timeout",
            self.timeout,
            "-header",
            f"User-Agent: {self.scan.useragent}",
            "-response-size-to-read",
            f"{self.max_response_size}",
        ]
        proxy = self.scan.config.get("http_proxy", "")
        if proxy:
            command += ["-http-proxy", proxy]
        for line in self.helpers.run_live(command, input=stdin, stderr=subprocess.DEVNULL):
            try:
                j = json.loads(line)
            except json.decoder.JSONDecodeError:
                self.debug(f"Failed to decode line: {line}")
                continue

            url = j.get("url", "")
            status_code = int(j.get("status-code", 0))
            if status_code == 0:
                self.debug(f'No HTTP status code for "{url}"')
                continue

            source_event = None
            for event in events:
                if url in event:
                    source_event = event
                    break

            if source_event is None:
                self.warning(f"Unable to correlate source event from: {line}")
                continue

            # discard 404s from unverified URLs
            if source_event.type == "URL_UNVERIFIED" and status_code in (404,):
                self.debug(f'Discarding 404 from "{url}"')
                continue

            # main URL
            url_event = self.make_event(url, "URL", source_event, tags=[f"status-{status_code}"])
            if url_event:
                self.emit_event(url_event)
                # HTTP response
                self.emit_event(j, "HTTP_RESPONSE", url_event, internal=True)
