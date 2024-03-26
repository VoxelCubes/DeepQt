from unittest.mock import patch
import deepqt.log_parser as lp
from tests.helpers import read_mock_file
import tests.mock_files.logs as log_files


def test_parse_good():
    # Test with good_pcleaner.log
    logfile = read_mock_file("good.log", module=log_files)
    # mock the get_username function to return "testvm"
    with patch("deepqt.log_parser.get_username", return_value="testvm"):
        sessions = lp.parse_log_file(logfile)

    assert len(sessions) == lp.MAX_SESSIONS
    assert sessions[19].criticals == 1
    assert sessions[19].errors == 3
    assert sessions[1].criticals == 0
    assert sessions[1].errors == 1
    assert sessions[1].corrupted is False
    assert sessions[5].criticals == 0
    assert sessions[5].errors == 0
