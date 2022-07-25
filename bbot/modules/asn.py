import ipaddress
import traceback

from bbot.modules.base import BaseModule


class asn(BaseModule):
    watched_events = ["IP_ADDRESS"]
    produced_events = ["ASN"]
    flags = ["passive", "subdomain-enum", "safe"]
    scope_distance_modifier = 0

    base_url = "https://api.bgpview.io"

    def setup(self):
        self.asn_counts = {}
        self.asn_data = {}
        self.asn_metadata = {}
        return True

    def filter_event(self, event):
        if "private" in event.tags:
            return False
        return True

    def handle_event(self, event):
        if self.cache_get(event.host) == False:
            for asn in self.get_asn(event.host):
                if asn not in self.asn_metadata:
                    contacts = self.get_asn_metadata(asn)
                    for c in contacts:
                        self.emit_event(c, "EMAIL_ADDRESS", source=event)
                    self.asn_metadata[asn] = True

    def report(self):
        asn_data = sorted(self.asn_data.items(), key=lambda x: self.asn_counts[x[0]], reverse=True)
        for subnet, prefix in asn_data:
            count = self.asn_counts[subnet]
            name = prefix.get("name", "")
            description = prefix.get("description", "")
            asn = str(prefix.get("asn", {}).get("asn", ""))
            event_str = f"AS{asn} - {subnet} ({count:,} hosts): {name}, {description}"
            self.emit_event(event_str, "ASN", source=self.scan.root_event)

    def cache_get(self, ip):
        ret = False
        for p in self.helpers.ip_network_parents(ip):
            try:
                self.asn_counts[p] += 1
                if ret == False:
                    ret = p
            except KeyError:
                continue
        return ret

    def get_asn(self, ip):
        url = f"{self.base_url}/ip/{ip}"
        r = self.helpers.request(url, retries=5)
        try:
            j = r.json()
            data = j.get("data", {})
            if data:
                prefixes = data.get("prefixes", [])
                for prefix in prefixes:
                    subnet = prefix.get("prefix", "")
                    if not subnet:
                        continue
                    subnet = ipaddress.ip_network(subnet)
                    self.asn_data[subnet] = prefix
                    self.asn_counts[subnet] = 1
                    asn = str(prefix.get("asn", {}).get("asn", ""))
                    yield asn
            else:
                self.debug(f'No results for "{ip}"')
        except Exception as e:
            self.warning(f"Error retrieving ASN for {ip}: {e}")
            self.debug(traceback.format_exc())

    def get_asn_metadata(self, asn):
        url = f"{self.base_url}/asn/{asn}"
        r = self.helpers.request(url, retries=5)
        try:
            j = r.json()
            data = j.get("data", {})
            if not data:
                self.debug(f'No results for "{asn}"')
                return
            email_contacts = data.get("email_contacts", [])
            abuse_contacts = data.get("abuse_contacts", [])
            contacts = [l.strip().lower() for l in email_contacts + abuse_contacts]
            return list(set(contacts))
        except Exception as e:
            self.warning(f"Error retrieving ASN metadata for {asn}: {e}")
            self.debug(traceback.format_exc())
