from sqlalchemy.util import await_only
from watchfiles import awatch

from models import Finance
from controller.crud.finance import FinanceCrud

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
                finance.type = finance_data['type']
    return finance

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
