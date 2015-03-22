#!/usr/bin/env python
#
import re
import urllib
import urllib2
import urlparse

from autopkglib import Processor, ProcessorError


__all__ = ["MakerBotURLProvider"]


USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 "
              "Safari/537.36")
MAKE_BASE_URL = "https://www.makerbot.com/desktop"
re_dmg = re.compile(r'urlMac":"(?P<filename>[^"]+\.dmg)')


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
          req = urllib2.Request(base_url)
          req.add_header('User-Agent', USER_AGENT)
          f = urllib2.urlopen(req)
          html = f.read()
          f.close()
        except BaseException as e:
          raise ProcessorError("Can't download %s: %s" % (base_url, e))

        # Search for download link.
        m = re_dmg.search(html)
        makerbot_dmg = m.group("filename").split('/')[-1]
        makerbot_url = "http://s3.amazonaws.com/downloads-makerbot-com/makerware/" + makerbot_dmg
        url_bits = urlparse.urlsplit(makerbot_url)
        encoded_path = urllib.quote(url_bits.path)
        url = url_bits.scheme + "://" + url_bits.netloc + encoded_path
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


