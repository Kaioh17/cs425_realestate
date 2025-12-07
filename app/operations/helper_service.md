# Helper Service Documentation

## Overview

The `helper_service.py` module provides utility classes and methods to simplify database operations and data display across the application. It reduces code repetition and standardizes common database interactions.

## Available Classes

### `query_`
Database query helper class for executing SQL operations. Initialize with a database connection.

**Methods:**
- `select_all(query, param)` - Execute SELECT queries and return results as mappings
- `_insert(query, params)` - Insert records into the database
- `_delete_by(query, param)` - Delete records by parameters
- `_update(query, param)` - Update existing records
- `_print_all(result)` - Print query results (debugging utility)

### `_Validators`
Static validation utilities for ensuring required parameters are provided.

**Methods:**
- `_ensure_query(query)` - Validates that a query string is provided
- `_ensure_params(param)` - Validates that parameters are provided

### `_Display`
Display formatting utilities for presenting data in a user-friendly format.

**Methods:**
- `pretty_df(df, showindex)` - Pretty-print pandas DataFrames using tabulate with PostgreSQL-style formatting

## Usage Example

```python
from app.operations.helper_service import query_, _Display
from app.db.connect import get_db

db = next(get_db())
query_helper = query_(db)

# Execute a select query
results = query_helper.select_all("SELECT * FROM properties WHERE location = :location", {"location": "NYC"})

# Display results
df = pd.DataFrame(results)
_Display.pretty_df(df)
```

## Extending the Module

Feel free to add new helper methods or classes as needed. The module is designed to be extended with additional utilities that follow the existing patterns. When adding new methods, ensure they follow the same validation and error handling conventions.

