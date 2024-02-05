# Created a new module called 'newsletters' that will scrap the websites (or recursive websites,
# thanks to BBOT's sub-domain enumeration) looking for the presence of an 'email type' that also
# contains a 'placeholder'. The combination of these two HTML items usually signify the presence
# of an "Enter Your Email Here" type Newsletter Subscription service. This module could be used
# to find newsletters for a future email bombing attack and/or find user-input fields that could
# be be susceptible to overflows or injections.

from .base import BaseModule
import requests
import re
from bs4 import BeautifulSoup

# Known Websites with Newsletters
# https://futureparty.com/
# https://www.marketingbrew.com/
# https://buffer.com/
# https://www.milkkarten.net/
# https://geekout.mattnavarra.com/

deps_pip = ["requests", "beautifulsoup4"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}


class newsletters(BaseModule):
    watched_events = ["HTTP_RESPONSE"]
    produced_events = ["NEWSLETTER"]
    flags = ["passive", "safe"]
    meta = {"description": "Searches for Newsletter Submission Entry Fields on Websites"}

    # Parse through Website to find a Text Entry Box of 'type = email'
    # and ensure that there is placeholder text within it.
    def find_type(self, soup):
        email_type = soup.find(type="email")
        if email_type:
            regex = re.compile(r"placeholder")
            if regex.search(str(email_type)):
                return True
            else:
                return False
        else:
            return False

    async def handle_event(self, event):
        req_url = event.data

        # req = requests.request("GET", req_url, headers=headers)  ## If it ain't broke, don't fix it
        # req = self.helpers.request(method="GET", url=req_url, headers=headers)    # Doesn't return a status_code
        # req = await self.helpers.curl(url=req_url, headers=headers)             # Doesn't return a status_code

        if event.data["status_code"] == 200:
            soup = BeautifulSoup(event.data["body"], "html.parser")
            result = self.find_type(soup)
            if result:
                newsletter_result = self.make_event(
                    data=f"Newsletter {event.data['url']}",
                    event_type="NEWSLETTER",
                    source=event,
                    tags=event.tags
                )
                # self.hugesuccess(f"Yippie! There is a Newsletter at {event.data}")
                self.emit_event(newsletter_result)
                return
            else:
                return
        else:
            return

            