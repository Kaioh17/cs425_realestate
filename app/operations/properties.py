from app.db.connect import get_db
from sqlalchemy import text
from . import helper_service
from .helper_service import query_
import pandas as pd
# pd =pd.set_option('display.float_format', '{:,.2f}'.format)

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
   
    def filter_search(self,ineq_dict: dict, type,order_by = None, **filter):
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
            for key, value in filter.items():
                if value is not None:
                    if key == 'location' or key == 'building_type':
                
                        conditions.append(f"lower({key}) like concat('%', :{key}, '%')")
                    elif key == 'price' or key == 'rental_price' or key == 'sqr_footage':
                        
                        if key == 'price':
                            gt = ineq_dict['gt']  
                            lt = ineq_dict['lt'] 
                        elif key == 'sqr_footage':
                            gt = ineq_dict['sgt']  
                            lt = ineq_dict['slt'] 

                        else:
                            gt = ineq_dict['rgt']  
                            lt = ineq_dict['rlt']                  
                            
        
                        if gt != 0 and lt != 0:
                            conditions.append(f"{key} >= {gt} and {key} <= {lt}")
                            
                        elif lt != 0:
                            conditions.append(f"{key} <= {lt}")
                        elif gt != 0:
                            conditions.append(f"{key} >= {gt}")

                    else:
                        conditions.append(f"{key} = :{key}")
                    params[key] = value
                
            where_filters=" or ".join(conditions) if conditions else "1=1"
            where_clause = f" where ({where_filters}) and availability = 't'" 
            order_clause = f", ".join(order_by) if order_by else ""
            order_stmt = f" order by {order_clause}" if order_by else ""
        
            select_sql = f"select price,{display[type]},location, type ,description, crime_rates from properties join {type} on {type}.property_id = properties.id {where_clause} {order_stmt}"
            resp = query_(db=self.db).select_all(query=select_sql, param=params)
            # pd.options.display.float_format = '{:,.2f}'.format
            
            df = pd.DataFrame(resp)
            # df_styled = df.style.format(formatter="{:,.2f}", subset=pd.IndexSlice[:, df.select_dtypes(float).columns])
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
            building_types = query_(db=self.db).select_all(query='select distinct building_type from apartments')
            crime_rate = 'High, Medium, Low'
            # print(building_types)
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
# - Search by location, rental/sale type, number of bedrooms, price range, property type, and desired date.

            ineq_dict = {}
            print()
            location = input('  Location (press Enter to skip): ').lower() or None
            n_rooms = input('  Number of rooms (press Enter to skip): ').lower() or None if type not in no_bed else None
            price_range = input('  Filter by sale price range? [y|n] (press Enter to skip): ').lower() or None
            match price_range:
                case 'y':
                    print("   (press Enter to skip either field)")
                    gt_raw = input('   Minimum price: ')
                    lt_raw = input('   Maximum price: ')
                    
                    ineq_dict['gt'] = int(gt_raw) if gt_raw.strip() else 0
                    ineq_dict['lt'] = int(lt_raw) if lt_raw.strip() else 0
                    
            rent_price = input('  Filter by rental price range? [y|n] (press Enter to skip): ').lower() or None if type not in no_rent else None
            match rent_price:
                case 'y':
                    print("   (press Enter to skip either field)")
                    gt_raw = input('   Minimum rental price: ')
                    lt_raw = input('   Maximum rental price: ') 
                    
                    ineq_dict['rgt'] = int(gt_raw) if gt_raw.strip() else 0
                    ineq_dict['rlt'] = int(lt_raw) if lt_raw.strip() else 0
                    
                    # print(f"Ineq {ineq_dict}")
            sqr_footage = input('  Filter by square footage? [y|n] (press Enter to skip): ').lower() or None
            match sqr_footage:
                case 'y':
                    print("   (press Enter to skip either field)")
                    gt_raw = input('   Minimum square footage: ')
                    lt_raw = input('   Maximum square footage: ')
                    
                    ineq_dict['sgt'] = int(gt_raw) if gt_raw.strip() else 0
                    ineq_dict['slt'] = int(lt_raw) if lt_raw.strip() else 0
            print(f"\n  Available crime rates: {crime_rate}")
            crime_rate = input('  Crime rate (press Enter to skip): ').capitalize() or None
            
            # query_(db=self.db)._print_all(result=building_types)
            building_type_list = [building_types[i]['building_type'] for i in range(len(building_types))]
            print(f'\n  Available building types: {building_type_list}') or None if type == 'apartments' else None
            building_type = input('  Building type (press Enter to skip): ').lower() or None if type == 'apartments' else None
            
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
            rank_type = input('  Sort order (ascending/descending)? [asc/desc|no]: ')  or 'no'
            while rank_type not in ['asc', 'desc', 'no']:
                rank_type = input('  Enter a valid sort order [asc/desc|no]: ') or 'no'
                
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
                print(f"\n  ✓ Results will be sorted by: {', '.join(order_by).replace('_', ' ').title().replace('Sqr', 'Square')}")
            print()
            
                
            self.filter_search(ineq_dict=ineq_dict, order_by=order_by,type=type, price = price_range, num_rooms = n_rooms,
                               rental_price = rent_price,building_type=building_type, crime_rates =crime_rate,
                               sqr_footage=sqr_footage ,location=location)
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