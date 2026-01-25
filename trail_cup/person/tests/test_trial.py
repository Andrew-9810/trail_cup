from django.test import TestCase
from person.views import converter_time, add_simbol_zero


class FuncTest(TestCase):
    """Тест функций."""

    def test_converter_time(self):
        """Тест функции converter_time"""
        hour = 60*60
        minute = 60
        data = (
            ('11:37:19', 11 * hour + 37 * minute + 19),
            ('01:07:09', 1 * hour + 7 * minute + 9),
            (11 * hour + 37 * minute + 19, '11:37:19'),
            (1 * hour + 7 * minute + 9, '01:07:09'),
            (0 * hour + 37 * minute + 0, '00:37:00'),
        )
        for i in data:
            result = converter_time(i[0])
            answer = i[1]
            self.assertEqual(result, answer)

    def test_add_simbol_zero(self):
        data = (
            (0, '00'), (33, '33')
        )
        for i in data:
            result = add_simbol_zero(i[0])
            answer = i[1]
            self.assertEqual(result, answer)