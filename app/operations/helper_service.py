
from app.db.connect import get_db
from sqlalchemy import text

class query_:
    def __init__(self, db):
        self.db = db
    def select_all(self,query: str = None, param: str = None):
        """This helper is used for select queries and execution:
                - it prevents repetitive coding
                - and accepts basic sql query as strings 
            """
        _Validators._ensure_query(query)
        stmt = text(query)
        
        if not param:
            result = self.db.execute(stmt)
        elif param:
            result = self.db.execute(stmt, param)
            
        rows = result.mappings().all()
        # self._print_all(result)
        # print('Debug: {}'.format(rows))
        return rows
    def _insert(self, query, params: dict):
        
        _Validators._ensure_params(params)
        _Validators._ensure_query(query)
        sql_query = text(query)
        result = self.db.execute(sql_query, params)
       
        self.db.commit()
        
        return result
    def _delete_by(self, query: str=None, 
                   param: any=None):
        """
            _delete_by: delete by params

        Args:
            query (str, optional): _description_. Defaults to None.
            param (any, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_
        """
        try:
            _Validators._ensure_params(param)
            _Validators._ensure_query(query)
            sql_query = text(query)
            
            self.db.execute(sql_query, param)
            self.db.commit()
            print('\nDelete Successfull🎊\n')
            return 
        
        except Exception as e:
            raise e
    def _update(self, query, param):
        try:
            _Validators._ensure_params(param)
            _Validators._ensure_query(query)
            
            sql_query = text(query)
            self.db.execute(sql_query, param)
            self.db.commit()
            print('\nUpdate successfull🎊\n')
            return
        except Exception as e:
            raise e
    def _print_all(self, result):
        for i in result:
            print(i, "\n")
             
class _Validators:
    
    def _ensure_query(query):
        if not query:
            raise ValueError('Query parameter needs to be filled')
    def _ensure_params(param):
        if not param: 
            raise ValueError('Param is needed to filter search')