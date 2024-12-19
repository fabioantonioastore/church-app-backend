from typing_extensions import override
from controller.src.pdf import PDF
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

class PDFTable(PDF):
    def __init__(self, in_memory: bool = True) -> None:
        super().__init__(in_memory)
        self.style = None
        self.table = None
        self.table_data = []
        self.table_header = []
        self.set_table_style()

    def set_table_header(self, header: list) -> None:
        self.table_header = header
        if len(self.table_data) == 1:
            self.table_data = []
        if not self.table_data:
            self.table_data.append(self.table_header)
        else:
            raise "Table cannot modify it's header"

    @override
    def write(self, row_items: list) -> None:
        if len(row_items) != len(self.table_header):
            raise "Size of row is not equals size of the header"
        self.table_data.append(row_items)

    @override
    def build(self, data = None) -> None:
        self.table = Table(self.table_data)
        self.__set_table_style()
        super().build([self.table])

    @override
    def get_file(self) -> bytes:
        self.build()
        if self.in_memory:
            self.buffer.seek(0)
            return self.buffer.getvalue()

    def set_table_style(self, style: TableStyle = None) -> None:
        if not style:
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
        self.style = style

    def __set_table_style(self) -> None:
        self.table.setStyle(self.style)

    def __repr__(self) -> str:
        return f"PDFTable({self.in_memory!r})"
