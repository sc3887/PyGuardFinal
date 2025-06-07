import csv
import datetime
from importlib.metadata import version


class Version:
    def __init__(self,summary, description):
        self.hashCode = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-{summary}-{'hash'}"
        self.date = datetime.datetime.now()
        self.summary = summary
        self.description = description
