# Copyright (C) 2016 Kevin Ross
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

try:
    import re2 as re
except ImportError:
    import re


class RansomwareDMALocker(Signature):
    name = "ransomware_dmalocker"
    description = "Exhibits behavior characteristic of DMALocker ransomware"
    weight = 3
    severity = 3
    categories = ["ransomware"]
    families = ["DMALocker"]
    authors = ["Kevin Ross"]
    minimum = "1.3"
    evented = True
    ttps = ["T1486"]  # MITRE v6,7,8
    mbcs = ["OB0008", "E1486"]

    filter_apinames = set(["RegSetValueExA"])

    def on_call(self, call, process):
        if call["api"] == "RegSetValueExA" and call["status"]:
            key = re.compile(r".*\\SOFTWARE\\(Wow6432Node\\)?Microsoft\\Windows\\CurrentVersion\\Run\\cryptedinfo$")
            buff = self.get_argument(call, "Buffer").lower()
            fullname = self.get_argument(call, "FullName")
            if buff == "notepad c:\programdata\cryptinfo.txt" and key.match(fullname):
                if self.pid:
                    self.mark_call()
                return True
