#!/usr/bin/python
#
# Copyright 2013 Greg Neagle
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
"""See docstring for MakerBotPkgFinder class"""

import os
import glob

from autopkglib.DmgMounter import DmgMounter
from autopkglib import ProcessorError


__all__ = ["MakerBotPkgFinder"]

CORE = "MakerBot Bundle*"


class MakerBotPkgFinder(DmgMounter):
    """Mounts a Makerbot.dmg and finds the sub packages."""
    input_variables = {
        "dmg_path": {
            "required": True,
            "description": "Path to a dmg containing the MakerBot Package.",
        },
    }
    output_variables = {
        "makerbot_pkg": {
            "description": "Relative path to MakerBot Bundle.pkg.",
        },
    }
    description = __doc__

    def find_match(self, mount_point, match_string):
        """Finds a file using shell globbing"""
        #pylint: disable=no-self-use
        matches = glob.glob(os.path.join(mount_point, match_string))
        if matches:
            return matches[0][len(mount_point) + 1:]
        else:
            return ""

    def main(self):
        # Mount the image.
        mount_point = self.mount(self.env["dmg_path"])
        # Wrap all other actions in a try/finally so the image is always
        # unmounted.
        try:
            self.env["makerbot_pkg"] = self.find_match(mount_point, CORE)
            self.output("Found %s" % self.env["makerbot_pkg"])
        except BaseException as err:
            raise ProcessorError(err)
        finally:
            self.unmount(self.env["dmg_path"])


if __name__ == "__main__":
    PROCESSOR = MakerBotPkgFinder()
    PROCESSOR.execute_shell()
