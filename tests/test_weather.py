import unittest
from unittest.mock import patch
from services.weather import get_weather

class TestWeatherService(unittest.TestCase):
    @patch('services.weather.requests.get')
    def test_get_weather_success(self, mock_get):
        # Мок ответа API с 4 элементами в списке
        mock_response = {
            "main": {"temp": 25},
            "weather": [{"description": "clear", "icon": "01d"}],
            "list": [
                {"dt": 1620000000, "main": {"temp": 26}, "weather": [{"icon": "01n"}]},
                {"dt": 1620003600, "main": {"temp": 24}, "weather": [{"icon": "02n"}]},
                {"dt": 1620007200, "main": {"temp": 23}, "weather": [{"icon": "03n"}]},
                {"dt": 1620010800, "main": {"temp": 22}, "weather": [{"icon": "04n"}]}  # Добавлен 4-й элемент
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status.return_value = None

        result = get_weather()
        self.assertEqual(len(result["forecast"]), 3)  # Теперь будет 3 элемента