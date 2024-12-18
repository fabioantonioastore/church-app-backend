import csv
import io

from watchfiles import awatch

from models import Finance
from controller.crud.finance import FinanceCrud
from fastapi import HTTPException, status
from typing import List
import datetime
from dataclasses import dataclass
from typing import Union, NamedTuple, TypedDict

class ResumeDict(TypedDict):
    input: float
    output: float
    recipe: float
    last_month: float

FINANCE_TYPE = Union[dict, Finance]
DEFAULT_TITLE = "Last Month"

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

async def get_csv_finance_resume(finances: [Finance], date: DateYearMonth = None):
   pass

def get_finance_resume(finances: [Finance]) -> dict:
    finance_resume = ResumeDict(input=0, output=0, last_month=0, recipe=0)
    for finance in finances:
        if finance.title == DEFAULT_TITLE:
            finance_resume['last_month'] = finance.value
            continue
        if finance.type == FinanceType.INPUT:
            finance_resume['input'] += finance.value
        elif finance.type == FinanceType.OUTPUT:
            finance_resume['output'] += finance.value
    recipe = finance_resume['input'] - finance_resume['output']
    finance_resume['recipe'] = recipe
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

async def update_finance_months_by_finance_data(finance_data: FinanceData) -> None:
    finances = await finance_crud.get_finances_where_date_is_greater_than(finance_data.date)
    if finances:
        if finance_data.type == FinanceType.INPUT:
            for finance in finances:
                update_data = {"value": finance.value + finance_data.value}
                await finance_crud.update_finance_by_id(finance.id, update_data)
        elif finance_data.type == FinanceType.OUTPUT:
            for finance in finances:
                update_data = {"value": finance.value - finance_data.value}
                await finance_crud.update_finance_by_id(finance.id, update_data)

def create_finance_model(finance_data: dict) -> Finance:
    finance = Finance()
    for key in finance_data:
        match key:
            case "title":
                finance.title = finance_data['title']
            case "description":
                finance.description = finance_data['description']
            case "date":
                finance.date = finance_data['date']
            case "value":
                finance.value = finance_data['value']
            case "community_id":
                finance.community_id = finance_data['community_id']
            case "type":
                if is_available_type(finance_data['type']):
                    finance.type = finance_data['type']
                else:
                    raise HTTPException(detail="Invalid finance type: (input/output)", status_code=status.HTTP_400_BAD_REQUEST)
    return finance

def is_available_type(finance_type: str) -> bool:
    return finance_type == FinanceType.INPUT or finance_type == FinanceType.OUTPUT

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
        "id": finance.id
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

def get_total_available_money_from_finances_obj(finances: List[Finance] | List[dict] | dict) -> float:
    total_amount = 0
    for finance in finances:
        if type(finance) == dict:
            if finance['type'] == FinanceType.INPUT:
                total_amount += finance['value']
            else:
                total_amount -= finance['value']
        elif type(finance) == Finance:
            if finance.type == FinanceType.INPUT:
                total_amount += finance.value
            else:
                total_amount -= finance.value
        else:
            raise HTTPException(detail="An unexpected error occurs, report it to dev", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return round(total_amount, 2)

def is_actual_month_and_year(finance: Finance) -> bool:
    actual_date = datetime.datetime.now()
    return (
        finance.date.month == actual_date.month and
        finance.date.year == actual_date.year
    )
