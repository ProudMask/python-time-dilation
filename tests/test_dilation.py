import json
import subprocess
import sys
import unittest
from main import C_M_PER_S, calculate, speed_m_per_s


class DilationTests(unittest.TestCase):
    def test_reference_values(self):
        self.assertEqual(calculate(0, 'm/s', 10)['proper_elapsed_time'], 10)
        self.assertAlmostEqual(calculate(60, '% of c', 10)['lorentz_factor'], 1.25)
        self.assertAlmostEqual(calculate(80, '% of c', 10)['proper_elapsed_time'], 6)

    def test_unit_consistency(self):
        for speed, unit in [(1000, 'm/s'), (1, 'km/s'), (3600, 'km/h')]:
            self.assertAlmostEqual(speed_m_per_s(speed, unit), 1000)

    def test_inverse_conversion(self):
        result = calculate(80, '% of c', 6, time_frame='proper')
        self.assertAlmostEqual(result['observer_elapsed_time'], 10)
        self.assertEqual(result['proper_elapsed_time'], 6)

    def test_invalid_speed(self):
        for speed, unit in [(-1, 'm/s'), (C_M_PER_S, 'm/s'), (100, '% of c'), (101, '% of c'), (float('nan'), 'm/s'), (float('inf'), 'm/s'), (True, 'm/s'), (1, 'mph')]:
            with self.subTest(speed=speed, unit=unit), self.assertRaises(ValueError):
                calculate(speed, unit, 1)

    def test_invalid_time(self):
        for elapsed in (-1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                calculate(10, '% of c', elapsed)
        self.assertEqual(calculate(10, '% of c', 0)['proper_elapsed_time'], 0)

    def test_cli(self):
        result = subprocess.run([sys.executable, 'main.py', '--speed', '80', '--time', '10'], capture_output=True, text=True, check=True, timeout=10)
        self.assertAlmostEqual(json.loads(result.stdout)['proper_elapsed_time'], 6)
        invalid = subprocess.run([sys.executable, 'main.py', '--speed', '100', '--time', '10'], capture_output=True, text=True, timeout=10)
        self.assertNotEqual(invalid.returncode, 0)
        self.assertNotIn('Traceback', invalid.stderr)

    def test_import_without_gui(self):
        result = subprocess.run([sys.executable, '-c', 'import main'], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
