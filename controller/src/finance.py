from controller.src.csv_file import CSVFile
from io import StringIO
from models import Finance
from controller.crud.finance import FinanceCrud
from fastapi import HTTPException, status
from typing import List
import datetime
from dataclasses import dataclass
from typing import Union, NamedTuple, TypedDict
from controller.src.pdf_table import PDFTable


class ResumeDict(TypedDict):
    input: float
    output: float
    recipe: float
    last_month: float


FINANCE_TYPE = Union[dict, Finance]
DEFAULT_TITLE = "Last Month"
DATE_FORMAT = "%m-%d-%Y"


@dataclass
class FinanceData:
    value: float
    type: str
    date: datetime


class FinanceType:
    INPUT = "input"
    OUTPUT = "output"


class DateYearMonth(NamedTuple):
    year: int
    month: int


finance_crud = FinanceCrud()

DEFAULT_TITLE = "Last Month"
FINANCE_HEADER = ["Date", "Title", "Type", "Value"]


def get_pdf_table_finance_resume(finances: [Finance]) -> bytes:
    pdf_table = PDFTable()
    pdf_table.set_table_header(FINANCE_HEADER)

    return get_finance_resume_file(finances, pdf_table)


async def get_finance_resume_pdf_year(
    finances: List[Finance], year: int
) -> bytes:
    pdf_table = PDFTable()
    pdf_table.set_table_header(FINANCE_HEADER)

    return await get_finance_resume_by_year_file(finances, year, pdf_table)


def get_csv_finance_resume(finances: [Finance]) -> StringIO:
    csv_file = CSVFile()
    csv_file.set_file_header(FINANCE_HEADER)

    return get_finance_resume_file(finances, csv_file)


async def get_finance_resume_by_year_file(
    finances: List[Finance], year: int, file
):
    recipe = 0
    data = []
    last_month = await finance_crud.get_finance_last_month_obj_by_date(
        year - 1, 12
    )

    for finance in finances:
        if finance.title == DEFAULT_TITLE:
            continue
        recipe = modify_recipe_by_finance(recipe, finance)
        finance_row = get_finance_row(finance)
        data.append(finance_row)

    data = sorted(data, key=parse_date)
    if last_month:
        last_month_row = [
            "",
            "Last Month",
            "input",
            round(last_month.value, 2),
        ]
        data.insert(0, last_month_row)
        recipe = modify_recipe_by_finance(recipe, last_month)
    for row in data:
        file.write(row)

    recipe_row = ["", "Recipe", "input", round(recipe, 2)]
    file.write(recipe_row)

    return file.get_file()


async def get_csv_finance_resume_year(
    finances: List[Finance], year: int
) -> StringIO:
    csv_file = CSVFile()
    csv_file.set_file_header(FINANCE_HEADER)

    return await get_finance_resume_by_year_file(finances, year, csv_file)


def get_finance_resume_file(finances: List[Finance], file):
    recipe = 0
    data = []
    last_month = None

    for finance in finances:
        if finance.title == DEFAULT_TITLE:
            last_month = finance
            recipe = modify_recipe_by_finance(recipe, finance)
            continue
        recipe = modify_recipe_by_finance(recipe, finance)
        finance_row = get_finance_row(finance)
        data.append(finance_row)

    data = sorted(data, key=parse_date)
    if last_month:
        last_month_row = get_finance_row(last_month)
        data.insert(last_month_row)
    for row in data:
        file.write(row)

    recipe_row = ["", "Recipe", "input", round(recipe, 2)]
    file.write(recipe_row)

    return file.get_file()


def parse_date(row) -> datetime:
    return datetime.datetime.strptime(row[0], DATE_FORMAT)


def get_finance_row(finance: Finance) -> list:
    date = get_finance_date_str(finance)
    return [date, finance.title, finance.type, finance.value]


def get_finance_date_str(finance: Finance) -> str:
    date = str(finance.date.month) + "-"
    date += str(finance.date.day) + "-"
    return date + str(finance.date.year)


def modify_recipe_by_finance(recipe: float, finance: Finance) -> float:
    if finance.type == FinanceType.INPUT:
        recipe += finance.value
    elif finance.type == FinanceType.OUTPUT:
        recipe -= finance.value
    return recipe


def get_finance_resume(finances: [Finance]) -> dict:
    finance_resume = ResumeDict(input=0, output=0, last_month=0, recipe=0)
    for finance in finances:
        if finance.title == DEFAULT_TITLE:
            finance_resume["last_month"] = finance.value
            continue
        if finance.type == FinanceType.INPUT:
            finance_resume["input"] += finance.value
        elif finance.type == FinanceType.OUTPUT:
            finance_resume["output"] += finance.value
    recipe = finance_resume["input"] - finance_resume["output"]
    finance_resume["recipe"] = recipe + finance_resume["last_month"]
    finance_resume = rounded_resume(finance_resume)
    return finance_resume


def rounded_resume(resume: dict[str, float]) -> dict:
    for key in resume.keys():
        resume[key] = round(resume[key], 2)
    return resume


def integer_to_month(month: int) -> str:
    match month:
        case 1:
            return "january"
        case 2:
            return "february"
        case 3:
            return "march"
        case 4:
            return "april"
        case 5:
            return "may"
        case 6:
            return "june"
        case 7:
            return "july"
        case 8:
            return "august"
        case 9:
            return "september"
        case 10:
            return "october"
        case 11:
            return "november"
        case 12:
            return "december"
        case _:
            raise "Not valid integer month representation (1 - 12)"


async def update_finance_months_by_finance_data(
    finance_data: FinanceData,
) -> None:
    finances = await finance_crud.get_finances_where_date_is_greater_than(
        finance_data.date
    )
    if finances:
        if finance_data.type == FinanceType.INPUT:
            for finance in finances:
                update_data = {"value": finance.value + finance_data.value}
                await finance_crud.update_finance_by_id(
                    finance.id, update_data
                )
        elif finance_data.type == FinanceType.OUTPUT:
            for finance in finances:
                update_data = {"value": finance.value - finance_data.value}
                await finance_crud.update_finance_by_id(
                    finance.id, update_data
                )


def create_finance_model(finance_data: dict) -> Finance:
    finance = Finance()
    for key in finance_data:
        match key:
            case "title":
                finance.title = finance_data["title"]
            case "description":
                finance.description = finance_data["description"]
            case "date":
                finance.date = finance_data["date"]
            case "value":
                finance.value = finance_data["value"]
            case "community_id":
                finance.community_id = finance_data["community_id"]
            case "type":
                if is_available_type(finance_data["type"]):
                    finance.type = finance_data["type"]
                else:
                    raise HTTPException(
                        detail="Invalid finance type: (input/output)",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
    return finance


def is_available_type(finance_type: str) -> bool:
    return (
        finance_type == FinanceType.INPUT or finance_type == FinanceType.OUTPUT
    )


async def create_finance_in_database(finance_data: dict) -> Finance:
    finance = create_finance_model(finance_data)
    return await finance_crud.create_finance(finance)


def finance_no_sensitive_data(finance: Finance) -> dict:
    return {
        "title": finance.title,
        "description": finance.description,
        "type": finance.type,
        "value": finance.value,
        "date": finance.date,
        "id": finance.id,
    }


def month_to_integer(month: str) -> int:
    month.lower()
    match month:
        case "january":
            return 1
        case "february":
            return 2
        case "march":
            return 3
        case "april":
            return 4
        case "may":
            return 5
        case "june":
            return 6
        case "july":
            return 7
        case "august":
            return 8
        case "september":
            return 9
        case "october":
            return 10
        case "november":
            return 11
        case "december":
            return 12
        case _:
            raise "Month not found"


def get_total_available_money_from_finances_obj(
    finances: List[Finance] | List[dict] | dict,
) -> float:
    total_amount = 0
    for finance in finances:
        if type(finance) == dict:
            if finance["type"] == FinanceType.INPUT:
                total_amount += finance["value"]
            else:
                total_amount -= finance["value"]
        elif type(finance) == Finance:
            if finance.type == FinanceType.INPUT:
                total_amount += finance.value
            else:
                total_amount -= finance.value
        else:
            raise HTTPException(
                detail="An unexpected error occurs, report it to dev",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    return round(total_amount, 2)


def is_actual_month_and_year(finance: Finance) -> bool:
    actual_date = datetime.datetime.now()
    return (
        finance.date.month == actual_date.month
        and finance.date.year == actual_date.year
    )
