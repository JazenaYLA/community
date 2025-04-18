from cape_parsers.CAPE.core.HttpBrowser import extract_config, rule_source
from maco.extractor import Extractor
from maco.model import ExtractorModel as MACOModel

from modules.parsers.utils import get_YARA_rule


def convert_to_MACO(raw_config: dict):
    if not (raw_config and isinstance(raw_config, dict)):
        return None

    parsed_result = MACOModel(family="HttpBrowser", other=raw_config)

    port = raw_config["port"][0] if "port" in raw_config else None

    if "c2_address" in raw_config:
        parsed_result.http.append(MACOModel.Http(uri=raw_config["c2_address"], port=port, usage="c2"))

    if "filepath" in raw_config:
        parsed_result.paths.append(MACOModel.Path(path=raw_config["filepath"]))

    if "injectionprocess" in raw_config:
        parsed_result["injectionprocess"] = raw_config["injectionprocess"]

    return parsed_result


class HttpBrowser(Extractor):
    author = "kevoreilly"
    family = "HttpBrowser"
    last_modified = "2024-10-26"
    sharing = "TLP:CLEAR"
    yara_rule = get_YARA_rule(family)

    yara_rule = rule_source

    def run(self, stream, matches):
        return convert_to_MACO(extract_config(stream.read()))
