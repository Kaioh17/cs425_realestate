
from app.db.connect import get_db
from sqlalchemy import text

class query_:
    def __init__(self, db):
        self.db = db
    def select_all(self, user ,query: str = None):
        """This helper is used for select queries and execution:
                - it prevents repetitive coding
                - and accepts basic sql query as strings 
            """
        stmt = text(query)
        result = self.db.execute(stmt).fetchall()
        user._print_all(result)
    
    def _insert(self, query, params: dict):
        sql_query = text(query)
        result = self.db.execute(sql_query, params)
       
        self.db.commit()
        
        return result
    def _print_all(self, result):
        for i in result:
            print(i, "\n")
        