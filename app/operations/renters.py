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

class Renter:
    db_gen = get_db()
    db = next(db_gen)
    # select = helper_ser
    query = helper_service.query_(db)
    
    def create_renters():
        print("Users Sign up page....")
        print("you may begin....")
        role = 'renter'
        first_name = input("first_name: ")
        last_name = input("last_name: ")
        email = input("email: ")
        move_in_date = input("When do you plan on moving in?(2025-09-01 00:00:00): ")
        preferred_location = input("preferred location: ")
        budget = input("budget: ")
        
        to_dict = {'user': {'role': role or 'renter',
                    'first_name': first_name.capitalize() or 'Buddy',
                'last_name': last_name.capitalize() or 'Baston',
                'email': email or 'baston@gmail.com'},
                'renter': {'id': 0,
                            'move_in_date': move_in_date or '2025-09-01 00:00:00',
                            'preferred_location': preferred_location or 'Chicago, IL',
                            'budget': budget or '80090'}}

        

        # print("User: {} agent {}".format(to_dict['user'], to_dict['agent']))
        sql = 'insert into users (role, first_name,last_name, email) values (:role, :first_name, :last_name, :email) returning id'
        
        result = Renter.query._insert(query=sql, params=to_dict['user'])
        user_id = result.scalar()
        # print(f"result: {user_id}")
        to_dict['renter']['id'] = user_id
        sql_agent = f'insert into renters_profile (id, move_in_date, preferred_location, budget) values (:id, :move_in_date, :preferred_location, :budget)'
        # print(f"result: {sql_agent}")
        
        Renter.query._insert(query=sql_agent, params=to_dict['renter'])
        
        print('\n--------CONGRATULATIONS ON JOINING OUR PLATFORM🎉🎉🎉------------\n')
    def signin():
        print("You may begin login...")
        email =input("email: ")
        # password = input("password: ")
        
        sql = text('select * from users where email = :email') 
        result = Renter.db.execute(sql,{'email':email})
        
        result = result.fetchone()
    def get_agent():
        print('renter  detaisls for')
    def cli():
        switch = input('You may begin: ')
        # while switch == 'start':
        print("Hello there 🌟 Sign-in or create account: \n"
        "• Sign in (1)\n"
        "• Create an agent account (2)\n"
        "type category below ⤵\n")
        decision = int(input(""))
        match decision:
            case 1:
                print('feature coming up soon...')
                Renter.signin()
                token_created = 'token'
            case 2: 
                Renter.create_renters()
                token_created = 'token'
            case _:
                print('you have to login or create an account to proceed')
        while token_created == 'token':
            print('\nwelcome back!!!\n')
			##perform all operations in here 
            status = input('enter (q) to quit: ')
            if status == 'q':
                print('')
            else:
                print('exiting....')
                break
if __name__ == '__main__':
    Renter.cli()