from app.db.connect import get_db
from sqlalchemy import text
from . import helper_service
from .helper_service import query_
import pandas as pd
from tabulate import tabulate

# NOTE: For useful database utilities and table printing helpers, refer to:
# - helper_service.py for query_ class methods (select_all, _insert, _update, _delete_by)
# - helper_service.md for documentation
# - helper_service._Display.pretty_df() for formatting DataFrames as tables

"""
### 4.3 Search for Properties

- Search by location, rental/sale type, number of bedrooms, price range, property type, and desired date.
- Only available properties meeting all criteria are shown.
- Results display price, bedrooms, property type, and description.
- Users can sort results by price or number of bedrooms.
"""

class Properties: 
    def __init__(self, db_gen, db):
        self.db_gen = db_gen    
        self.db = db
   
    def filter_search(self, type,rank=None,order_by = None, **filter):
        try:
            
            conditions = []
            params = {}
            ## 
            display = {
                "vacation_homes": "num_rooms, sqr_footage",
                "commercial_buildings": "sqr_footage, rental_price",
                "houses" : "num_rooms, rental_price, sqr_footage, house_availability, nearby_schools",
                "apartments": "num_rooms, building_type,rental_price, sqr_footage, nearby_schools",
                "land": "sqr_footage"
            }
            rank_dict = {
                "desc": " desc ",
                "asc": " asc "
            }
            for key, value in filter.items():
                if value is not None:
                    conditions.append(f"{key} = :{key}")
                    params[key] = value
                    
            where_filters=" and ".join(conditions) if conditions else "1=1"
            # print(where_filters)
            where_clause = f" where {where_filters}" 
            # print(where_clause)
            # order = 'desc_asc'
            print(order_by)
            
            # print("rank",desc_asc)
            order_clause = f", ".join(order_by) if order_by else ""
            order_stmt = f" order by {order_clause}" if order_by else ""
            # TODO add asc and desc order
            select_sql = f"select price,{display[type]}, type ,description from properties join {type} on {type}.property_id = properties.id {where_clause} {order_stmt}"
            print(select_sql)
            # return
            resp = query_(db=self.db).select_all(query=select_sql, param=params)
            df = pd.DataFrame(resp)
            
            # Display results in a user-friendly format
            print("\n" + "="*80)
            print(" " * 30 + "SEARCH RESULTS")
            print("="*80)
            if len(df) == 0:
                print("\n  No properties found matching your criteria.\n")
            else:
                print(f"\n  Found {len(df)} property/properties:\n")
                # print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                helper_service._Display.pretty_df(df=df, showindex=False)
                print()
            print("="*80 + "\n")
        except Exception as e:
            raise e
        
    def filter_prints(self):
        try:
            rank_dict = {
                "desc": " desc",
                "asc": " asc"
            }
            order_by = []
            no_rent = ['vacation_homes', 'land']
            no_bed = ['land','commercial_buildings']
            allowed_types = ['vacation_homes', 'land', 'apartments', 'commercial_buildings', 'houses']
            print("\n" + "-"*80)
            print(" " * 25 + "PROPERTY SEARCH")
            print("-"*80)
            print(f"\n  Available property types:")
            for idx, prop_type in enumerate(allowed_types):
                print(f"    [{idx}] {prop_type.replace('_', ' ').title()}")
            print()
            type = input('  * Property Type (enter number or name): ').lower() or 'apartments'
            if type.isdigit() == True:
                type =allowed_types[int(type)]
            while type not in allowed_types:
                print("  ⚠ Invalid property type. Please try again.")
                type = input('  * Enter a valid property type: ').lower() or 'apartments'

            print()
            location = input('  Location (press Enter to skip): ').lower() or None
            if location:
                print(f"  ✓ Searching in: {location.title()}\n")
            
            print("  Sort Options (T = Yes, F = No):")
            print("  " + "-"*76)
            sale_value = input('  Sort by Sale Price? [T|F]: ').upper() or 'F'
            if type not in no_rent:
                rental_price = input('  Sort by Rental Price? [T|F]: ').upper() or 'F'
            else: rental_price = 'F'
            # if type not in no_bed:
            num_rooms = input('  Sort by Number of Bedrooms? [T|F]: ').upper() or 'F' if type not in no_bed else 'F'
            # print(f"{num_rooms}, {sale_value}, {rental_price}")
            rank_type = input('  Sort order (ascending/descending)? [asc/desc|no]: ')
            while rank_type not in ['asc', 'desc', 'no']:
                rank_type = input('  Enter a valid sort order [asc/desc|no]: ')
                
            # if rank_type:
            if rank_type == 'desc' or rank_type == 'asc':
                desc_asc = rank_dict[rank_type] 
                
            
            if sale_value == 'T':
                order_by.append("price") if rank_type == 'no' else order_by.append(f"price{desc_asc}")
            if rental_price == 'T':
                order_by.append("rental_price") if rank_type == 'no' else order_by.append(f"rental_price{desc_asc}")
            if num_rooms == 'T':
                order_by.append("num_rooms") if rank_type == 'no' else order_by.append(f"num_rooms{desc_asc}")
            
            if order_by:
                print(f"\n  ✓ Results will be sorted by: {', '.join(order_by).replace('_', ' ').title()}")
            print()
            
                
            self.filter_search(rank=rank_type, order_by=order_by,type=type, location=location)
        except Exception as e:
            raise e
    def cli(self, role):
        try:
            if role.lower() == 'renter':
                live = True
                print("\n" + "="*80)
                print(" " * 30 + "PROPERTIES MENU")
                print("="*80)
                while live == True:
                    print("\n  What would you like to do today?\n")
                    print("    [s] Search our property library")
                    print("    [q] Quit")
                    print()
                    ans = input('  Enter your choice: ').lower().strip()
                    
                    match ans:
                        case 'q':
                            print("\n  Thank you for using our property search system. Goodbye!\n")
                            break
                        case 's':
                            self.filter_prints()
                        case _:
                            print("\n  ⚠ Invalid option. Please try again.\n")
            
        except Exception as e:
            raise e
if __name__ == "__main__":
    db_gen = get_db()
    db = next(db_gen)
    Properties(db=db, db_gen=db_gen).cli(role = 'renter')