from enum import Enum
from models import Finance
from controller.crud.finance import FinanceCrud

class FinanceType(Enum):
    INPUT = "input"
    OUTPUT = "output"

finance_crud = FinanceCrud()

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
                    raise "Invalid finance type: (input/output)"
    return finance

def is_available_type(finance_type: str) -> bool:
    return ((finance_type == FinanceType.INPUT.value()) or
            (finance_type == FinanceType.OUTPUT.value()))

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

def get_total_available_money_from_finances_obj(finances: [Finance]) -> float:
    total_amount = 0
    for finance in finances:
        if finance.type == FinanceType.INPUT.value():
            total_amount += finance.value
        else:
            total_amount -= finance.value
    return total_amount
