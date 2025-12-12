from tabulate import tabulate
from app.db.connect import get_db
from sqlalchemy import text

class query_:
    def __init__(self, db):
        """Initialize the query helper with a database connection.
        
        Args:
            db: Database connection object from SQLAlchemy.
        """
        self.db = db
    def select_all(self,query: str = None, param: str = None, limit: str = None):
        """Execute SELECT queries and return results as mappings.
        
        This helper method prevents repetitive coding and accepts SQL queries as strings.
        Results are returned as a list of RowMapping objects that can be easily converted
        to dictionaries or DataFrames.
        
        Args:
            query (str): SQL SELECT query string. Can use named parameters (e.g., :param_name).
            param (dict, optional): Dictionary of parameters for parameterized queries.
                                   Defaults to None for queries without parameters.
        
        Returns:
            list: List of RowMapping objects containing the query results.
        
        Raises:
            ValueError: If query is None or empty.
        """
        try:
            
            _Validators._ensure_query(query)
            # print(param)
            _limit = f" limit {int(limit)}" if limit is not None and limit.isdigit() else "" 
            stmt = text(query+_limit)
            # print(stmt)
            
            
            if not param:
                result = self.db.execute(stmt)
            elif param:
                result = self.db.execute(stmt, param)
                
            rows = result.mappings().all()
            # print(row
            return rows
        except Exception as e:
            print(f"Rollback occured: {e}")
            raise e
    def _insert(self, query, params: dict):
        """Insert records into the database using a parameterized query.
        
        Executes an INSERT query with the provided parameters and commits the transaction.
        
        Args:
            query (str): SQL INSERT query string with named parameters (e.g., :param_name).
            params (dict): Dictionary of parameters to bind to the query.
        
        Returns:
            Result: SQLAlchemy Result object from the executed query.
        
        Raises:
            ValueError: If query or params are None or empty.
        """
        try:
            _Validators._ensure_params(params)
            _Validators._ensure_query(query)
            sql_query = text(query)
            result = self.db.execute(sql_query, params)
        except Exception as e:
            print(f"Rollback occured: {e}")
            self.db.rollback()
            raise
        finally:           
            self.db.commit()
            return result
    def _delete_by(self, query: str=None, 
                   param: any=None):
        """Delete records from the database matching the provided parameters.
        
        Executes a DELETE query with the provided parameters and commits the transaction.
        Prints a success message upon completion.
        
        Args:
            query (str): SQL DELETE query string with named parameters (e.g., :param_name).
            param (dict, optional): Dictionary of parameters to bind to the query.
                                   Defaults to None.
        
        Returns:
            None
        
        Raises:
            ValueError: If query or param are None or empty.
            Exception: Re-raises any exception that occurs during execution.
        """
        try:
            _Validators._ensure_params(param)
            _Validators._ensure_query(query)
            sql_query = text(query)
            
            self.db.execute(sql_query, param)
            # self.db.commit()
            print('\nDelete Successfull🎊\n')
        
        except:
            self.db.rollback()
        finally:           
            self.db.commit()
            return 
            
    def _update(self, query, param):
        """Update existing records in the database.
        
        Executes an UPDATE query with the provided parameters and commits the transaction.
        Prints a success message upon completion.
        
        Args:
            query (str): SQL UPDATE query string with named parameters (e.g., :param_name).
            param (dict): Dictionary of parameters to bind to the query.
        
        Returns:
            None
        
        Raises:
            ValueError: If query or param are None or empty.
            Exception: Re-raises any exception that occurs during execution.
        """
        try:
            _Validators._ensure_params(param)
            _Validators._ensure_query(query)
            
            sql_query = text(query)
            self.db.execute(sql_query, param)
            print('\nUpdate successfull🎊\n')
    
        except Exception as e:
            print(f"There was Rollback {e}")
            self.db.rollback()
        finally:           
            self.db.commit()
            return 
    def _print_all(self, result: list[dict], key:str =None):
        """Print all rows from a query result (debugging utility).
        
        Iterates through the result set and prints each row with a newline separator.
        Useful for debugging and inspecting query results.
        
        Args:
            result: SQLAlchemy Result object or iterable containing query results.
        
        Returns:
            None
        """
        if key is None:
            return
        save_list = []
        for i in range(len(result)):
            save_list.append(result[i][key])
        print(save_list)
        return save_list
 
            
             
class _Validators:
    
    def _ensure_query(query):
        """Validate that a query string is provided and not empty.
        
        Args:
            query (str): SQL query string to validate.
        
        Raises:
            ValueError: If query is None, empty, or evaluates to False.
        """
        if not query:
            raise ValueError('Query parameter needs to be filled')
    def _ensure_params(param):
        """Validate that parameters are provided and not empty.
        
        Args:
            param (dict): Parameter dictionary to validate.
        
        Raises:
            ValueError: If param is None, empty, or evaluates to False.
        """
        if not param: 
            raise ValueError('Param is needed to filter search')
    # def _is_exist(db, query, param):
        
                 
        
class _Display:
    
    def pretty_df(df, showindex: bool = False):
        """Pretty-print a pandas DataFrame in PostgreSQL-style table format.
        
        Formats and displays a DataFrame using the tabulate library with a clean,
        readable PostgreSQL-style table format. Useful for displaying query results
        in the console.
        
        Args:
            df (pd.DataFrame): The DataFrame to display.
            showindex (bool, optional): Whether to show the DataFrame index.
                                       Defaults to False.
        
        Returns:
            None
        """
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=showindex))

        