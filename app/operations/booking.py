"""
booking.py

Responsibilities:
- Create and manage property bookings (select property, rental period, payment method).
- Calculate total cost for booking periods and persist booking records.
- Allow renters and agents to view and cancel bookings; handle refund routing.
"""

# Implementation notes:
# - Integrate with Payment and Property models; record payment method and status.
# - Enforce availability checks before creating a booking.
from app.db.connect import get_db
from sqlalchemy import text
from . import helper_service
from app.db.schemas import UserCreate, AgentCreate
from .helper_service import query_
class Agent:
    db_gen = get_db()
    db = next(db_gen)
    
    def get_all_bookings():
        try:
            sql = "select * from bookings"
            
            result = query_(db=Agent.db).select_all(query=sql)
            
            return result
        except Exception as e:
            raise e
    
if __name__ == '__main__':
    Agent.get_all_bookings()