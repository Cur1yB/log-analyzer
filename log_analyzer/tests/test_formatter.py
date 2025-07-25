from log_analyzer.formatter import Output
import pytest


# Фикстуры для тестовых данных
@pytest.fixture
def sample_average_data():
    return [
        ["/api/users", 1500, 0.125],
        ["/api/products", 1200, 0.183],
        ["/", 800, 0.056],
    ]


@pytest.fixture
def sample_unsorted_data():
    return [
        ["/api/products", 1200, 0.183],
        ["/", 800, 0.056],
        ["/api/users", 1500, 0.125],
    ]


@pytest.fixture
def empty_data():
    return []


class TestOutput:
    def test_create_table_sorts_correctly(self, sample_unsorted_data):
        """Testing sorting"""
        result = Output.create_table(sample_unsorted_data, sort_by=1)
        lines = result.split("\n")

        # Проверяем порядок строк после сортировки
        assert "1500" in lines[2]  # Первая строка после заголовков
        assert "1200" in lines[3]
        assert "800" in lines[4]

    def test_create_table_headers(self, sample_average_data):
        """Testing headers for average report"""
        result = Output.create_table(sample_average_data)
        assert "handler" in result
        assert "total" in result
        assert "avg_response_time" in result

    def test_create_table_empty_data(self, empty_data):
        """Testing empty data"""
        result = Output.create_table(empty_data)
        assert "handler" in result
        assert len(result.split("\n")) == 2

    def test_create_table_different_sort_column(self, sample_average_data):
        """Testing different sort column"""
        result = Output.create_table(sample_average_data, sort_by=2)
        lines = result.split("\n")

        # sorting by avg_response_time
        assert "0.183" in lines[2]
        assert "0.056" in lines[4]

    def test_create_table_showindex(self, sample_average_data):
        """testing index correctness"""
        result = Output.create_table(sample_average_data)
        lines = result.split("\n")

        assert "0" in lines[2]
        assert "1" in lines[3]
        assert "2" in lines[4]

    def test_create_table_invalid_sort_column(self, sample_average_data):
        """Negative test for invalid name column for sorting"""
        with pytest.raises(IndexError):
            Output.create_table(sample_average_data, sort_by=10)
