import json

from .base import ModuleTestBase
from bbot.core.event.base import event_from_json


class TestJSON(ModuleTestBase):
    def check(self, module_test, events):
        scan_data = f"{module_test.scan.name} ({module_test.scan.id})"
        dns_data = "blacklanternsecurity.com"
        context_data = f"Scan {module_test.scan.name} seeded with DNS_NAME: blacklanternsecurity.com"

        # json events
        txt_file = module_test.scan.home / "output.json"
        lines = list(module_test.scan.helpers.read_file(txt_file))
        assert lines
        json_events = [json.loads(line) for line in lines]
        scan_json = [e for e in json_events if e["type"] == "SCAN"]
        dns_json = [e for e in json_events if e["type"] == "DNS_NAME"]
        assert len(scan_json) == 1
        assert len(dns_json) == 1
        scan_json = scan_json[0]
        dns_json = dns_json[0]
        assert scan_json["data"] == scan_data
        assert dns_json["data"] == dns_data
        assert dns_json["discovery_context"] == context_data
        assert dns_json["discovery_path"] == [context_data]

        # event objects reconstructed from json
        scan_reconstructed = event_from_json(scan_json)
        dns_reconstructed = event_from_json(dns_json)
        assert scan_reconstructed.data == scan_data
        assert dns_reconstructed.data == dns_data
        assert dns_reconstructed.discovery_context == context_data
        assert dns_reconstructed.discovery_path == [context_data]


class TestJSONSIEMFriendly(ModuleTestBase):
    modules_overrides = ["json"]
    config_overrides = {"modules": {"json": {"siem_friendly": True}}}

    def check(self, module_test, events):
        txt_file = module_test.scan.home / "output.json"
        lines = list(module_test.scan.helpers.read_file(txt_file))
        passed = False
        for line in lines:
            e = json.loads(line)
            if e["data"] == {"DNS_NAME": "blacklanternsecurity.com"}:
                passed = True
        assert passed
