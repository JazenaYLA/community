# Copyright (C) 2014 Robby Zeitfuchs (@robbyFux)
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


class DownloaderCabby(Signature):
    name = "downloader_cabby"
    description = "Suspicious downloader (Cabby)"
    severity = 3
    categories = ["downloader"]
    families = ["Cabby"]
    authors = ["Robby Zeitfuchs"]
    minimum = "0.5"
    references = [
        "https://malwr.com/analysis/MmM0NDA5NWU5NjVmNDE5OGJmZmQ1MTdiZWVkMmU2ZDE/",
        "https://malwr.com/analysis/MmNmM2YxOWJhY2QxNDYyYTk3Y2IyNzI4NjQ0ZTEzOGY/",
    ]

    def run(self):
        match_mutex = self.check_mutex(pattern=".*[0-9]{8}", regex=True)

        if match_mutex:
            self.data.append({"mutex": match_mutex})
        else:
            return False

        match_cab_file = self.check_file(pattern=r".*\\Temp\\temp_cab_[0-9]*\.cab", regex=True)

        if match_cab_file:
            self.data.append({"cab_file": match_cab_file})
        else:
            return False

        match_connectivity_check = self.check_domain(pattern="windowsupdate.microsoft.com")

        if match_connectivity_check:
            self.data.append({"connectivity_check": match_connectivity_check})
        else:
            return False

        return True
