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
from datetime import date, datetime
from .properties import Properties



class Booking:
    # db_gen = get_db()
    # db = next(db_gen)
    # id = 4
    
    def __init__(self, get_db, db, id):
        self.id = id
        self.db = db
        self.get_db = get_db
        self.query = query_(db)
        
    def mask_card(self, card_number: str):
        return f"**** **** **** {card_number[-4:]}"

    def _months_between(self, start: date, end: date) -> int:
        months = (end.year - start.year) * 12 + (end.month - start.month)
        if end.day < start.day:
            months -= 1
        return max(1, months)

    def _get_monthly_rate(self, property_id: int) -> float:
        # determine property type
        select_sql = "select id, type, price from properties where id = :id"
        resp = self.query.select_all(query=select_sql, param={"id": property_id})
        if len(resp) == 0:
            raise ValueError('Property not found')
        prop = resp[0]
        ptype = prop['type']
        # Try to pull rental_price from related type table
        if ptype in ['apartments', 'houses', 'commercial_buildings']:
            sel = f"select rental_price from {ptype} where property_id = :id"
            r = self.query.select_all(query=sel, param={"id": property_id})
            if len(r) > 0 and r[0].get('rental_price') is not None:
                return float(r[0]['rental_price'])
        # fallback to properties.price
        return float(prop['price'])

    def book_cli(self, renter_email):
        from .renters import Renter
        
        try:
            print("\n" + "="*80)
            print(" " * 30 + "📅 MAKE A BOOKING 📅")
            print("="*80)

            # email = input("  Enter your email (for renter lookup) [rentertest@gmail.com]: ") or 'rentertest@gmail.com'
            # email = renter_email
            # user = self.query.select_all(query="select * from users where email = :email", param={"email": email})
            # if len(user) == 0:
            #     print("\n  ⚠️  No renter found with that email. Please create an account first.\n")
            #     return
            # renter_id = user[0]['id']
            renter_id = self.id
            # Show available properties
            select_sql = "select a.agency_id, aa.agent_id from agent_assigned aa join agents_profile a on  a.id = aa.agent_id where renter_id = :renter_id"
            response = query_(self.db).select_all(query = select_sql,param={"renter_id": renter_id})
            if response == []:
                print("you are not assigned to an agent!!!")
                return 
            agent_id = response[0]["agent_id"]
            agency_id = response[0]["agency_id"]
            
            Properties(db=self.db, 
                       db_gen=self.get_db, 
                       agency_id=agency_id,
                       agent_id=agent_id)._get_property_data()

            prop_id_raw = input("  Enter property ID to book: ")
            if not prop_id_raw or not prop_id_raw.isdigit():
                print("  ⚠ Invalid property id. Aborting.")
                return
            property_id = int(prop_id_raw)

            # dates
            sd_raw = input("  Start date (YYYY-MM-DD) [2025-12-01]: ") or '2025-12-01'
            ed_raw = input("  End date (YYYY-MM-DD) [2026-06-01]: ") or '2026-06-01'
            try:
                start_date = datetime.fromisoformat(sd_raw).date()
                end_date = datetime.fromisoformat(ed_raw).date()
            except Exception:
                print("  ⚠ Invalid date format. Use YYYY-MM-DD.")
                return
            if end_date <= start_date:
                print("  ⚠ End date must be after start date.")
                return

            # Payment methods
            cards = self.query.select_all(query="select id, card_number, card_type from credit_cards where renter_id = :renter_id", param={"renter_id": renter_id})
            if len(cards) == 0:
                print("\n  ⚠ No payment methods found. Please add a card first.\n")
                ans = input("  Would you like to add a card now? [y/n]: ")
                if ans.lower() == 'y':
                    Renter.add_card(renter_email, renter_id)
                    cards = self.query.select_all(query="select id, card_number, card_type from credit_cards where renter_id = :renter_id", param={"renter_id": renter_id})
                else:
                    return

            df_cards = pd.DataFrame(cards)
            helper_service._Display.pretty_df(df_cards, showindex=False)
            card_choice = input("  Select card ID to use for payment: ")
            if not card_choice.isdigit():
                print("  ⚠ Invalid card selection.")
                return
            card_id = int(card_choice)
            chosen = None
            for c in cards:
                if c['id'] == card_id:
                    chosen = c
                    break
            if chosen is None:
                print("  ⚠ Card not found.")
                return

            # compute pricing (monthly)
            months = self._months_between(start_date, end_date)
            monthly_rate = self._get_monthly_rate(property_id=property_id)
            total = round(months * monthly_rate, 2)

            # persist booking
            insert_sql = "insert into bookings (renter_id, property_id, start_date, end_date, payment_card_id, price, booking_status) values (:renter_id, :property_id, :start_date, :end_date, :payment_card_id, :price, :booking_status) returning id"
            params = {
                'renter_id': renter_id,
                'property_id': property_id,
                'start_date': start_date,
                'end_date': end_date,
                'payment_card_id': card_id,
                'price': total,
                'booking_status': 'pending'
            }
            resp = self.query._insert(query=insert_sql, params=params)
            # booking_id = resp.scalar() if resp is not None else None
            booking_id = resp
            # display booking details
            details = [{
                'booking_id': booking_id,
                'renter_id': renter_id,
                'property_id': property_id,
                'rental_period': f"{start_date} to {end_date}",
                'months': months,
                'monthly_rate': monthly_rate,
                'total_cost': total,
                'payment_method': f"{chosen['card_type'].upper()} {self.mask_card(chosen['card_number'])}",
                'status': 'pending'
            }]
            
            df = pd.DataFrame(details)
            print("\n" + "-"*80)
            print("  ✅ Booking created — details below:")
            helper_service._Display.pretty_df(df=df, showindex=False)
            print("-"*80 + "\n")
            return details

        except Exception as e:
            print(f"\n  ❌ An error occurred while creating booking: {e}\n")
            raise e
