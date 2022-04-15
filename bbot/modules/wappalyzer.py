from .base import BaseModule
from Wappalyzer import Wappalyzer, WebPage

import warnings

warnings.filterwarnings(
    "ignore",
    message="""Caught 'unbalanced parenthesis at position 119' compiling regex""",
    category=UserWarning,
)


class wappalyzer(BaseModule):

    watched_events = ["URL"]
    produced_events = ["TECHNOLOGY"]

    def handle_event(self, event):

        wappalyzer = Wappalyzer.latest()
        r = self.helpers.request(event.data)
        w = WebPage.new_from_response(r)
        res_set = wappalyzer.analyze(w)
        for res in res_set:
            self.emit_event(res, "TECHNOLOGY", event, tags=["web"])
