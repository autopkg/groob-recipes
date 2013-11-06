#!/usr/bin/env python
#
# Copyright 2010 Per Olofsson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import re
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["logstashURLProvider"]


APP_BASE_URL = "http://logstash.net"
re_app_zip = re.compile(r'<a class="awesome_button" href="(?P<url>https://download.elasticsearch.org\/logstash\/logstash\/logstash\-.+\-flatjar\.jar)"', re.I)
class logstashURLProvider(Processor):
    description = "Provides URL to the latest release of logstash."
    input_variables = {
        "base_url": {
            "required": False,
            "description": "Default is 'http://logstash.net'",
        },
    }
    output_variables = {
        "url": {
            "description": "URL to the latest release of logstash.",
        },
    }
    
    __doc__ = description
    
    def get_nvalt_zip_url(self, base_url):
        # Read HTML index.
        try:
            f = urllib2.urlopen(base_url)
            html = f.read()
            f.close()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (base_url, e))
        
        # Search for download link.
        m = re_app_zip.search(html)
        if not m:
            raise ProcessorError("Couldn't find logstash download URL in %s" % base_url)
        
        # Return URL.
        return m.group("url")
    
    def main(self):
        # Determine base_url.
        base_url = self.env.get('base_url', APP_BASE_URL)
        
        self.env["url"] = self.get_nvalt_zip_url(base_url)
        self.output("Found URL %s" % self.env["url"])
    

if __name__ == '__main__':
    processor = logstashURLProvider()
    processor.execute_shell()
    

