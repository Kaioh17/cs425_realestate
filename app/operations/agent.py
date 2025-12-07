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
from . import helper_service


class Agent:
    db_gen = get_db()
    db = next(db_gen)
    # select = helper_service.query_(db).
    query = helper_service.query_(db)
    def create_agent():
        print("Agents Sign up page....")
        print("you may begin....")
        role = 'agent'
        first_name = input("first_name: ")
        last_name = input("last_name: ")
        email = input("email: ")
        job_title = input("job_title: ")
        agency = input("agency: ")
        contact_info = input("contact_info: ")
        
        to_dict={'user': {'role': role or 'agent',
                'first_name': first_name.capitalize() or 'James',
                'last_name': last_name.capitalize() or 'Lucky',
                'email': email or 'lucky@gmail.com'},
                'agent': {'id': 0,
                                'job_title': job_title or 'agent',
                            'agency': agency or 'B&B',
                            'contact_info': contact_info or 'lucky@gmail.com'}}

        # print(to_dict)
        # user_model = UserCreate(to_dict)
        # Agent.create_agent(to_dict)
        

        # print("User: {} agent {}".format(to_dict['user'], to_dict['agent']))
        sql = 'insert into users (role, first_name, last_name, email) values (:role, :first_name, :last_name, :email) returning id'
        
        result = Agent.query._insert(query=sql, params=to_dict['user'])
        user_id = result.scalar()
        # print(f"result: {user_id}")
        to_dict['agent']['id'] = user_id
        sql_agent = f'insert into agents_profile (id, job_title, agency, contact_info) values (:id, :job_title, :agency, :contact_info)'
        # print(f"result: {sql_agent}")
        
        Agent.query._insert(query=sql_agent, params=to_dict['agent'])
        
        print('\n--------CONGRATULATIONS YOU ARE NOW AN AGENT🎉🎉🎉------------\n')
    
    def signin():
        print("You may begin login...")
        email =input("email: ")
        # password = input("password: ")
        
        sql = text('select * from users where email = :email') 
        result = Agent.db.execute(sql,{'email':email or 'test@dreamhomes.com'})
        
        result = result.fetchone()
    def get_agent():
        print('Agent detaisls for')
    def cli():
        print("Hello there 🌟 Sign-in or create account: \n"
        "• Sign in (1)\n"
        "• Create an agent account (2)\n"
        "type category below ⤵\n")
        decision = int(input(""))
        match decision:
            case 1:
                print('feature coming up soon...')
                Agent.signin()
                token_created = 'token'
            case 2: 
                Agent.create_agent()
                token_created = 'token'
            case _:
                print('you have to login or create an account to proceed')
        while token_created == 'token':
            print('welcome back!!!')
            print('See all bookings[]')
            print('create listings')
            print('see clients') 
            status = input('enter (q) to quit: ')
            if status != 'q':
                print('es')
            else:
                print('exiting....')
                break
            
if __name__ == "__main__":
    Agent.cli()
    