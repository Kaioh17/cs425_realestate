from app.db.connect import get_db
from sqlalchemy import text
from . import renters, agent, helper_service

# NOTE: For useful database utilities and table printing helpers, refer to:
# - helper_service.py for query_ class methods (select_all, _insert, _update, _delete_by)
# - helper_service.md for documentation
# - helper_service._Display.pretty_df() for formatting DataFrames as tables

class User:
    db_gen = get_db()
    db = next(db_gen)

    def get_user_():
        
        try:
            helper_service.query_(db).select_all("SELECT * FROM users")

            return
        except Exception as e:
            raise e
    def get_agents():
        try:
            helper_service.query_(db).select_all("select * from users where role = 'agent'")
    
            return
        except Exception as e:
            raise e

if __name__ == '__main__':
    db_gen = get_db()
    db = next(db_gen)
    print('\n' + '='*60)
    print(' '*15 + '🏠 REAL ESTATE SYSTEM 🏠')
    print('='*60)
    print('\n' + ' '*18 + 'Welcome! Please select your role:')
    print('\n' + ' '*20 + '👤 Agent     → Press (A)')
    print(' '*20 + '🔑 Renter    → Press (R)')
    print('\n' + '='*60)
    answ = input('\n' + ' '*20 + 'Your choice: ').capitalize()    
    match answ:
        case 'R':
            renters.Renter.cli()
        case 'A':
            agent.Agent(db=db, db_gen=db_gen).cli()