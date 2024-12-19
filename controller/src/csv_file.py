import csv
import io

class CSVFile:
    def __init__(self, in_memory: bool = True) -> None:
        self.file_header = None
        self.in_memory = in_memory
        if self.in_memory:
            self.csv_file = io.StringIO()
        else:
            raise NotImplemented("Feature not implemented already")
        self.writer = csv.writer(self.csv_file)

    def set_file_header(self, file_header: list[str], auto_write_header: bool = True) -> None:
        self.file_header = file_header
        if auto_write_header:
            self.write_header()

    def write_header(self) -> None:
        self.writer.writerow(self.file_header)

    def write(self, row_items: list) -> None:
        self.writer.writerow(row_items)

    def get_csv_file(self) -> io.StringIO:
        if self.in_memory:
            self.csv_file.seek(0)
            return self.csv_file
        raise NotImplemented("Feature not implemented already")

    def __repr__(self) -> str:
        return f"CSVFile({self.in_memory!r})"
