import os
from tempfile import TemporaryFile, NamedTemporaryFile
from zipfile import ZipFile


class BaseWriter(object):

    def __init__(self, formatter):
        """

        :param formatter: ashtag.apps.export.dataformatters.BaseFormatter
        """
        self.formatter = formatter

    def __enter__(self):
        self.obj = self.do_it()
        return self.obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if  exc_type is not None:
            # Exception occurred
            self.finish(self.obj)
            # Return False to raise the exception
            return False

        self.finish(self.obj)
        return True

    def do_it(self):
        raise NotImplemented()

    def finish(self, obj):
        pass


class FileWriter(BaseWriter):

    def __init__(self, formatter, compress=True, compressed_name=None):
        super(FileWriter, self).__init__(formatter)
        self.compress = compress
        self.compressed_name = compressed_name

    def do_it(self):
        if self.formatter.file_ext:
            suffix = '.%s' % self.formatter.file_ext
        else:
            suffix = None

        with NamedTemporaryFile(mode='wb', suffix=suffix, delete=self.compress) as f:
            for record in self.formatter:
                f.write(record)

            if not self.compress:
                file_name = f.name
            else:
                f.flush()

                if self.compressed_name:
                    compressed_name = self.compressed_name
                else:
                    compressed_name = os.path.basename(f.name)
                file_name = '%s.zip' % f.name
                with ZipFile(file_name, mode='w') as zip:
                    zip.write(f.name, arcname=compressed_name)

        return open(file_name)

    def finish(self, f):
        f.close()
        os.unlink(f.name)
