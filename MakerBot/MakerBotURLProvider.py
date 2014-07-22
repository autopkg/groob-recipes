#!/usr/bin/env python
#
import re
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["MakerBotURLProvider"]


MAKE_BASE_URL = "https://www.makerbot.com/desktop"
re_dmg = re.compile(r'urlMac": "(?P<filename>[^"]+\.dmg)')


class MakerBotURLProvider(Processor):
    description = "Provides URL to the latest MakerBot Desktop Bundle."
    input_variables = {
        "base_url": {
          "required": False,
          "description": "Default is '%s." % MAKE_BASE_URL,
          },
        }
    output_variables = {
        "url": {
          "description": "URL to the latest MakerBot Desktop Bundle.",
          },
        }

    __doc__ = description

    def get_makerbot_dmg_url(self, base_url):
      # Read HTML index.
        try:
          f = urllib2.urlopen(base_url)
          html = f.read()
          f.close()
        except BaseException as e:
          raise ProcessorError("Can't download %s: %s" % (base_url, e))

        # Search for download link.
        m = re_dmg.search(html)
        url = m.group("filename")
        if not m:
          raise ProcessorError(
              "error Couldn't find %s download URL in %s" 
              % (base_url))

          return url

    def main(self):
      base_url = self.env.get("base_url", MAKE_BASE_URL)
      self.env["url"] = self.get_makerbot_dmg_url(base_url)
      self.output("Found URL %s" % self.env["url"])


if __name__ == "__main__":
  processor = MakerBotURLProvider()
  processor.execute_shell()


