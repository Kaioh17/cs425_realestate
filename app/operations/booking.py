"""
booking.py

Responsibilities:
- Create and manage property bookings (select property, rental period, payment method).
- Calculate total cost for booking periods and persist booking records.
- Allow renters and agents to view and cancel bookings; handle refund routing.
"""


# NOTE: For useful database utilities and table printing helpers, refer to:
# - helper_service.py for query_ class methods (select_all, _insert, _update, _delete_by)
# - helper_service.md for documentation
# - helper_service._Display.pretty_df() for formatting DataFrames as tables

from app.db.connect import get_db
from sqlalchemy import text
from . import helper_service
from .helper_service import query_
import pandas as pd

class Agent:
    db_gen = get_db()
    db = next(db_gen)
    
    def get_all_bookings():
        try:
            select_sql = "select renter_id, property_id, start_date, payment_card_id  from bookings"
            
            result = query_(db=Agent.db).select_all(query=select_sql)
            df = pd.DataFrame(result)
            helper_service._Display.pretty_df(df)
            return result
        except Exception as e:
            raise e
   
    def cli():
        try:
            
            Agent.get_all_bookings()

        except Exception as e:
            raise e
if __name__ == '__main__':
    Agent.cli()