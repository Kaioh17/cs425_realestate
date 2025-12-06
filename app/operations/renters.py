"""
renters.py

Responsibilities:
- Renter account workflows: registration and profile management.
- Manage renter payment methods and addresses (add/modify/delete), enforcing rules
	such as "billing address cannot be deleted if associated with a card".
- Allow renters to view and cancel their bookings.
"""

# Implementation notes:
# - Use secure storage for payment metadata (do not store raw card numbers).
# - Validate address/payment relationships before delete operations.

from app.db.connect import get_db
from sqlalchemy import text
from . import helper_service
from app.db.schemas import UserCreate, AgentCreate
import pandas as pd 
from .properties import Properties

class Renter:
    db_gen = get_db()
    db = next(db_gen)
    # select = helper_ser
    query = helper_service.query_(db)
    
    def create_renters():
        try:
            print("\n" + "="*50)
            print("📝 RENTER REGISTRATION")
            print("="*50)
            print("\n  Let's get you set up! 🚀\n")
            role = 'renter'
            print("  Please provide the following information:\n")
            first_name = input("  First Name [Terrel]: ") or 'Terrel'
            last_name = input("  Last Name [Williams]: ") or 'Williams'
            email = input("  Email Address: ")
            print()
            move_in_date = input("  When do you plan on moving in? [2025-09-01 00:00:00]: ") or '2025-09-01 00:00:00'
            preferred_location = input("  Preferred Location [Chicago, IL]: ") or 'Chicago, IL'
            budget = input("  Budget [80090]: ") or '80090'
            
            to_dict = {'user': {'role': role,
                        'first_name': first_name.capitalize(),
                    'last_name': last_name.capitalize(),
                    'email': email or 'terrel@gmail.com'},
                    'renter': {'id': 0,
                                'move_in_date': move_in_date ,
                                'preferred_location': preferred_location ,
                                'budget': budget }}
        
            

            # print("User: {} agent {}".format(to_dict['user'], to_dict['agent']))
            sql = 'insert into users (role, first_name,last_name, email) values (:role, :first_name, :last_name, :email) returning id'
            
            result = Renter.query._insert(query=sql, params=to_dict['user'])
            user_id = result.scalar()
            # print(f"result: {user_id}")
            to_dict['renter']['id'] = user_id
            sql_agent = 'insert into renters_profile (id, move_in_date, preferred_location, budget) values (:id, :move_in_date, :preferred_location, :budget)'
            # print(f"result: {sql_agent}")
            
            Renter.query._insert(query=sql_agent, params=to_dict['renter'])
            
            print("\n" + "="*80)
            print(" " * 20 + "✅ CONGRATULATIONS ON JOINING OUR PLATFORM! 🎉")
            print("="*80)
            print("\n  Your account has been created successfully!")
            print("  You can now sign in and start searching for properties.\n")
            return
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def signin():
        try:
            print("\n" + "="*50)
            print("🔐 RENTER LOGIN")
            print("="*50 + "\n")
            email = input("📧 Email [terrel@gmail.com]: ") or 'terrel@gmail.com'
            # password = input("password: ")
            
            sql = 'select * from users where email = :email'
            # result = Renter.db.execute(sql,{'email':email})
            result = Renter.query.select_all(sql, param={"email":email})
            if len(result) == 0:
                print('\n  ⚠️  User does not exist with this email address.\n')
                ans = input('  Would you like to create a new account? [y/n]: ').lower()
                if ans == 'y':
                    return Renter.create_renters()
                else:
                    print('\n  Returning to main menu...\n')
                    return  None
            # result = result.fetchone()
            # print(result)
            return result
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    ###Address management
    
    def add_card(email, renter_id):
        try:
            print("\n" + "="*50)
            print("💳 ADD NEW CARD")
            print("="*50)
            print("\n  💰 Card Details:\n")
            card_number = input("    Card Number [34353435344]: ") or '34353435344'
            card_type = input("    Card Type [visa|mastercard]: ").lower() or 'visa'
            card_exp_month = int(input("    Expiration Month [08]: ") or 8)
            card_exp_year = int(input("    Expiration Year [2029]: ") or 2029)
            print("\n  📍 Billing Address:\n")
            street = input("    Street [1234 S TestAddress]: ") or '1234 S TestAddress'
            city = input("    City [Chicago]: ") or 'Chicago'
            state = input("    State [IL]: ").capitalize() or 'IL'
            zip = input("    Zip Code [60872]: ") or '60872'
            """
                BEGIN TRANSACTION;
                    
                    INSERT INTO  renter_addresses (renter_id, street, city, state, zip) VALUES (:renter_id, :street, :city, :state, :zip) returning id;
                    INSERT INTO credit_cards (renter_id, card_number, card_type, billing_address_id, expiration_month, expiration_year) VALUES (:renter_id, :card_number, :card_type, :billing_address_id, :expiration_month, :expiration_year);

                COMMIT TRANSACTION;
            """
            """WITH NewData AS (
                    SELECT 'Value1' AS ColA, 'Value2' AS ColB
                )
                INSERT INTO Table1 (ColumnA, ColumnB)
                SELECT ColA, ColB FROM NewData;

                WITH MoreNewData AS (
                    SELECT 'Value3' AS ColX, 'Value4' AS ColY
                )
                INSERT INTO Table2 (ColumnX, ColumnY)
                SELECT ColX, ColY FROM MoreNewData;"""
            # print(f'email {email}')
            
            insert_ra_sql=text("INSERT INTO  renter_addresses (renter_id, street, city, state, zip) VALUES (:renter_id, :street, :city, :state, :zip) returning id")
            insert_cc_sql=text("INSERT INTO credit_cards (renter_id, card_number, card_type, billing_address_id, expiration_month, expiration_year) VALUES (:renter_id, :card_number, :card_type, :billing_address_id, :expiration_month, :expiration_year) ")
        
            insert_response = Renter.db.execute(insert_ra_sql, {'renter_id':renter_id, 'street':street, 
                                                        'city': city, 'state': state, 'zip': zip})
            billing_address_id = insert_response.scalar()
            # print(billing_address_id)
            Renter.db.execute(insert_cc_sql, {'renter_id':renter_id,'card_number':card_number,
                                                'card_type':card_type, 'billing_address_id':billing_address_id, 
                                                'expiration_month':card_exp_month,
                                                'expiration_year': card_exp_year})
            Renter.db.commit()
            print(f"\n  ✅ Card ending in {card_number[-4:]} has been added successfully!\n")
            return 
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def get_agent():
        try:
            print('\n  📋 Renter details:\n')
            # Feature implementation coming soon
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def delete_address(email, renter_id):
        try:
            select_sql = """select ra.id, ra.street,c.card_number, ra.renter_id  from renter_addresses ra 
                            join credit_cards c on ra.id = c.billing_address_id where ra.renter_id = :renter_id""" 
                               
            response = Renter.query.select_all(query=select_sql, param={'renter_id':renter_id})
            if len(response) == 0:
                print("\n  ⚠️  No addresses available to delete.\n")
                ans = input("  Would you like to add a new card? [y/n]: ")
                if ans.lower() == 'y':
                    Renter.add_card(email, renter_id)
                return
            print("\n" + "="*80)
            print(" " * 30 + "🗑️  DELETE ADDRESS")
            print("="*80)
            print("\n  📋 Your Addresses:\n")
            df_from_list = pd.DataFrame(response)
            print("  " + df_from_list.to_string(index=False).replace('\n', '\n  '))
            print()
            to_delete = input("  Enter ID(s) to delete (comma-separated, e.g., 1,2,3): ").split(',')
            delete_sql = 'delete from renter_addresses where id = :id and renter_id = :renter_id'
            for i in range(len(to_delete)):
                Renter.query._delete_by(query=delete_sql,
                                        param={"id":int(to_delete[i]), 
                                            "renter_id": renter_id})
            print("\n  ✅ Address(es) deleted successfully!\n")
            ans = input("  Do you have more addresses to delete? [y/n]: ")
            if ans.lower() == 'y':
                return Renter.delete_address(renter_id=renter_id, email=email)
            else:
                return
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def update_address(renter_id, email):
        try:
            print("\n" + "="*50)
            print("✏️  UPDATE ADDRESS")
            print("="*50)
            update_sql = 'update renter_addresses set street = :street, city = :city, state = :state, zip = :zip where id=:id '
            select_sql = "select id as addr_id, street, city, state, zip from renter_addresses where renter_id = :renter_id"
            current_resp = Renter.query.select_all(query=select_sql, param={"renter_id":renter_id})
            if len(current_resp) == 0:
                print("\n  ⚠️  No addresses available to update.\n")
                ans = input("  Would you like to add a new card? [y/n]: ")
                if ans.lower() == 'y':
                    Renter.add_card(email, renter_id)
                return
            print("\n  📋 Your Addresses:\n")
            df_from_list = pd.DataFrame(current_resp)
            print("  " + df_from_list.to_string(index=False).replace('\n', '\n  '))
            print()
            right = True
            choice = int(input("  Select address ID to update: "))
            while right == True:
                if choice not in df_from_list['addr_id'].to_list():
                    choice = int(input('  ❌ Invalid ID. Please enter a valid address ID: ')) 
                else:
                    right = False
                    break
            choice_index = df_from_list.index[df_from_list['addr_id'] == choice].to_list()
            choice_index = choice_index[0]
            
            print("\n  💡 Leave blank to keep current value:\n")
            street = input(f"    Street (current: {current_resp[choice_index]['street']}): ") or current_resp[choice_index]['street']
            city = input(f"    City (current: {current_resp[choice_index]['city']}): ") or current_resp[choice_index]['city']
            state = input(f"    State (current: {current_resp[choice_index]['state']}): ") or current_resp[choice_index]['state']
            zip = input(f"    Zip Code (current: {current_resp[choice_index]['zip']}): ") or current_resp[choice_index]['zip']
        
            Renter.query._update(query=update_sql, param={"street":street, "city":city,"state":state,"zip":zip, "id": choice})
            print("\n  ✅ Address updated successfully!\n")
            return 
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    ###card management
    def update_card(renter_id, email):
        try:
            print("\n" + "="*50)
            print("✏️  UPDATE CARD")
            print("="*50)
            update_sql = 'update credit_cards set card_number = :card_number, expiration_month = :expiration_month, expiration_year = :expiration_year where id=:id'
            select_sql = "select id as card_id, card_number, card_type, expiration_month as exp_month, expiration_year as exp_year from credit_cards where renter_id = :renter_id"
            current_resp = Renter.query.select_all(query=select_sql, param={"renter_id":renter_id})
            if len(current_resp) == 0:
                print("\n  ⚠️  No cards available to update.\n")
                ans = input("  Would you like to add a new card? [y/n]: ")
                if ans.lower() == 'y':
                    Renter.add_card(email, renter_id)
                return
            
            print("\n  📋 Your Cards:\n")
            df_from_list = pd.DataFrame(current_resp)
            print("  " + df_from_list.to_string(index=False).replace('\n', '\n  '))
            print()
            right = True
            choice = int(input("  Select card ID to update: "))
            while right == True:
                if choice not in df_from_list['card_id'].to_list():
                    choice = int(input('  ❌ Invalid ID. Please enter a valid card ID: ')) 
                else:
                    right = False
                    break
            choice_index = df_from_list.index[df_from_list['card_id'] == choice].to_list()
            choice_index = choice_index[0]
            
            print("\n  💡 Leave blank to keep current value:\n")
            card_number = input(f"    Card Number (current: {current_resp[choice_index]['card_number']}): ") or current_resp[choice_index]['card_number']
            card_type = input(f"    Card Type (current: {current_resp[choice_index]['card_type']}): ") or current_resp[choice_index]['card_type']
            exp_month = input(f"    Expiration Month (current: {current_resp[choice_index]['exp_month']}): ") or current_resp[choice_index]['exp_month']
            exp_year = input(f"    Expiration Year (current: {current_resp[choice_index]['exp_year']}): ") or current_resp[choice_index]['exp_year']
        
            Renter.query._update(query=update_sql, param={"card_number":card_number, "card_type":card_type,"expiration_year":exp_year,"expiration_month":exp_month, "id": choice})
            print("\n  ✅ Card updated successfully!\n")
            return 
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def delete_card(email, renter_id):
        try:
            print("\n" + "="*50)
            print("🗑️  DELETE CARD")
            print("="*50)
            sql = 'select c.id as card_id, c.card_number, c.renter_id, c.billing_address_id as bill_addr_id from credit_cards c join users u on u.id = c.renter_id where u.email = :email'
            response = Renter.query.select_all(query=sql, param={'email':email})
            
            if len(response) == 0:
                print("\n  ⚠️  No cards available to delete.\n")
                ans = input("  Would you like to add a new card? [y/n]: ")
                if ans.lower() == 'y':
                    Renter.add_card(email, renter_id)
                return
            
            print("\n  📋 Your Cards:\n")
            df_from_list = pd.DataFrame(response)
            print("  " + df_from_list.to_string(index=False).replace('\n', '\n  '))
            print()
            card_id = int(input('  Enter card ID to delete: '))
            
            if card_id:
                billing_addr_id = df_from_list.loc[df_from_list["card_id"] == card_id, 'bill_addr_id'].iloc[0]
            # renter_id = response[0]['renter_id']
            sql = 'delete from credit_cards where id = :id and renter_id = :renter_id'
            Renter.query._delete_by(query=sql, param={"id":int(card_id), "renter_id": int(renter_id)})
            sql = "delete from renter_addresses where id = :id and renter_id = :renter_id"
            Renter.query._delete_by(query=sql, param={"id":int(billing_addr_id), "renter_id": int(renter_id)})
            print("\n  ✅ Card and associated address deleted successfully!\n")
            anse = input('  Do you have more cards to delete? [y/n]: ')
            if anse.lower() == 'y':
                return Renter.delete_card(email=email)
            else:
                return
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def cli():
        """
        Interactive CLI for renter account management.
        Stage 1: Authentication (sign in or create account)
        Stage 2: Operations menu (payment, address, profile management)
        Returns: None
        """
        try:
            b = True
            while b == True:
                print("\n" + "="*80)
                print(" " * 30 + "👋 WELCOME TO RENTER PORTAL 🌟")
                print("="*80)
                print("\n  Please select an option:\n")
                print("    [1] Sign In")
                print("    [2] Create Account")
                print()
                print("-"*80)
                decision = input("\n  Choose an option: ")
                match decision:
                    case '1':
                        # print('feature coming up soon...')
                        response = Renter.signin()
                        if response is None:
                            return
                        email = response[0]['email']
                        # print(email)
                        
                        renter_id = response[0]['id']
                        role = response[0]['role']
                        token_created = 'token'
                        b=False
                    case '2': 
                        Renter.create_renters()
                        token_created = 'token'
                        b=False
                    case _:
                        print('\n  ❌ Invalid choice. Please select 1 or 2.\n')
                        b = True
                
            print(f"\n{'='*80}")
            print(f" " * 25 + f"👋 Welcome back, {email}! 🌟")
            print(f"{'='*80}\n")
                
            while token_created == 'token':
                print("\n" + "="*80)
                print(" " * 35 + "🏠  MAIN MENU")
                print("="*80)
                print("\n  What would you like to do?\n")
                print("    [1] Payment Management")
                print("    [2] Address Management")
                print("    [e] Edit Profile")
                print("    [p] Browse Properties")
                print("    [q] Quit")
                print()
                print("-"*80)
                selection = input("\n  Choose an option: ").lower()
                match selection:
                    case 'q':
                        print("\n  ✅ Thank you for using Renter Portal. Goodbye! 👋\n")
                        break
                    case 'e':
                        print("\n  🔄 Edit Profile feature coming soon...\n")
                        pass
                    case '1':
                        print("\n" + "="*80)
                        print(" " * 30 + "💳 PAYMENT MANAGEMENT")
                        print("="*80)
                        print("\n  Please select an option:\n")
                        print("    [a] Add New Card")
                        print("    [u] Update Card")
                        print("    [d] Delete Card")
                        print("    [ENTER] Go Back")
                        print()
                        print("-"*80)
                        func = input("\n  Choose an option: ")
                        match func:
                            case 'a':
                                Renter.add_card(email, renter_id)
                            case 'd':
                                Renter.delete_card(email, renter_id)
                            case 'u':
                                Renter.update_card(renter_id=renter_id, email=email)
                            case _:
                                print("\n  ⬅️  Returning to main menu...\n")
                    case '2':
                        print("\n" + "="*80)
                        print(" " * 30 + "📍 ADDRESS MANAGEMENT")
                        print("="*80)
                        print("\n  Please select an option:\n")
                        print("    [u] Update Address")
                        print("    [d] Delete Address (⚠️  Associated card will be deleted too)")
                        print("    [ENTER] Go Back")
                        print()
                        print("-"*80)
                        func = input("\n  Choose an option: ").lower()
                        match func:
                            case 'u':
                                Renter.update_address(renter_id=renter_id, email=email)
                            case 'd':
                                Renter.delete_address(email, renter_id=renter_id)                            
                            case _:
                                print("\n  ⬅️  Returning to main menu...\n")
                    case 'p':
                        Properties(db=Renter.db, db_gen=Renter.db_gen).cli(role=role)
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
if __name__ == '__main__':
    Renter.cli()
    