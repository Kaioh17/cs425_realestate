"""
renters.py

Responsibilities:
- Renter account workflows: registration and profile management.
- Manage renter payment methods and addresses (add/modify/delete), enforcing rules
	such as "billing address cannot be deleted if associated with a card".
- Allow renters to view and cancel their bookings.
"""

 

# NOTE: For useful database utilities and table printing helpers, refer to:
# - helper_service.py for query_ class methods (select_all, _insert, _update, _delete_by)
# - helper_service.md for documentation
# - helper_service._Display.pretty_df() for formatting DataFrames as tables

from app.db.connect import get_db
from sqlalchemy import text
from . import helper_service
from .booking import Booking
import pandas as pd 
from .properties import Properties

class Renter:
    db_gen = get_db()
    db = next(db_gen)
    # select = helper_ser
    query = helper_service.query_(db)
    def input(string: str):
        return input(string).strip()
        
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
            email = input("  Email Address[terrel@gmail.com]: ") or 'terrel@gmail.com'
            print()
            move_in_date = input("  When do you plan on moving in? [2025-09-01 00:00:00]: ") or '2025-09-01 00:00:00'
            preferred_location = input("  Preferred Location [Chicago, IL]: ") or 'Chicago, IL'
            budget = input("  Budget [80090]: ") or '80090'
            
            to_dict = {'user': {'role': role,
                        'first_name': first_name.capitalize(),
                    'last_name': last_name.capitalize(),
                    'email': email},
                    'renter': {'id': 0,
                                'move_in_date': move_in_date ,
                                'preferred_location': preferred_location ,
                                'budget': budget }}
        
            

            # print("User: {} agent {}".format(to_dict['user'], to_dict['agent']))
            sql = 'insert into users (role, first_name,last_name, email) values (:role, :first_name, :last_name, :email) returning id'
            
            result = Renter.query._insert(query=sql, params=to_dict['user'])
            user_id = result
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
            email = Renter.input("📧 Email [terrel@gmail.com]: ") or 'terrel@gmail.com'
            # password = input("password: ")
            
            sql = 'select * from users where email = :email'
            # result = Renter.db.execute(sql,{'email':email})
            result = Renter.query.select_all(sql, param={"email":email})
            if len(result) == 0:
                print('\n  ⚠️  User does not exist with this email address.\n')
                ans = input('  Would you like to create a new account? [y/n]: ').lower()
                if ans == 'y':
                    Renter.create_renters()
                    return Renter.signin()
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
            df = pd.DataFrame(response)
            # print("  " + df.to_string(index=False).replace('\n', '\n  '))
            helper_service._Display.pretty_df(df=df, showindex=False)
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
            df = pd.DataFrame(current_resp)
            # print("  " + df.to_string(index=False).replace('\n', '\n  '))
            helper_service._Display.pretty_df(df=df, showindex=False)
            print()
            right = True
            choice = int(input("  Select address ID to update: "))
            while right == True:
                if choice not in df['addr_id'].to_list():
                    choice = int(input('  ❌ Invalid ID. Please enter a valid address ID: ')) 
                else:
                    right = False
                    break
            choice_index = df.index[df['addr_id'] == choice].to_list()
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
            df = pd.DataFrame(current_resp)
            # print("  " + df.to_string(index=False).replace('\n', '\n  '))
            helper_service._Display.pretty_df(df=df, showindex=False)
            print()
            right = True
            choice = int(input("  Select card ID to update: "))
            while right == True:
                if choice not in df['card_id'].to_list():
                    choice = int(input('  ❌ Invalid ID. Please enter a valid card ID: ')) 
                else:
                    right = False
                    break
            choice_index = df.index[df['card_id'] == choice].to_list()
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
            df = pd.DataFrame(response)
            # print("  " + df_from_list.to_string(index=False).replace('\n', '\n  '))
            helper_service._Display.pretty_df(df=df, showindex=False)
            print()
            card_id = int(input('  Enter card ID to delete: '))
            
            if card_id:
                billing_addr_id = df.loc[df["card_id"] == card_id, 'bill_addr_id'].iloc[0]
            # renter_id = response[0]['renter_id']
            sql = 'delete from credit_cards where id = :id and renter_id = :renter_id'
            Renter.query._delete_by(query=sql, param={"id":int(card_id), "renter_id": int(renter_id)})
            sql = "delete from renter_addresses where id = :id and renter_id = :renter_id"
            Renter.query._delete_by(query=sql, param={"id":int(billing_addr_id), "renter_id": int(renter_id)})
            print("\n  ✅ Card and associated address deleted successfully!\n")
            anse = input('  Do you have more cards to delete? [y/n]: ')
            if anse.lower() == 'y':
                return Renter.delete_card(email=email, renter_id=renter_id)
            else:
                return
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def get_rewards(renter_id):
        try:
            select_sql = "select total_points from renter_reward_view where renter_id = :renter_id"
            
            resp =Renter.query.select_all(select_sql, {"renter_id":renter_id})
            if len(resp) == 0:
                print("\n" + "="*80)
                print(" " * 25 + "🎁 REWARD POINTS 🎁")
                print("="*80)
                print("\n  😔 You have not made any bookings with us yet.")
                print("\n  Start booking properties to earn reward points!")
                print("="*80 + "\n")
                return
        
            print("\n" + "="*80)
            print(" " * 25 + "🎁 REWARD POINTS 🎁")
            print("="*80)
            print("\n" + " " * 25 + f"⭐ Your Total Reward Points ⭐")
            print(" " * 30 + f"{round(resp[0]['total_points']):,}")
            print("\n" + "="*80 + "\n")
            
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
        
    def view_bookings(renter_id):
            try:
                select_sql = """
                    select b.id as booking_id, b.start_date, b.end_date, b.price, b.booking_status, p.description, p.location, p.city, c.card_number, c.card_type 
                    from bookings b 
                    left join credit_cards c on b.payment_card_id = c.id 
                    join properties p on b.property_id = p.id 
                    where b.renter_id = :renter_id
                """
                resp = Renter.query.select_all(query = select_sql, param = {"renter_id": renter_id})

                if len(resp) == 0:
                    print("\n" + "="*80)
                    print(" " * 25 + "📋 MY BOOKINGS 📋")
                    print("="*80)
                    print("\n  😔 You do not have any bookings yet!")
                    print("  Start booking properties to see them here!\n")
                    print("="*80 + "\n")
                    return None

                print("\n" + "="*80)
                print(" " * 25 + "📋 MY BOOKINGS 📋")
                print("="*80 + "\n")
                df = pd.DataFrame(resp)
                helper_service._Display.pretty_df(df=df, showindex=False)
                print()
                print("="*80 + "\n")
                return(resp)

            except Exception as e:
                print(f'\n  ❌ An error occurred: {e}\n')
                raise e
            
    def cancel_booking(renter_id):
        """Cancel a booking for the logged-in renter."""
        try:
            # Check if user has any bookings
            resp = Renter.view_bookings(renter_id)
            if resp is None:
                return 
            
            # Filter to show only bookings that can be canceled
            active_bookings = [b for b in resp if b['booking_status'] != 'canceled']
            if len(active_bookings) == 0:
                print("\n  ⚠️  No active bookings to cancel.\n")
                return 
            
            print("\n" + "-"*80)
            booking_id = input("\n  Enter Booking ID to cancel (or press ENTER to go back): ").strip()
            
            if not booking_id:
                print("\n  ⬅️  Returning to menu...\n")
                return
            
            # Verify the booking belongs to this renter and is not already canceled
            booking_ids = [str(b['booking_id']) for b in active_bookings]
            if booking_id not in booking_ids:
                print("\n  ⚠️  Invalid booking ID or booking already canceled.\n")
                return
            
            # Confirm cancellation
            confirm = input(f"\n  ⚠️  Are you sure you want to cancel booking #{booking_id}? [y/n]: ").lower()
            if confirm != 'y':
                print("\n  ⬅️  Cancellation aborted.\n")
                return
            
            # Update booking status to canceled
            update_sql = """
                UPDATE bookings 
                SET booking_status = 'canceled'
                WHERE id = :booking_id AND renter_id = :renter_id
            """
            Renter.query._update(query=update_sql, param={"booking_id": int(booking_id), "renter_id": renter_id})
            
            print("\n" + "="*80)
            print(" " * 25 + "✅ BOOKING CANCELED ✅")
            print("="*80)
            print(f"\n  Booking #{booking_id} has been canceled successfully.")
            print("  💰 Refund will be processed to your saved payment method.\n")
            print("="*80 + "\n")
            
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    
    
    def manage_bookings(renter_id):
        """Booking management menu for renters."""
        try:
            while True:
                print("\n" + "="*80)
                print(" " * 30 + "BOOKING MANAGEMENT")
                print("="*80)
                print("\n  Please select an option:\n")
                print("    [v] View My Bookings")
                print("    [c] Cancel a Booking")
                print("    [ENTER] Go Back")
                print()
                print("-"*80)
                choice = input("\n  Choose an option: ").lower().strip()
                
                match choice:
                    case 'v':
                        Renter.view_bookings(renter_id)
                    case 'c':
                        Renter.cancel_booking(renter_id)
                    case _:
                        print("\n  ⬅️  Returning to main menu...\n")
                        break
                        
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e

    def assign_agent(renter_id: int):
        try:
            print("\n" + "="*80)
            print(" " * 30 + "👤 ASSIGN AGENT 👤")
            print("="*80)
            print("\n  📋 Available Agents:\n")
            select_sql = "select a.id as agent_id, first_name,last_name ,email from agents_profile a join users on users.id = a.id"
            response = helper_service.query_(Renter.db).select_all(query=select_sql)
            helper_service._Display.pretty_df(response)
            print()
            agent_ids = [response[i]["agent_id"] for i in range(len(response))]
            agent_id = int(input("  Enter ID of agent you want to use: "))
            while not agent_id or agent_id not in agent_ids:
                agent_id = int(input("  ❌ Invalid ID. Enter a valid agent ID: "))
                
            insert_sql = "insert into agent_assigned(renter_id, agent_id) values (:renter_id, :agent_id)"
            helper_service.query_(Renter.db)._insert(query=insert_sql,
                                                     params={"renter_id":renter_id, "agent_id":agent_id})
            
            agent_name = f"{response[agent_ids.index(agent_id)]['first_name']} {response[agent_ids.index(agent_id)]['last_name']}"
            print("\n" + "="*80)
            print(" " * 25 + "✅ AGENT ASSIGNED SUCCESSFULLY ✅")
            print("="*80)
            print(f"\n  You are now assigned to Agent #{agent_id}: {agent_name}\n")
            print("="*80 + "\n")
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
    def get_agent_info(renter_id):
        try:
            select_sql = "select a.agency_id, aa.agent_id from agent_assigned aa join agents_profile a on  a.id = aa.agent_id where renter_id = :renter_id"
            response = helper_service.query_(Renter.db).select_all(query = select_sql,param={"renter_id": renter_id})
            if response == []:
                print("\n  ⚠️  You are not assigned to an agent yet.\n")
                ans = input("  Would you like to select an agent? [y/n]: ")
                if ans.lower() == 'y':
                    return Renter.assign_agent(renter_id=renter_id)
                else: 
                    return None
            agent_info = response[0]
            return agent_info
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
                        # token_created = 'token'
                        b=True
                    case _:
                        print('\n  ❌ Invalid choice. Please select 1 or 2.\n')
                        b = True
                
            print(f"\n{'='*80}")
            print(f" " * 25 + f"👋 Welcome back, {email}! 🌟")
            print(f"{'='*80}\n")
            
            booking = Booking(get_db=Renter.db_gen, db=Renter.db, id=renter_id)
            
            while token_created == 'token':
                print("\n" + "="*80)
                print(" " * 35 + "🏠  MAIN MENU")
                print("="*80)
                print("\n  What would you like to do?\n")
                print("    [1] Payment Management")
                print("    [2] Address Management")
                print("    [b] Manage Bookings")
                # print("    [e] Edit Profile")
                print("    [r] See reward points")
                print("    [p] Browse Properties")
                print("    [bn] Start new Bookings")
                print("    [5] Assign Agent")
                
                
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
                        agent_info = Renter.get_agent_info(renter_id=renter_id)
                        agent_id = agent_info["agent_id"]
                        agency_id = agent_info["agency_id"]
                        Properties(db=Renter.db, db_gen=Renter.db_gen, agent_id=agent_id, agency_id=agency_id).cli(role=role)
                    case 'r':
                        Renter.get_rewards(renter_id)
                    case 'b':
                        Renter.manage_bookings(renter_id)
                    case 'bn':
                        print()
                        booking.book_cli(renter_email=email)
                    case '5':
                        Renter.assign_agent(renter_id=renter_id)
                    
        except Exception as e:
            print(f'\n  ❌ An error occurred: {e}\n')
            raise e
        
    
if __name__ == '__main__':
    Renter.cli()
