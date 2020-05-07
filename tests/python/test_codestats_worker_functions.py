import json
import re
import codestats_worker

XPS_DICT = {
    "C": 15,
    "Python": 20,
    "VimL": 7
}


def test_timestamp_format():
    ts = codestats_worker.get_timestamp()
    assert re.match(
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$', ts)


def test_xps_conversion():
    xps_list = codestats_worker.get_xps_list(XPS_DICT)
    _assert_correct_converted_xps_list(xps_list)


def test_payload():
    payload = codestats_worker.get_payload(XPS_DICT)
    data = json.loads(payload)
    keys = data.keys()

    assert len(keys) == 2
    assert "coded_at" in keys
    assert "xps" in keys
    _assert_correct_converted_xps_list(data["xps"])


def _assert_correct_converted_xps_list(xps_list):
    assert len(xps_list) == 3
    assert {"language": "C", "xp": 15} in xps_list
    assert {"language": "Python", "xp": 20} in xps_list
    assert {"language": "VimL", "xp": 7} in xps_list
