"""
agent.py

Responsibilities:
- Agents: create, update, and delete property listings.
- Provide endpoints/operations for agents to view bookings for their properties.
- Validate agent ownership and enforce agent-specific business rules.
"""



# NOTE: For useful database utilities and table printing helpers, refer to:
# - helper_service.py for query_ class methods (select_all, _insert, _update, _delete_by)
# - helper_service.md for documentation
# - helper_service._Display.pretty_df() for formatting DataFrames as tables

import pandas as pd

from app.db.connect import get_db
from sqlalchemy import text
from . import helper_service, properties
from .helper_service import _Display as d
from pydantic import EmailStr

class Agent:
    db_gen = get_db()
    db = next(db_gen)
    # select = helper_service.query_(db).
    def __init__(self, db_gen, db):
        self.db_gen = db_gen
        self.db = db
    query = helper_service.query_(db)
    def add_agency(self):
        try:
            print("\n" + "="*80)
            print(" " * 25 + "🏢 CREATE NEW AGENCY 🏢")
            print("="*80 + "\n")
            agency_name = input("  🏢 Agency name: ")
            agency_email = input("  📧 Agency email: ")
            
            insert_sql = "insert into agencies(agency_name, agency_email) values (:agency_name, :agency_email) returning id"
            
            response = self.query._insert(insert_sql, params={"agency_name": agency_name, "agency_email" : agency_email})
            return response
        except Exception as e:
            raise e
    def create_agent(self):
        try:
            # from  import Renter
            print("\n" + "="*80)
            print(" " * 25 + "👤 AGENT SIGN UP 👤")
            print("="*80)
            print("\n  Welcome! Let's create your agent account.\n")
            
            select_sql = "select agency_name from agencies"
            resp = self.query.select_all(select_sql)
            if resp == []:
                print("There are no agencies to join...")
                ans = input("would you like to create yours: [y|n] ")
                if ans.lower() == "y":
                    return self.add_agency()
            role = 'agent'
            first_name = input("  📝 First name: ")
            last_name = input("  📝 Last name: ")
            email:EmailStr = input("  📧 Email: ")
            job_title = input("  💼 Job title: ")
            helper_service._Display.pretty_df(resp)
            print("  🏢Enter Agency you will be joining [or else you want to create a new agency they  [y]]: ")
            agency = d.input(   "")
            if agency != "y":
                agency_response = self.query.select_all(query="select id from agencies where agency_name = :agency_name ", param={"agency_name": agency})
                agency_id = agency_response[0]['id']
            if agency == "y":
                agency_id = self.add_agency()
            
            contact_info = input("  📞 Contact info: ")
            
            
            to_dict={'user': {'role': role or 'agent',
                    'first_name': first_name.capitalize() or 'James',
                    'last_name': last_name.capitalize() or 'Lucky',
                    'email': email or 'lucky@gmail.com'},
                    'agent': {'id': 0,
                                    'job_title': job_title or 'agent',
                                'agency_id': agency_id,
                                'contact_info': contact_info or '775-342-2323'}}

            # print(to_dict)
            # user_model = UserCreate(to_dict)
            # Agent.create_agent(to_dict)
            

            # print("User: {} agent {}".format(to_dict['user'], to_dict['agent']))
            sql = 'insert into users (role, first_name, last_name, email) values (:role, :first_name, :last_name, :email) returning id'
            
            result = self.query._insert(query=sql, params=to_dict['user'])
        
            # print(f"result: {user_id}")
            to_dict['agent']['id'] = result
            sql_agent = f'insert into agents_profile (id, job_title, agency_id, contact_info) values (:id, :job_title, :agency_id, :contact_info)'
            # print(f"result: {sql_agent}")
            
            self.query._insert(query=sql_agent, params=to_dict['agent'])
            
            print("\n" + "="*80)
            print(" " * 20 + "🎉 CONGRATULATIONS! YOU ARE NOW AN AGENT! 🎉")
            print("="*80)
            print("\n  Your agent account has been successfully created!\n")
            print("="*80 + "\n")

            return email
        except Exception as e:
            print(f"Error at {e}")
            raise
    def signin(self):
        print("\n" + "="*80)
        print(" " * 30 + "🔐 AGENT SIGN IN 🔐")
        print("="*80 + "\n")
        email = input("  📧 Email: ").strip() or 'admintest@gmail.com'
        # password = input("password: ")
        
        select_sql = 'select *, a.agency_id from users join agents_profile a on a.id = users.id where email = :email'
        
        # result = Agent.db.execute(sql,{'email':email or 'test@dreamhomes.com'})
        result = helper_service.query_(db=self.db).select_all(query=select_sql, param={'email': email})
    
        
        # result = result
        # print(result)
        if len(result) == 0:
            print("\n" + "="*40)
            print("  ⚠ Agent is not in our system!")
            print("="*40 + "\n")
            ans = input("  Would you like to create a new account? [y|n|ENTER to try again]: ").lower()
            match ans:
                case 'y':
                    self.create_agent()
                    return self.signin()
                case 'n':
                    return
                case _:
                    self.signin()
        else:
            print("\n" + "="*80)
            print(" " * 30 + "✅ Sign In Successful!")
            print("="*80 + "\n")
        return result
    def get_agent():
        print("\n" + "="*80)
        print(" " * 30 + "👤 AGENT DETAILS 👤")
        print("="*80 + "\n")
    
    def view_bookings(self, agent_id):
        """View all bookings for renters assigned to this agent."""
        try:
            print(agent_id)
            select_sql = """
                SELECT b.id AS booking_id, 
                    u.first_name || ' ' || u.last_name AS renter_name,
                    u.email AS renter_email,
                    p.description, p.location, p.city,
                    b.start_date, b.end_date, b.price, b.booking_status,
                    c.card_number, c.card_type
                FROM agent_assigned aa
                JOIN bookings b ON aa.renter_id = b.renter_id
                JOIN users u ON b.renter_id = u.id
                JOIN properties p ON b.property_id = p.id
                LEFT JOIN credit_cards c ON b.payment_card_id = c.id
                WHERE aa.agent_id = :agent_id
                ORDER BY b.start_date DESC
            """
            result = self.query.select_all(query=select_sql, param={"agent_id": agent_id})
            
            print("\n" + "="*80)
            print(" " * 25 + " CLIENT BOOKINGS ")
            print("="*80)
            
            if len(result) == 0:
                print("\n  No bookings found for your assigned clients.\n")
                return None
            
            df = pd.DataFrame(result)
            print()
            helper_service._Display.pretty_df(df=df, showindex=False)
            print()
            return result
            
        except Exception as e:
            print(f'Error: {e}')
            raise e

    def cancel_booking(self, agent_id):
        """Cancel a booking for a renter assigned to this agent."""
        try:
            # Show bookings first
            result = self.view_bookings(agent_id)
            if result is None:
                return
            
            # Filter to only active bookings
            active_bookings = [b for b in result if b['booking_status'] != 'canceled']
            if len(active_bookings) == 0:
                print("  No active bookings to cancel.\n")
                return
            
            print("-"*80)
            booking_id = input("\n  Enter Booking ID to cancel (or press ENTER to go back): ").strip()
            
            if not booking_id:
                print("\n  Returning to menu...\n")
                return
            
            # Validate booking ID
            valid_ids = [str(b['booking_id']) for b in active_bookings]
            if booking_id not in valid_ids:
                print("\n  Invalid booking ID or booking already canceled.\n")
                return
            
            # Get booking details for confirmation
            booking_info = next((b for b in active_bookings if str(b['booking_id']) == booking_id), None)
            
            # Show details and confirm
            print(f"\n    Booking Details:")
            print(f"     Renter: {booking_info['renter_name']} ({booking_info['renter_email']})")
            print(f"     Property: {booking_info['description']}")
            print(f"     Dates: {booking_info['start_date']} to {booking_info['end_date']}")
            print(f"     Price: ${booking_info['price']}")
            
            confirm = input(f"\n  Are you sure you want to cancel this booking? [y/n]: ").lower()
            if confirm != 'y':
                print("\n  Cancellation aborted.\n")
                return
            
            # Execute the cancel - note we join through agent_assigned for security
            update_sql = """
                UPDATE bookings 
                SET booking_status = 'canceled'
                WHERE id = :booking_id 
                AND renter_id IN (SELECT renter_id FROM agent_assigned WHERE agent_id = :agent_id)
            """
            self.query._update(query=update_sql, param={"booking_id": int(booking_id), "agent_id": agent_id})
            
            print("\n" + "="*80)
            print(" " * 25 + "✅ BOOKING CANCELED ✅")
            print("="*80)
            print(f"\n  Booking #{booking_id} has been canceled.")
            print(f"  Refund will be processed to {booking_info['renter_name']}'s payment method.\n")
            
        except Exception as e:
            print(f'Error: {e}')
            raise e

    def manage_bookings(self, agent_id):
        """Booking management menu for agents."""
        try:
            while True:
                print("\n" + "="*80)
                print(" " * 30 + "BOOKING MANAGEMENT")
                print("="*80)
                print("\n  Please select an option:\n")
                print("    [v] View Client Bookings")
                print("    [c] Cancel a Booking")
                print("    [ENTER] Go Back")
                print()
                print("-"*80)
                choice = input("\n  Choose an option: ").lower().strip()
                
                match choice:
                    case 'v':
                        self.view_bookings(agent_id)
                    case 'c':
                        self.cancel_booking(agent_id)
                    case _:
                        print("\n  Returning to main menu...\n")
                        break
                        
        except Exception as e:
            print(f'Error: {e}')
            raise e
        
    def view_clients(self, agent_id):
        """View summary of all clients assigned to this agent."""
        try:
            select_sql = """
                SELECT u.id AS client_id,
                    u.first_name || ' ' || u.last_name AS client_name,
                    u.email,
                    rp.preferred_location,
                    rp.budget,
                    COUNT(b.id) AS total_bookings
                FROM agent_assigned aa
                JOIN users u ON aa.renter_id = u.id
                JOIN renters_profile rp ON u.id = rp.id
                LEFT JOIN bookings b ON u.id = b.renter_id
                WHERE aa.agent_id = :agent_id
                GROUP BY u.id, u.first_name, u.last_name, u.email, rp.preferred_location, rp.budget
                ORDER BY u.last_name, u.first_name
            """
            result = self.query.select_all(query=select_sql, param={"agent_id": agent_id})
            
            print("\n" + "="*80)
            print(" " * 30 + " YOUR CLIENTS ")
            print("="*80)
            
            if len(result) == 0:
                print("\n  You have no clients assigned to you yet.\n")
                return None
            
            df = pd.DataFrame(result)
            print()
            helper_service._Display.pretty_df(df=df, showindex=False)
            print()
            return result
            
        except Exception as e:
            print(f'Error: {e}')
            raise e

    def view_client_details(self, agent_id, client_id):
        """View detailed information for a specific client."""
        try:
            # Get client basic info
            client_sql = """
                SELECT u.id, u.first_name, u.last_name, u.email,
                    rp.move_in_date, rp.preferred_location, rp.budget
                FROM users u
                JOIN renters_profile rp ON u.id = rp.id
                JOIN agent_assigned aa ON u.id = aa.renter_id
                WHERE u.id = :client_id AND aa.agent_id = :agent_id
            """
            client = self.query.select_all(query=client_sql, param={"client_id": client_id, "agent_id": agent_id})
            
            if len(client) == 0:
                print("\n  Client not found or not assigned to you.\n")
                return
            
            client = client[0]
            
            print("\n" + "="*80)
            print(f" " * 25 + f" {client['first_name']} {client['last_name']} ")
            print("="*80)
            
            # Basic info
            print(f"\n   Email: {client['email']}")
            print(f"   Preferred Location: {client['preferred_location']}")
            print(f"   Budget: ${client['budget']:,.2f}")
            print(f"   Move-in Date: {client['move_in_date']}")
            
            # Get addresses
            address_sql = """
                SELECT street, city, state, zip
                FROM renter_addresses
                WHERE renter_id = :client_id
            """
            addresses = self.query.select_all(query=address_sql, param={"client_id": client_id})
            
            print("\n  " + "-"*40)
            print("   ADDRESSES")
            print("  " + "-"*40)
            if len(addresses) == 0:
                print("    No addresses on file.")
            else:
                for addr in addresses:
                    print(f"    {addr['street']}, {addr['city']}, {addr['state']} {addr['zip']}")
            
            # Get cards (last 4 digits only)
            card_sql = """
                SELECT card_type, RIGHT(card_number, 4) AS last_four, 
                    expiration_month, expiration_year
                FROM credit_cards
                WHERE renter_id = :client_id
            """
            cards = self.query.select_all(query=card_sql, param={"client_id": client_id})
            
            print("\n  " + "-"*40)
            print("  PAYMENT METHODS")
            print("  " + "-"*40)
            if len(cards) == 0:
                print("    No cards on file.")
            else:
                for card in cards:
                    print(f"    {card['card_type'].capitalize()} ending in {card['last_four']} (Exp: {card['expiration_month']}/{card['expiration_year']})")
            
            # Get bookings
            booking_sql = """
                SELECT b.id AS booking_id, p.description, p.city,
                    b.start_date, b.end_date, b.price, b.booking_status
                FROM bookings b
                JOIN properties p ON b.property_id = p.id
                WHERE b.renter_id = :client_id
                ORDER BY b.start_date DESC
            """
            bookings = self.query.select_all(query=booking_sql, param={"client_id": client_id})
            
            print("\n  " + "-"*40)
            print(" BOOKINGS")
            print("  " + "-"*40)
            if len(bookings) == 0:
                print("    No bookings yet.")
            else:
                df = pd.DataFrame(bookings)
                print()
                helper_service._Display.pretty_df(df=df, showindex=False)
            
            print()
            
        except Exception as e:
            print(f'Error: {e}')
            raise e

    def manage_clients(self, agent_id):
        """Client management menu for agents."""
        try:
            while True:
                # Show client summary
                result = self.view_clients(agent_id)
                
                if result is None:
                    return
                
                print("-"*80)
                client_id = input("\n  Enter Client ID to view details (or press ENTER to go back): ").strip()
                
                if not client_id:
                    print("\n  Returning to main menu...\n")
                    break
                
                # Validate client ID
                valid_ids = [str(c['client_id']) for c in result]
                if client_id not in valid_ids:
                    print("\n  Invalid Client ID. Please try again.\n")
                    continue
                
                # Show client details
                self.view_client_details(agent_id, int(client_id))
                
                input("  Press ENTER to continue...")
                        
        except Exception as e:
            print(f'Error: {e}')
            raise e
            
    def cli(self):
        token_created = None
        while token_created is None:
            print("\n" + "="*80)
            print(" " * 25 + "🌟 AGENT PORTAL 🌟")
            print("="*80)
            print("\n  Hello there! Please choose an option:\n")
            print("    [1] Sign in")
            print("    [2] Create an agent account")
            print()
            decision = int(input("  Enter your choice: "))
            match decision:
                case 1:
                    resp = self.signin()
                    role = resp[0]['role']
                    agency_id = resp[0]['agency_id']
                    agent_id = resp[0]['id']
                    print(f"  Role: {role}\n")
                    token_created = 'token'
                case 2: 
                    resp = self.create_agent()
                    
                    token_created = None
                case _:
                    print("\n" + "="*40)
                    print("  ⚠ You must login or create an account to proceed")
                    print("="*40 + "\n")
                    token_created = None
        while token_created == 'token':
            print("\n" + "="*80)
            print(" " * 30 + "👋 WELCOME BACK! 👋")
            print("="*80)
            print("\n  What would you like to do today?\n")
            print("    [b] See all bookings")
            print("    [p] Manage properties")
            print("    [c] Manage clients")
            print("    [q] Quit")
            print()
            status = input("  Enter your choice: ").lower().strip()
            match status:
                case 'q':
                    print("\n" + "="*80)
                    print(" " * 30 + "👋 Thank You! 👋")
                    print("="*80)
                    print("\n  Thank you for using our system. Goodbye!\n")
                    break
                case 'p':
                    properties.Properties(db=self.db,db_gen=self.db_gen, agency_id = agency_id, agent_id = agent_id).cli(role)
                case 'b':
                    self.manage_bookings(agent_id=agent_id)
                case 'c':
                    self.manage_clients(agent_id)
                case _:
                    print("\n  Exiting...\n")
                    break
            
if __name__ == "__main__":
    db_gen = get_db()
    db = next(db_gen)
    const = Agent(db_gen, db)
    const.cli()
    