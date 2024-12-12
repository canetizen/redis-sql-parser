import re
import os
import sys

"""Reads the SQL file and returns its content."""
def read_sql_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

"""Extracts CREATE TABLE commands and returns a dictionary of table names and their columns."""
def extract_create_table_commands(sql_content):
    create_table_pattern = r'CREATE TABLE\s+(\w+)\s*\(\s*([^;]*?)\);'
    matches = re.findall(create_table_pattern, sql_content, re.DOTALL)
    
    return {
        table_name: [
            col.strip().split()[0] for col in columns_definition.strip().split(',')
            if col and 'FOREIGN' not in col and col.strip().split()[0].isidentifier() # To ignore data types like VARCHAR(100), isidentifier() is used.
        ]
        for table_name, columns_definition in matches
    }

"""Extracts INSERT INTO commands and returns a list of tuples (table_name, values)."""
def extract_insert_into_commands(sql_content):
    insert_into_pattern = r'INSERT INTO\s+(\w+)\s+VALUES\s*((?:\(\s*[^)]+\s*\)(?:,\s*)?)+);'
    return re.findall(insert_into_pattern, sql_content, re.DOTALL)

"""Formats a new HSET command with table name, fields, and values."""
def format_insert_command(insert_table_name, fields, values):
    result = []
    
    for match in re.findall(r'\(\s*[^)]+\s*\)', values):
        values_list = match.strip()[1:-1].split(',') # To ignore opening and closing parentheses
        
        grouped_values = " ".join([
            f"{fields[i]} {values_list[i].strip()}"
            for i in range(len(fields))
        ])
        
        table_with_id = f"{insert_table_name}:{values_list[0].strip()}" # values_list[0] refers to the id
        result.append(f"HSET {table_with_id} {grouped_values}".replace("'", ""))
    
    return result

def process_sql_files_in_directory(directory_path):
    sql_content = read_sql_file(directory_path + "/example.sql")

    table_fields = extract_create_table_commands(sql_content)
    insert_commands = extract_insert_into_commands(sql_content)

    output_file_name = f"{os.path.splitext("example")[0]}_parsed.sql"
    output_file_path = os.path.join(directory_path, output_file_name)

    with open(output_file_path, 'w') as output_file:
        for insert_table_name, values in insert_commands:
            fields = table_fields.get(insert_table_name, [])
            new_commands = format_insert_command(insert_table_name, fields, values)
            for command in new_commands:
                output_file.write(command + '\n')


if __name__ == "__main__":
    process_sql_files_in_directory("./matcher")
