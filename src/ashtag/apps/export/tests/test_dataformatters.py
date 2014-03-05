from ashtag.apps.export.datacollections import UserCollection
from ashtag.apps.export.dataformatters import CsvFormatter
from ashtag.apps.export.tests.base import BaseExportTestCase


class BaseFormatterTestCase(BaseExportTestCase):
    collection_class = None
    formatter_class = None

    def setUp(self):
        super(BaseFormatterTestCase, self).setUp()
        self.formatter = self.formatter_class(self.collection)


class CsvFormatterTestCase(BaseFormatterTestCase):
    collection_class = UserCollection
    formatter_class = CsvFormatter

    def test_get_csv_row(self):
        row = self.formatter.get_csv_row(['a', 'b', 3, 'hey, bob'])
        self.assertEqual(row, 'a,b,3,"hey, bob"\r\n')

    def test_format_header(self):
        row = self.formatter.format_header()
        self.assertEqual(row, 'id,username,email,date_joined\r\n')

    def test_iterator(self):
        rows = "".join(self.formatter)
        self.assertEqual(rows, 'id,username,email,date_joined\r\n%s,testuser,a@a.com,2012-03-04T12:30:10+00:00\r\n' % self.user.pk)

