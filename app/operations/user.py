from app.db.connect import get_db
from sqlalchemy import text
from . import renters, agent

# NOTE: For useful database utilities and table printing helpers, refer to:
# - helper_service.py for query_ class methods (select_all, _insert, _update, _delete_by)
# - helper_service.md for documentation
# - helper_service._Display.pretty_df() for formatting DataFrames as tables

class User:
    db_gen = get_db()
    db = next(db_gen)

    def get_user_():
        
        try:
            User.select_all("SELECT * FROM users")

            return
        except Exception as e:
            raise e
    def get_agents():
        try:
            User.select_all("select * from users where role = 'agent'")
    
            return
        except Exception as e:
            raise e
    
    ##helpers
    ## TODO move helper to seperate directory
    def select_all(query: str = None):
        """This helper is used for select queries and execution:
                - it prevents repetitive coding
                - and accepts basic sql query as strings 
            """
        stmt = text(query)
        result = User.db.execute(stmt).fetchall()
        User._print_all(result)
        
    def _print_all(result):
        for i in result:
            print(i, "\n")

if __name__ == '__main__':
    print('Who are you: \n - agent(A) \n - renter(R)')
    answ = input('').capitalize()    
    match answ:
        case 'R':
            renters.Renter.cli()
        case 'A':
            agent.Agent.cli()