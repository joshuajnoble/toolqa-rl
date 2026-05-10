import sqlite3

def execute(db_path, sql_cmd):
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
    db_path = "/Users/joshua.noble/projects/ToolQA/data/external_sql_lite/yelp.sqlite"
    sql_cmd = "SELECT latitude, longitude FROM yelp_data WHERE address='6830 Rising Sun Ave'"
    rows = execute(db_path, sql_cmd)
    print(rows)
