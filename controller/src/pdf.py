from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO

class PDF:
    def __init__(self, in_memory: bool = True) -> None:
        self.in_memory = in_memory
        if self.in_memory:
            self.buffer = BytesIO()
            self.pdf = SimpleDocTemplate(self.buffer)
        else:
            NotImplemented("Feature not implemented yet")
        self.set_pdf_style()

    def set_pdf_style(self, style = None) -> None:
        self.pdf.pagesize = letter

    def build(self, data: list = None) -> None:
        if not data:
            data = []
        self.pdf.build(data)

    def get_file(self) -> bytes:
        if self.in_memory:
            self.buffer.seek(0)
            return self.buffer.getvalue()

    def write(self, data) -> None:
        pass

    def close_buffer(self) -> None:
        if self.in_memory:
            self.buffer.close()

    def __del__(self) -> None:
        self.close_buffer()

    def __repr__(self) -> str:
        return f"PDF({self.in_memory!r})"
