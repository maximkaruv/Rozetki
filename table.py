import csv
import os

class CsvTable:
    def __init__(self, filename, headers=None):
        self.filename = filename
        self.headers = headers
        # Файл создаём и пишем заголовки, если они есть
        file_exists = os.path.exists(self.filename)
        self.file = open(self.filename, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        if headers and not file_exists:
            self.writer.writerow(headers)
            self.file.flush()

    def add(self, *args):
        self.writer.writerow(args)
        self.file.flush()

    def close(self):
        self.file.close()
