from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """test waiting for db when db is available"""
        with patch("django.db.utils.ConnectionHandler.create_connection") as con:
            con.return_value = True
            call_command("wait_for_db")
            self.assertEqual(con.call_count, 0)

    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch("django.db.utils.ConnectionHandler.create_connection") as con:
            con.side_effect = [OperationalError] * 2 + [True]
            call_command("wait_for_db")
            self.assertEqual(con.call_count, 0)
