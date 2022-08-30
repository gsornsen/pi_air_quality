import json
from pathlib import Path
from air_quality.emulation import ranges

file_path = Path(__file__)
aggregate_mock_file = file_path.parents[0] / "real_aggregate_mock.json"

def test_ranges_exist_for_all_measurables():
    with open(aggregate_mock_file) as mock_file:
        mock = json.load(mock_file)
        for key in ranges:
            assert key in mock
