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
        print("\n" + "="*80)
        print(" " * 25 + "👤 AGENT SIGN UP 👤")
        print("="*80)
        print("\n  Welcome! Let's create your agent account.\n")
        role = 'agent'
        first_name = input("  📝 First name: ")
        last_name = input("  📝 Last name: ")
        email:EmailStr = input("  📧 Email: ")
        job_title = input("  💼 Job title: ")
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
    def signin(self):
        print("\n" + "="*80)
        print(" " * 30 + "🔐 AGENT SIGN IN 🔐")
        print("="*80 + "\n")
        email = input("  📧 Email: ") or 'admintest@gmail.com'
        # password = input("password: ")
        
        select_sql = 'select *, agency_id from users join agents_profile a on a.id = users.id where email = :email'
        
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
            print("    [c] See clients")
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
                case _:
                    print("\n  Exiting...\n")
                    break
            
if __name__ == "__main__":
    db_gen = get_db()
    db = next(db_gen)
    const = Agent(db_gen, db)
    const.cli()
    