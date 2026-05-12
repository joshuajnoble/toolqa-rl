import sqlite3
from langchain.tools import tool

@tool("execute_sql_query", return_direct=True)
def execute(db_path: str, sql_cmd: str) -> str:
    """
    Executes a SQL command on the specified SQLite database and returns the results as a formatted string.
    Args:
        db_path (str): Path to the SQLite database file.
        sql_cmd (str): SQL command to execute.
    Returns:
        str: Query results formatted as a string.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_cmd)
    column_names = [i[0] for i in cursor.description]
    rows = cursor.fetchall()
    rows_string = []
    for row in rows:
        current_row = [column_names[i]+": "+str(row[i]) for i in range(len(row))]
        current_row = ', '.join(current_row)
        rows_string.append(current_row)
    rows_string = '\n'.join(rows_string)
    conn.close()
    return rows_string

if __name__ == "__main__":
    db_path = "./external_sql_lite/yelp.sqlite"
    sql_cmd = "SELECT latitude, longitude FROM yelp_data WHERE address='6830 Rising Sun Ave'"
    rows = execute(db_path, sql_cmd)
    print(rows)
