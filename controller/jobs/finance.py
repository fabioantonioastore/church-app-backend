from controller.crud.community import CommunityCrud
from controller.crud.finance import FinanceCrud
from datetime import datetime
from controller.src.finance import (
    create_finance_in_database,
    get_total_available_money_from_finances_obj,
    FinanceType,
)
import calendar

community_crud = CommunityCrud()
finance_crud = FinanceCrud()
DEFAULT_TITLE = "Last Month"


async def calc_community_available_money() -> None:
    actual_year = datetime.now().year
    actual_month = datetime.now().month

    if actual_month == 1:
        last_month = 12
        last_year = actual_year - 1
    else:
        last_month = actual_month - 1
        last_year = actual_year

    DEFAULT_TITLE = ""

    communities = await community_crud.get_all_communities()

    for community in communities:

        last_month_total_payment = community.last_month_total_payment_value

        finance_data = {
            "title": "Dizimo",
            "value": last_month_total_payment,
            "community_id": community.id,
            "date": datetime(
                year=last_year,
                month=last_month,
                day=calendar.monthrange(last_year, last_month)[1],
                hour=23,
                minute=59,
                second=59,
            ),
            "type": FinanceType.INPUT,
        }

        await create_finance_in_database(finance_data)

        last_month_finances = await finance_crud.get_finances_by_month(
            last_year, last_month, community.id
        )
        total_available_money = get_total_available_money_from_finances_obj(
            last_month_finances
        )

        finance_data = {
            "title": DEFAULT_TITLE,
            "value": total_available_money,
            "community_id": community.id,
            "date": datetime(year=actual_year, month=actual_month, day=1),
            "type": FinanceType.INPUT,
        }

        await create_finance_in_database(finance_data)
