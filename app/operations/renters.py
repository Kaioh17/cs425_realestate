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
        sql_agent = 'insert into renters_profile (id, move_in_date, preferred_location, budget) values (:id, :move_in_date, :preferred_location, :budget)'
        # print(f"result: {sql_agent}")
        
        Renter.query._insert(query=sql_agent, params=to_dict['renter'])
        
        print('\n--------CONGRATULATIONS ON JOINING OUR PLATFORM🎉🎉🎉------------\n')
    def signin():
        print("You may begin login...")
        email =input("email: ")  or 'terrel@gmail.com'
        # password = input("password: ")
        
        sql = text('select * from users where email = :email') 
        result = Renter.db.execute(sql,{'email':email})
        
        result = result.fetchone()
        print(result)
        return email
    ###Address management
    def add_card(email):
        print('Add a card')
        print('\nEnter card details>>>>>>')
        card_number = input('Card number: ') or '34353435344'
        card_type = input('Card type[Visa|MasterCard]: ') or 'visa'
        card_exp_month = int(input('exp. Month: ') or 8)
        card_exp_year = int(input('exp year: ') or 2029)
        print('\nBilling Address>>>>')
        street = input('street: ') or '1234 S TestAddress'
        city = input('city: ') or 'Chicago'
        state = input('state: ') or 'IL'
        zip = input('zip: ') or '60872'
        """BEGIN TRANSACTION;
                
                INSERT INTO Table2 (ColumnX, ColumnY) VALUES ('Value3', 'Value4');

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
        get_id_sql=text("select id from users where email = :email")
        insert_ra_sql=text("INSERT INTO  renter_addresses (renter_id, street, city, state, zip) VALUES (:renter_id, :street, :city, :state, :zip) returning id")
        insert_cc_sql=text("INSERT INTO credit_cards (renter_id, card_number, card_type, billing_address_id, expiration_month, expiration_year) VALUES (:renter_id, :card_number, :card_type, :billing_address_id, :expiration_month, :expiration_year) ")
        response = Renter.db.execute(get_id_sql,{'email': email})
        response = response.mappings().all()
        # print(response[0]['id'])
        
        renter_id = response[0]['id']
        insert_response = Renter.db.execute(insert_ra_sql, {'renter_id':renter_id, 'street':street, 
                                                     'city': city, 'state': state, 'zip': zip})
        billing_address_id = insert_response.scalar()
        print(billing_address_id)
        Renter.db.execute(insert_cc_sql, {'renter_id':renter_id,'card_number':card_number,
                                            'card_type':card_type, 'billing_address_id':billing_address_id, 
                                            'expiration_month':card_exp_month,
                                            'expiration_year': card_exp_year})
        Renter.db.commit()
        
        # print(response)
        print('\nYour card {} has been added successfully\n'.format(card_number))
        return response
    def get_agent():
        print('renter  details for')
    def delete_address(email):
        sql = """select ra.id, ra.street,c.card_number, u.id as renter_id  from renter_addresses ra join users u on u.id = ra.renter_id 
                join credit_cards c on ra.id = c.billing_address_id where u.email = :email"""
        # print(dict(email))
        response = Renter.query.select_all(query=sql, param={'email':email})
        if len(response) == 0:
            print("You have no addresses left to delete->\n")
            ans = input("would you like to add a new card?[y/n]: ")
            if ans.lower() == 'y':
                Renter.add_card(email)
            return
        print('what will you be deleting today:')
        for i in range(len(response)):
            print("id[{}] street[{}] card_no[{}] ".format(response[i]['id'],response[i]['street'], response[i]['card_number']))
        # to_delete = list(tuple(input('id: [if more than one enter as "(1,2, 3)"]:'))) #
        to_delete = input('id: [if delete more than one enter as "1,2,3"]: ').split(',')
        print(to_delete)
        sql = 'delete from renter_addresses where id = :id and renter_id = :renter_id'
        
        
        for i in range(len(to_delete)):
            Renter.query._delete_by(query=sql,
                                    param={"id":int(to_delete[i]), 
                                           "renter_id": response[0]['renter_id']})
    def update_address(email):
        """
            UPDATE table_name
            SET column1 = value1, column2 = value2, ...
            WHERE condition;
        """
        'update renter_addresses set <> where '
        pass 
    def update_card(email):
        pass  
    def delete_card(email):
        ##card_number or card_id?
        print('What cards will you be deleting today?')
        sql = 'select c.id, c.card_number, c.renter_id from credit_cards c join users u on u.id = c.renter_id where u.email = :email'
        response = Renter.query.select_all(query=sql, param={'email':email})
        for i in range(len(response)):
            print("id:{} card_no:{}".format(response[i]['id'], response[i]['card_number']))
        card_id = input('Enter card id: ')
        
        if len(response) == 0:
            print("You have no addresses left to delete->\n")
            ans = input("would you like to add a new card?[y/n]: ")
            if ans.lower() == 'y':
                Renter.add_card(email)
            return
            
        renter_id = response[0]['renter_id']
        print(f'Renter id: {renter_id}')
        sql = 'delete from credit_cards where id = :id and renter_id = :renter_id'
        Renter.query._delete_by(query=sql, param = {"id":int(card_id), "renter_id": int(renter_id)})
        
    def cli():
        # while switch == 'start':
        b = True
        while b == True:
            print("\n Hello there 🌟 Sign-in or create account: \n"
            "• Sign in (1)\n"
            "• Create an agent account (2)\n"
            "type category below ⤵")
            decision = input("")
            match decision:
                case '1':
                    # print('feature coming up soon...')
                    email = Renter.signin()
                    print(email)
                    
                    token_created = 'token'
                    b=False
                case '2': 
                    Renter.create_renters()
                    token_created = 'token'
                    b=False
                case _:
                    print('You have to login or create an account to proceed🚨❗❗\n')
                    b = True
            
        print(f'\nwelcome back {email}🌟\n')
            
        while token_created == 'token':
            print('• Edit profile(e)')
            print('• Payment management[1]')
            print('• Address management [2]')
            print('• Select agent')
            print('• See rewards')
			##perform all operations in here 
            print('• enter (q) to quit: ')
            
            
            selection = input('')
            match selection:
                case 'q':
                    print('exiting:')
                    break
                case 'e':
                    print('Not built yet')
                    pass
                case '1':
                    print('\n------------Payment Management-----------\n')
                    print('- Add new card[a]')
                    print('- Update billing address[u]')
                    print('- Delete card[d]')
                    func = input('')
                    match func:
                        case 'a':
                            Renter.add_card(email)
                        case 'd':
                            Renter.delete_card(email)
                        case 'u':
                            Renter.update_card(email)
                case '2':
                    print('\n------------Address Management_-----------')
                    print('- Update billing address[u]')
                    print('- Delete old address(note: Associated card will be deleted too)[d]')
                    
                    func = input('')
                    match func:
                        case 'u':
                            Renter.update_address(email)
                        case 'd':
                            Renter.delete_address(email)                            
                        case _:
                            print('Showing list again')
                    
if __name__ == '__main__':
    Renter.cli()
    