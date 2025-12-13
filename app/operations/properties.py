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
""" **Add/Delete/Modify properties** (agents)"""
class Properties: 
    def __init__(self, db_gen, db, agency_id, agent_id):
        self.db_gen = db_gen    
        self.db = db 
        self.agency_id = agency_id
        self.agent_id = agent_id
        
        
        
    joint_to_agencies = " join agency_property as a on a.property_id  = p.id "
    allowed_types = ['vacation_homes', 'land', 'apartments', 'commercial_buildings', 'houses']
    display = {
                "vacation_homes": "num_rooms, sqr_footage",
                "commercial_buildings": "sqr_footage, rental_price",
                "houses" : "num_rooms, rental_price, sqr_footage, houses_availability, nearby_schools",
                "apartments": "num_rooms, building_type,rental_price, sqr_footage, nearby_schools",
                "land": "sqr_footage"
            }
    property = "price, location, type, description, crime_rates"
    def filter_search(self,ineq_dict: dict, type,order_by = None, **filter):
        try:
            
            conditions = []
            params = {}
        
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
            if type == 'houses':
                where_clause = f" where ({where_filters}) and houses_availability = 't' and availability = 't'" 
            order_clause = f", ".join(order_by) if order_by else ""
            order_stmt = f" order by {order_clause}" if order_by else ""
        
            select_sql = f"select {self.property},{self.display[type]} from properties p {self.joint_to_agencies} join {type} on {type}.property_id = p.id {where_clause} {order_stmt}"
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
     
    ###Agents only
    def add_properties(self, paylaod: dict):
        try:
            # allowed_types = ['vacation_homes', 'land', 'apartments', 'commercial_buildings', 'houses']
            type = paylaod['properties']['type']
            # print(paylaod)
            
            prop_param_placeholders = []
            prop_params = {}
            prop_columns = []
            
            type_param_placeholders = []
            type_params = {}
            type_columns = []
            
            for k, v in paylaod["properties"].items():
                prop_param_placeholders.append(f":{k}")
                prop_params[k] = v
                prop_columns.append(k)
            prop_columns_str = ", ".join(prop_columns)
            
            for k, v in paylaod[type].items():
                type_param_placeholders.append(f":{k}")
                type_params[k] = v
                type_columns.append(k)
            type_columns_str = ", ".join(type_columns)
                
            # print(prop_param_placeholders)  
            # verify = self._verify_agency(property_id = id)    
            
            print("")
            # param = prop_params | type_params
            # print(param)
            prop_values_str = ", ".join(prop_param_placeholders)
            type_values_str = ", ".join(type_param_placeholders)
            
            insert_sql = f"insert into properties ({prop_columns_str}) values ({prop_values_str}) returning id"
            
            insert_sql2 = f"insert into {type} (property_id, {type_columns_str}) values (:property_id, {type_values_str})"""
            insert_sql3 = f"insert into agency_property (property_id, agency_id) values (:property_id, :agency_id)"
            
            try:
                resp = self.db.execute(text(insert_sql), prop_params) ##to properties
                prop_id = resp.scalar()
                
                
                type_params['property_id'] = prop_id
                self.db.execute(text(insert_sql2), type_params)
                
                query_(self.db)._insert(query=insert_sql3,
                                        params={"property_id":prop_id, "agency_id":self.agency_id},
                                        no_commit=True)
                
            except Exception as e:
                print(f"Rollback occured as {e}")
                self.db.rollback()
            
        except Exception as e:
            raise e
        finally:
            self.db.commit()
            print("Insert successfull")
            
            self._get_property_data(type, prop_id)
    
        
    def add_properties_print(self):
        """properties details"""
        dict = {}
        # allowed_types = ['vacation_homes', 'land', 'apartments', 'commercial_buildings', 'houses']
        crime_rates_lst = ['Low', 'High', 'Medium']
        
        # Welcome banner
        print("\n" + "="*80)
        print(" " * 25 + "🏠 ADD NEW PROPERTY 🏠")
        print("="*80)
        
        # Input variables for property creation
        prop_dict = dict['properties'] = {}
        
        # Property type selection
        print("\n" + "-"*80)
        print(" " * 20 + "Step 1: Select Property Type")
        print("-"*80)
        
        print(f"\n  Available property types: {f' | '.join([f"[{t}] "+ self.allowed_types[t].replace('_', ' ').title() for t in range(len(self.allowed_types))])}\n")
        type = prop_dict['type'] = input("  * Enter property type: ").lower() or 'apartments'
        if type.isdigit():
            type = prop_dict['type'] = self.allowed_types[int(type)]
        while type == '' or type not in self.allowed_types:
            print("  ⚠ Invalid property type. Please try again.")
            type = prop_dict['type'] = input("  * Enter a valid type: ").lower() or ''

        # General property information
        print("\n" + "-"*80)
        print(" " * 20 + "Step 2: General Property Information")
        print("-"*80 + "\n")
        prop_dict['description'] = input("  📝 Property description: ") or 'It is a property'
        prop_dict['location'] = input("  📍 Location: ") or '4508 N Danovan'
        prop_dict['state'] = input("  🗺️  State (e.g. IL, AZ): ") or 'IL'
        prop_dict['city'] = input("  🏙️  City: ") or 'Chicago'
        prop_dict['price'] = float(input("  💰 Price: $") or 321432.0)
        availability = prop_dict['availability'] = input("  ✅ Availability (True/False): ") or 'True'
        availability = True if availability.lower() == "true" else False
        crime_rates = prop_dict['crime_rates'] = input(f"  🚨 Crime rates ({', '.join(crime_rates_lst)}): ").capitalize() or 'High'
        while crime_rates is None or crime_rates not in crime_rates_lst:
            print("  ⚠ Invalid crime rate. Please try again.")
            crime_rates = prop_dict['crime_rates'] = input(f"  🚨 Crime rates ({', '.join(crime_rates_lst)}): ").capitalize() or 'High'
            
        # Property type specific information
        print("\n" + "-"*80)
        print(" " * 20 + f"Step 3: {type.replace('_', ' ').title()} Details")
        print("-"*80 + "\n")
        
        match type.lower():
            case 'apartments':
                apt_dict = dict[type] = {}
                apt_dict['num_rooms'] = int(input("  🛏️  Number of rooms: ") or 2)
                apt_dict['sqr_footage'] = float(input("  📐 Square footage: ") or 2)
                apt_dict['building_type'] = input("  🏢 Building type: ").capitalize() or 'High-rise'
                apt_dict['rental_price'] = float(input("  💵 Rental price: $") or 1500.21)
                apt_dict['nearby_schools'] = input("  🎓 Nearby schools: ").capitalize() or 'Kenwood High School'

            case 'houses':
                house_dict = dict[type] = {}
                house_dict['num_rooms'] = int(input("  🛏️  Number of rooms: ") or 2)
                house_dict['sqr_footage'] = float(input("  📐 Square footage: ") or 2)
                house_dict['rental_price'] = float(input("  💵 Rental price: $") or 2)
                availability = house_dict['availability'] = input("  ✅ Availability (True/False): ").lower() or "true"
                availability = True if availability.lower() == "true" else False
                
                house_dict['nearby_schools'] = input("  🎓 Nearby schools: ").capitalize() or 'Kenwood High School'

            case 'commercial_buildings':
                commercial_dict = dict[type] = {}
                commercial_dict['sqr_footage'] = float(input("  📐 Square footage: ") or 2231320)
                commercial_dict['type_of_business'] = input("  🏪 Type of business: ") or 'Baking'
                commercial_dict['rental_price'] = float(input("  💵 Rental price: $") or 122223)

            case 'vacation_homes':
                vacation_dict = dict[type] = {}
                vacation_dict['num_rooms'] = int(input("  🛏️  Number of rooms: ") or 0)
                vacation_dict['sqr_footage'] = float(input("  📐 Square footage: ") or 23234)

            case 'land':
                land_dict = dict[type] = {}
                try:
                    sqr_ft = land_dict['sqr_footage'] = float(input("  📐 Square footage: ") or 232421)
                    while sqr_ft == '':
                        sqr_ft = land_dict['sqr_footage'] = float(input("  ⚠ Enter a valid square footage: ") or 232421)
                except ValueError as t:
                    sqr_ft = land_dict['sqr_footage'] = float(input("  📐 Square footage: ") or 232421)
        
        print("\n" + "="*80)
        print(" " * 30 + "✅ Property Added Successfully!")
        print("="*80 + "\n")

            
        # dict['land']['sqr_footage'] = float(input("Square footage: "))
        
        
        # print(dict)
        return self.add_properties(dict)
    
    def del_properties(self):
        try:
            print("\n" + "="*80)
            print(" " * 25 + "🗑️  DELETE PROPERTY 🗑️")
            print("="*80)
            
            print(" | ".join([f"[{t}]"+self.allowed_types[t].replace('_', ' ').title() for t in range(len(self.allowed_types))]))
            print("[q] quit")
            type = input('Property type or all: ').lower()
            if type == 'q':
                return
            if type and type.isdigit():
                type = self.allowed_types[int(type)]
                
            type_data = self._get_property_data(type=type)
            type_id = [type_data[t]['id'] for t in range(len(type_data))]
            print(type_id)
            # helper_service._Display.pretty_df(response)
            print()
            
            prop_id = input("  Enter property ID to delete: ").strip()
            # response = query_(self.db).select_all(query="select id from properties where id = :id", param={"id": prop_id})
            response = self._verify_agency(property_id= prop_id)
            print(response)
            if len(response) == 0 or int(prop_id) not in type_id:
                print("\n" + "="*40)
                print("  ⚠ Property ID not found in database!")
                print("="*40 + "\n")
                ans = input("  Would you like to try entering a correct ID again? [y|n]: ").lower()
                if ans == 'y':
                    return self.del_properties()
                else:
                    print("\n  ❌ Deletion cancelled.\n")
                    return
            
            print("\n" + "-"*80)
            verify = input("  ⚠ Are you sure you want to delete this property? [y|n]: ").lower()
            
            if verify == 'y':
                delete_sql = """delete from properties where id = :id"""
                query_(self.db)._delete_by(query=delete_sql, param={'id': prop_id})

                
                print("\n" + "="*80)
                print(" " * 30 + "✅ Property Deleted Successfully!")
                print("="*80 + "\n")
                return
            else:
                print("\n" + "-"*80)
                print("  ❌ Deletion process cancelled.")
                print("-"*80 + "\n")
                return 
        except Exception as e:
            raise e
    def _verify_agency(self, property_id:int):
        
        select_sql = "select property_id from agency_property where property_id = :property_id and agency_id = :agency_id"
        repsonse = query_(self.db).select_all(select_sql, param={"property_id": property_id,  "agency_id": self.agency_id})
        return repsonse
    def update_properties(self, dict, id, type_ids):
        try:
            type = dict['properties']['type']
            place_holders=[]
            type_place_holders=[]
            param = {}
            type_param = {}
            for k,v in dict['properties'].items():
                if v is not None:
                    place_holders.append(f"{k} = :{k}")
                    param[k] = v
                
            for k,v in dict[type].items():
                if v is not None:
                    type_place_holders.append(f"{k} = :{k}")
                    type_param[k] = v

            verify = self._verify_agency(property_id = id)    
            
            if len(verify) == 0 or int(id) not in type_ids:
                print("This property is not in your agency")
                return self.update_properties(dict,id)
            
            place_holders = ", ".join(place_holders)
            type_place_holders = ", ".join(type_place_holders)
            update_sql=f"update properties set {place_holders}  where id = {id}"
            type_update_sql=f"update {type} set {type_place_holders}  where property_id = {id}"
            
            if param != {}:
                query_(db=self.db)._update(query=update_sql, param=param)
            if type_param != {}:
                query_(db=self.db)._update(query=type_update_sql, param=type_param) 
            
            

            self._get_property_data(type, id=id)
            insert_sql = "insert into property_update_log(property_id, agent_id) values(:property_id, :agent_id)"
            query_(db=self.db)._insert(query=insert_sql, params={"property_id":id,"agent_id":self.agent_id})
        except Exception as e:
            raise e
    def update_properties_print(self):
        """properties details"""
        dict = {}
        crime_rates_lst = ['Low', 'High', 'Medium']
        
        # Welcome banner
        print("\n" + "="*80)
        print(" " * 25 + "🏠 UPDATE PROPERTIES 🏠")
        print("="*80)
        
        # Input variables for property creation
        prop_dict = dict['properties'] = {}
        
        
        # Property type selection
        print("\n" + "-"*80)
        print(" " * 20 + "Step 1: Select Property Type")
        print("-"*80)
        
        print(f"\n  Available property types: {f' | '.join([f"[{t}] "+ self.allowed_types[t].replace('_', ' ').title() for t in range(len(self.allowed_types))])}\n")
        
        
        type = prop_dict['type'] = input("  * Enter property type: ").lower()
        # if type and type.isdigit():
        #     type = prop_dict['type'] = allowed_types[int(type)]
        while type == '' and (type == '' or type not in self.allowed_types):
            print("  ⚠ Invalid property type. Please try again.")
            type = prop_dict['type'] = input("  * Enter a valid type: ").lower() or None
        if type and type.isdigit():
            type = prop_dict['type'] = self.allowed_types[int(type)]
        type_data = self._get_property_data(type=type)
        type_id = [type_data[t]['id'] for t in range(len(type_data))]
        
        print()
        
        id = input(f"Property id: ")
        # General property information
        print("\n" + "-"*80)
        print(" " * 20 + "Step 2: General Property Information")
        print("-"*80 + "\n")
        prop_dict['description'] = input("  📝 Property description: ") or None
        prop_dict['location'] = input("  📍 Location: ") or None
        prop_dict['state'] = input("  🗺️  State (e.g. IL, AZ): ") or None
        prop_dict['city'] = input("  🏙️  City: ") or None
        price_input = input("  💰 Price: $") or None
        prop_dict['price'] = float(price_input) if price_input else None
        availability_input = input("  ✅ Availability (True/False): ") or None
        if availability_input:
            availability_input = True if availability_input.lower() == "true" else False

        prop_dict['availability'] = availability_input.lower() == 'true' if availability_input else None
        crime_rates = prop_dict['crime_rates'] = input(f"  🚨 Crime rates ({', '.join(crime_rates_lst)}): ").capitalize() or None
        while crime_rates is not None and crime_rates not in crime_rates_lst:
            print("  ⚠ Invalid crime rate. Please try again.")
            crime_rates = prop_dict['crime_rates'] = input(f"  🚨 Crime rates ({', '.join(crime_rates_lst)}): ").capitalize() or None
            
        # Property type specific information
        print("\n" + "-"*80)
        print(" " * 20 + f"Step 3: {type.replace('_', ' ').title()} Details")
        print("-"*80 + "\n")
        
        match type.lower():
            case 'apartments':
                apt_dict = dict[type] = {}
                num_rooms_input = input("  🛏️  Number of rooms: ") or None
                apt_dict['num_rooms'] = int(num_rooms_input) if num_rooms_input else None
                sqr_footage_input = input("  📐 Square footage: ") or None
                apt_dict['sqr_footage'] = float(sqr_footage_input) if sqr_footage_input else None
                apt_dict['building_type'] = input("  🏢 Building type: ") or None
                if apt_dict['building_type']:
                    apt_dict['building_type'] = apt_dict['building_type'].capitalize()
                rental_price_input = input("  💵 Rental price: $") or None
                apt_dict['rental_price'] = float(rental_price_input) if rental_price_input else None
                apt_dict['nearby_schools'] = input("  🎓 Nearby schools: ") or None
                if apt_dict['nearby_schools']:
                    apt_dict['nearby_schools'] = apt_dict['nearby_schools'].capitalize()

            case 'houses':
                house_dict = dict[type] = {}
                num_rooms_input = input("  🛏️  Number of rooms: ") or None
                house_dict['num_rooms'] = int(num_rooms_input) if num_rooms_input else None
                sqr_footage_input = input("  📐 Square footage: ") or None
                house_dict['sqr_footage'] = float(sqr_footage_input) if sqr_footage_input else None
                rental_price_input = input("  💵 Rental price: $") or None
                house_dict['rental_price'] = float(rental_price_input) if rental_price_input else None
                availability_input = input("  ✅ Availability (True/False): ") or None
                if availability_input:
                    availability_input = True if availability_input.lower() == "true" else False
                house_dict['availability'] = availability_input.lower() if availability_input else None
                house_dict['nearby_schools'] = input("  🎓 Nearby schools: ") or None
                if house_dict['nearby_schools']:
                    house_dict['nearby_schools'] = house_dict['nearby_schools'].capitalize()

            case 'commercial_buildings':
                commercial_dict = dict[type] = {}
                sqr_footage_input = input("  📐 Square footage: ") or None
                commercial_dict['sqr_footage'] = float(sqr_footage_input) if sqr_footage_input else None
                commercial_dict['type_of_business'] = input("  🏪 Type of business: ") or None
                rental_price_input = input("  💵 Rental price: $") or None
                commercial_dict['rental_price'] = float(rental_price_input) if rental_price_input else None

            case 'vacation_homes':
                vacation_dict = dict[type] = {}
                num_rooms_input = input("  🛏️  Number of rooms: ") or None
                vacation_dict['num_rooms'] = int(num_rooms_input) if num_rooms_input else None
                sqr_footage_input = input("  📐 Square footage: ") or None
                vacation_dict['sqr_footage'] = float(sqr_footage_input) if sqr_footage_input else None

            case 'land':
                land_dict = dict[type] = {}
                sqr_footage_input = input("  📐 Square footage: ") or None
                if sqr_footage_input:
                    try:
                        land_dict['sqr_footage'] = float(sqr_footage_input)
                    except ValueError:
                        land_dict['sqr_footage'] = None
                else:
                    land_dict['sqr_footage'] = None
        
        print("\n" + "="*80)
        print(" " * 30 + "✅ Property updated Successfully!")
        print("="*80 + "\n")

            
        return self.update_properties(dict, id=id, type_ids = type_id)
    def list_all_properties(self):
        try:
            print("\n" + "="*80)
            print(" " * 25 + "📋 LIST PROPERTIES 📋")
            print("="*80)
            print("\n  How would you like to list properties?\n")
            print("    [a] List all properties")
            print("    [p] List by property type")
            print("    [s] Search with filters")
            print("    [id] Search by id")
            print("    [b] Go back ")
            print()
            option = input("  Enter your choice: ").lower().strip()
            
            match option:
                case "a":
                    print("\n" + "-"*80)
                    print(" " * 30 + "All Properties")
                    print("-"*80 + "\n")
                    # For "all", we need to handle multiple property types
                    # This is a simplified version - you may want to union all types
                    limit = input("Would you like to enter a limit['n' if no | Enter the limit]: ")
                    
                    # select_sql = f"select {self.property} from properties"
                    # response = query_(db=self.db).select_all(query=select_sql, limit=limit)
                    self._get_property_data(limit=limit)
                        
                    
                    
                case "p":
                    print("\n" + "-"*80)
                    print(" " * 25 + "List by Property Type")
                    print("-"*80)
                    print(f"\n  Available property types: {' | '.join([f'[{i}] {t.replace('_', ' ').title()}' for i, t in enumerate(self.allowed_types)])}\n")
                    type = input("  Enter property type (name or number): ").lower().strip()
                    
                    # Handle numeric input
                    if type.isdigit():
                        type = self.allowed_types[int(type)] if int(type) < len(self.allowed_types) else None
                    
                    while not type or type not in self.allowed_types:
                        print("  ⚠ Invalid property type. Please try again.")
                        type = input("  Enter a valid property type: ").lower().strip()
                        if type.isdigit():
                            type = self.allowed_types[int(type)] if int(type) < len(self.allowed_types) else None
                    
                    print("\n" + "-"*80)
                    print(f" " * 25 + f"{type.replace('_', ' ').title()} Properties")
                    print("-"*80 + "\n")
                    
                    select_sql = f"select {self.property}, {self.display[type]} from properties as p join {type} as t on t.property_id = p.id where p.type = :type"
                    response = query_(db=self.db).select_all(select_sql, {"type": type})
                    
                    if response:
                        helper_service._Display.pretty_df(response)
                        print("\n" + "="*80 + "\n")
                    else:
                        print(f"  No {type.replace('_', ' ')} properties found.\n")
                        
                case "s":
                    self.filter_prints()
                case "id":
                    id = input("Enter property id: ")
                    self._get_property_data(id=id)
                case "b":
                    return
                case _:
                    print("\n  ⚠  Invalid option. Please try again.\n")
                    self.list_all_properties()
            cont = input("Do you want to list again: [y|n]").lower()
            
            if cont == "y":
                self.list_all_properties()
            return 
                    
        except Exception as e:
            print(f"\n  ❌ Error listing properties: {e}\n")
            raise e
    
    def filter_prints(self):
        try:
            no_rent = ['vacation_homes', 'land']
            no_bed = ['land','commercial_buildings']
            # allowed_types = ['vacation_homes', 'land', 'apartments', 'commercial_buildings', 'houses']
            building_types = query_(db=self.db).select_all(query='select distinct building_type from apartments')
            crime_rate = 'High, Medium, Low'
            # print(building_types)
            print("\n" + "-"*80)
            print(" " * 25 + "PROPERTY SEARCH")
            print("-"*80)
            print(f"\n  Available property types:")
            for idx, prop_type in enumerate(self.allowed_types):
                print(f"    [{idx}] {prop_type.replace('_', ' ').title()}")
            print()
            type = input('  * Property Type (enter number or name): ').lower() or 'apartments'
            if type.isdigit() == True:
                type =self.allowed_types[int(type)]
            while type not in self.allowed_types:
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

            order_by = self._sort_prints(type=type, no_bed=no_bed, no_rent=no_rent)
                
            self.filter_search(ineq_dict=ineq_dict, order_by=order_by,type=type, price = price_range, num_rooms = n_rooms,
                               rental_price = rent_price,building_type=building_type, crime_rates =crime_rate,
                               sqr_footage=sqr_footage ,location=location)
        except Exception as e:
            raise e
    def _sort_prints(self,type ,no_rent: list, no_bed:list):
        try:
            rank_dict = {
                "desc": " desc",
                "asc": " asc"
            }
            order_by=[]
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
            return order_by
        except Exception as e:
            raise e
        
    def _get_property_data(self, type: str = None, id: int = None, limit: str = None):
        """id: property_id
            type: property type"""
        
        if id and type:
            response =  query_(db = self.db).select_all(query=f"select {self.property}, {self.display[type]} from properties p {self.joint_to_agencies} join {type} as t on p.id = t.property_id where id=:id and agency_id = :agency_id", param={"id":id, "agency_id": self.agency_id}, limit=limit)
           
            print("\n" + "-"*80)
            print(" " * 30 + "Property")
            print("-"*80 + "\n")
        elif type:
            response =  query_(db = self.db).select_all(query=f"select id, {self.property}, {self.display[type]} from properties p {self.joint_to_agencies} join {type} as t on p.id = t.property_id where type=:type and agency_id = :agency_id",
                                                        param={"type": type, "agency_id": self.agency_id}, limit=limit)
            print("\n" + "-"*80)
            print(" " * 30 + f"{type} Properties")
            print("-"*80 + "\n")
        elif id:
            response =  query_(db = self.db).select_all(query=f"select {self.property} from properties p {self.joint_to_agencies} where id=:id and agency_id = :agency_id", param={"id":id, "agency_id": self.agency_id}, limit=limit)
            
            print("\n" + "-"*80)
            print(" " * 30 + "Property")
            print("-"*80 + "\n")
        else:
            for t in self.allowed_types:
                # print(f"select {self.property}, {self.display[t]} from properties p join {t} as t on p.id = t.property_id")

                response =  query_(db = self.db).select_all(query=f"select {self.property}, {self.display[t]} from properties p {self.joint_to_agencies} join {t} as t on p.id = t.property_id where agency_id = :agency_id",
                                                            param={"agency_id": self.agency_id}, limit=limit)
                print("\n" + "-"*80)
                print(" " * 30 + f"{t} Property")
                print("-"*80 + "\n")
                if response:
                    helper_service._Display.pretty_df(response)
                    print("\n" + "="*80 + "\n")
                    
                else: print(f"   No data for {t}")
            return
                
        
        if response:
            helper_service._Display.pretty_df(response)
            print("\n" + "="*80 + "\n")
            return response
        else:
            print("  No properties found.\n")
    def cli(self, role):
        try:
            live = True
            
            
            print("\n" + "="*80)
            print(" " * 30 + "PROPERTIES MENU")
            print("="*80)
            while live == True:
                print("\n  What would you like to do today?\n")
                if role.lower() == 'agent':
                    print("    [d] Delete property")
                    print("    [a] Add new property")
                    print("    [u] Update a property")
                print("    [l] List all property") 
                     
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
                    case 'd':
                        self.del_properties()
                    case 'a':
                        self.add_properties_print()
                    case 'l':
                        self.list_all_properties()
                    case 'u':
                        self.update_properties_print()
                    case _:
                        print("\n  ⚠ Invalid option. Please try again.\n")
                        
            
            
        except Exception as e:
            raise e
if __name__ == "__main__":
    db_gen = get_db()
    db = next(db_gen)
    Properties(db=db, db_gen=db_gen).cli(role = 'agent')