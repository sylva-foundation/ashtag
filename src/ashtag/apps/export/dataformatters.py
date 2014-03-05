import StringIO
import csv


class BaseFormatter(object):
    send_header = False
    file_ext = None

    def __init__(self, collection):
        self.collection = collection
        self.sent_header = False

    def __iter__(self):
        return self

    def next(self):
        if self.send_header and not self.sent_header:
            self.sent_header = True
            return self.format_header()
        return self.format_record(self.collection.next())

    def format_header(self):
        raise NotImplemented()

    def format_record(self, record):
        raise NotImplemented()


class CsvFormatter(BaseFormatter):
    send_header = True
    file_ext = 'csv'

    def get_csv_row(self, values):
        csv_file = StringIO.StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(values)
        return csv_file.getvalue()

    def format_header(self):
        return self.get_csv_row(self.collection.fields)

    def format_record(self, record):
        values = []
        for field in self.collection.fields:
            values.append(record.get(field, None))
        return self.get_csv_row(values)

