import unittest

from manager_cw_bot_api import get_business_conn_and_info_conn


class Test(unittest.TestCase):
    """
    Class for the unit tests.
    """
    def testGetBusinessConn(self) -> None:
        """
        Test for the get business connection | First test - for false.

        :return: None.
        """
        false: bool = False
        res: bool = get_business_conn_and_info_conn.gets("Not")['ok']
        self.assertEqual(false, res)

    def testGetBusinessConnSecond(self) -> None:
        """
        Test for the get business connection | Second test - for true.

        :return: None.
        """
        true: bool = True
        res: bool = get_business_conn_and_info_conn.gets("6805567328:AAEOORdRjKqdv8wv_TxHlqMtE7gzaX_iIc4")['ok']
        self.assertEqual(true, res)

    def testGetBusinessConnThirdForContent(self) -> None:
        """
        Test for the get business connection | Third test - for NOT FOUND-data.

        :return: None.
        """
        n_f: str = 'Not Found'
        res: str = get_business_conn_and_info_conn.gets("Not Found")['description']
        self.assertEqual(n_f, res)


if __name__ == '__main__':
    unittest.main()
