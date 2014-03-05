import os.path

from zipfile import ZipFile
from ashtag.apps.export.datacollections import UserCollection
from ashtag.apps.export.dataformatters import CsvFormatter
from ashtag.apps.export.datawriters import FileWriter
from ashtag.apps.export.tests.base import BaseExportTestCase


class BaseWriterTestCase(BaseExportTestCase):
    collection_class = None
    formatter_class = None
    writer_class = None

    def setUp(self):
        super(BaseWriterTestCase, self).setUp()
        self.formatter = self.formatter_class(self.collection)
        self.writer = FileWriter(self.formatter)


class FileWriterTestCase(BaseWriterTestCase):
    collection_class = UserCollection
    formatter_class = CsvFormatter
    writer_class = FileWriter

    def test_standard(self):
        self.writer.compress = False

        with self.writer.do_it() as f:
            data = f.read()
        self.assertEqual(data, 'id,username,email,date_joined\r\n%s,testuser,a@a.com,2012-03-04T12:30:10+00:00\r\n' % self.user.pk)

    def test_compressed_no_name(self):
        self.writer.compress = True

        with self.writer.do_it() as f:
            with ZipFile(f.name) as zipf:
                self.assertEqual(zipf.namelist(), [os.path.basename(f.name).replace('.zip', '')])
                # How big is the compressed file
                info = zipf.getinfo(zipf.namelist()[0])
                self.assertEqual(info.file_size, 77)

                # How big is the zip file
                f.seek(0, 2)
                bytes = f.tell()
                self.assertGreater(bytes, 160)

    def test_compressed_named(self):
        self.writer.compress = True
        self.writer.compressed_name= 'myfile.csv'

        with self.writer.do_it() as f:
            with ZipFile(f.name) as zipf:
                self.assertEqual(zipf.namelist(), ['myfile.csv'])
                # How big is the compressed file
                info = zipf.getinfo('myfile.csv')
                self.assertEqual(info.file_size, 77)

                # How big is the zip file
                f.seek(0, 2)
                bytes = f.tell()
                self.assertGreater(bytes, 160)

                self.assertEqual(zipf.read('myfile.csv'), 'id,username,email,date_joined\r\n%s,testuser,a@a.com,2012-03-04T12:30:10+00:00\r\n' % self.user.pk)