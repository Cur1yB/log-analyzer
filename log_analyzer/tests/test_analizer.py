import pytest
from log_analyzer.analizer import Analyzer
import json
from collections import defaultdict


@pytest.fixture
def analyzer():
    return Analyzer()


@pytest.fixture
def sample_log_file(tmp_path):
    data = [
        {
            "@timestamp": "2023-01-01T12:00:00+00:00",
            "url": "/api/users",
            "response_time": 0.2,
        },
        {
            "@timestamp": "2023-01-01T12:01:00+00:00",
            "url": "/api/products",
            "response_time": 0.3,
        },
        {
            "@timestamp": "2023-01-02T12:00:00+00:00",
            "url": "/api/users",
            "response_time": 0.1,
        },
    ]
    file_path = tmp_path / "test.log"
    with open(file_path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return file_path


@pytest.fixture
def sample_log_file_invalid(tmp_path):
    file_path = tmp_path / "invalid.log"
    with open(file_path, "w") as f:
        f.write("invalid json\n")
    return file_path


class TestAnalyzer:
    def test_row_generator_success(self, analyzer, sample_log_file):
        gen = analyzer.row_generator(str(sample_log_file))
        first_line = next(gen)
        assert json.loads(first_line)["url"] == "/api/users"

    def test_row_generator_file_not_found(self, analyzer):
        with pytest.raises(FileNotFoundError):
            next(analyzer.row_generator("nonexistent.log"))

    def test_get_response_time_basic(self, analyzer):
        crude = defaultdict(lambda: {"sum_response_time": 0, "count": 0})
        line = {
            "@timestamp": "2023-01-01T12:00:00+00:00",
            "url": "/test",
            "response_time": 0.5,
        }
        analyzer.get_response_time(line, crude)
        assert crude["/test"]["sum_response_time"] == 0.5
        assert crude["/test"]["count"] == 1

    def test_get_response_time_date_filter_match(self, analyzer):
        crude = defaultdict(lambda: {"sum_response_time": 0, "count": 0})
        line = {
            "@timestamp": "2023-01-01T12:00:00+00:00",
            "url": "/test",
            "response_time": 0.5,
        }
        analyzer.get_response_time(line, crude, "2023-01-01")
        assert crude["/test"]["count"] == 1

    def test_get_response_time_date_filter_no_match(self, analyzer):
        crude = defaultdict(lambda: {"sum_response_time": 0, "count": 0})
        line = {
            "@timestamp": "2023-01-01T12:00:00+00:00",
            "url": "/test",
            "response_time": 0.5,
        }
        analyzer.get_response_time(line, crude, "2023-01-02")
        assert "/test" not in crude or crude["/test"]["count"] == 0

    def test_get_response_time_missing_fields(self, analyzer):
        crude = defaultdict(lambda: {"sum_response_time": 0, "count": 0})
        line = {"@timestamp": "2023-01-01T12:00:00+00:00"}
        with pytest.raises(KeyError):
            analyzer.get_response_time(line, crude)

    def test_make_table_response_time(self, analyzer):
        crude = defaultdict(lambda: {"sum_response_time": 0, "count": 0})
        crude["/api1"]["sum_response_time"] = 1.5
        crude["/api1"]["count"] = 3
        crude["/api2"]["sum_response_time"] = 2.0
        crude["/api2"]["count"] = 4

        table = analyzer.make_table_response_time(crude)
        assert len(table) == 2
        assert table[0][0] == "/api1"
        assert table[0][2] == 0.5  # 1.5 / 3

    def test_analyze_rows_success(self, analyzer, sample_log_file):
        result = analyzer.analyze_rows([str(sample_log_file)], "average")
        assert len(result) == 2  # 2 unique URLs
        assert any(row[0] == "/api/users" for row in result)

    def test_analyze_rows_date_filter(self, analyzer, sample_log_file):
        result = analyzer.analyze_rows([str(sample_log_file)], "average", "2023-01-01")
        assert len(result) == 2  # 2 URLs from 2023-01-01

    def test_analyze_rows_invalid_json(self, analyzer, sample_log_file_invalid):
        with pytest.raises(json.JSONDecodeError, match="Wrong format of log file"):
            analyzer.analyze_rows([str(sample_log_file_invalid)], "average")

    def test_analyze_rows_invalid_report_name(self, analyzer, sample_log_file):
        with pytest.raises(KeyError):
            analyzer.analyze_rows([str(sample_log_file)], "invalid_report")

    def test_analyze_rows_empty_files(self, analyzer):
        with pytest.raises(ValueError):
            analyzer.analyze_rows([], "average")
