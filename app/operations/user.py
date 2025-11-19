from app.db.connect import get_db
from sqlalchemy import text

class user:
    db_gen = get_db()
    db = next(db_gen)

    def get_user_():
        
        try:
            user.select_all("SELECT * FROM users")

            return
        except Exception as e:
            raise e
    def get_agents():
        try:
            user.select_all("select * from users where role = 'agent'")
    
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
        result = user.db.execute(stmt).fetchall()
        user._print_all(result)
        
    def _print_all(result):
        for i in result:
            print(i, "\n")
    
        
user.get_user_()
user.get_agents()