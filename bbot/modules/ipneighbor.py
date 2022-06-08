import ipaddress

from .base import BaseModule


class ipneighbor(BaseModule):

    watched_events = ["IP_ADDRESS"]
    produced_events = ["IP_ADDRESS"]
    flags = ["subdomain-enum"]
    max_scope_distance = 1
    options = {"num_bits": 4}
    options_desc = {"num_bits": "Netmask size (in CIDR notation) to check. Default is 4 bits (16 hosts)"}

    def setup(self):
        self.processed = set()
        self.num_bits = max(1, int(self.config.get("num_bits", 4)))
        return True

    def handle_event(self, event):
        main_ip = event.host
        netmask = main_ip.max_prefixlen - min(main_ip.max_prefixlen, self.num_bits)
        network = ipaddress.ip_network(f"{main_ip}/{netmask}", strict=False)
        subnet_hash = hash(network)
        if not subnet_hash in self.processed:
            self.processed.add(subnet_hash)
            for ip in network:
                if ip != main_ip:
                    self.emit_event(str(ip), "IP_ADDRESS", event, internal=True)
