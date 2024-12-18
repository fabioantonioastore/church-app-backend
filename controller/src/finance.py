from watchfiles import awatch

from models import Finance
from controller.crud.finance import FinanceCrud
from fastapi import HTTPException, status
from typing import List
import datetime
from dataclasses import dataclass
from typing import Union

FINANCE_TYPE = Union[dict, Finance]

@dataclass
class FinanceData:
    value: float
    type: str
    date: datetime

class FinanceType:
    INPUT = "input"
    OUTPUT = "output"

finance_crud = FinanceCrud()

DEFAULT_TITLE = "Last Month"

async def get_finance_resume(finances: [Finance], year: int = None, month: int = None) -> dict:
    finance_resume = {
        "input": 0,
        "output": 0,
        "last_recipe": 0,
        "recipe": 0
    }

    for finance in finances:
        match finance.type:
            case "input":
                finance_resume['input'] += finance.value
            case "output":
                finance_resume['output'] -= finance.value

    finance_resume['recipe'] = finance_resume['input'] - finance_resume['output']

    if year and not month:
        last_recipe = await finance_crud.get_finance_last_month_obj_by_date(year - 1, 12)
        if last_recipe:
            finance_resume['last_recipe'] = last_recipe
    elif year and month:
        last_recipe = await finance_crud.get_finance_last_month_obj_by_date(year, month)
        if last_recipe:
            finance_resume['last_recipe'] = last_recipe
    return finance_resume

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
