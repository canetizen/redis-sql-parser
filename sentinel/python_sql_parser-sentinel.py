from redis.sentinel import Sentinel
import redis
import sys

class RedisSentinelExecutor:
    def __init__(self):
        try:
            sentinel_nodes = [
                ('127.0.0.1', 26379),
                ('127.0.0.1', 26380),
                ('127.0.0.1', 26381)
            ]
            sentinel = Sentinel(sentinel_nodes, socket_timeout=0.1)
            
            master_name = 'mymaster'
            
            # Get a connection to the master
            self.master = sentinel.master_for(master_name, socket_timeout=0.1, decode_responses=True)
            
            # Get a connection to a slave
            self.slave = sentinel.slave_for(master_name, socket_timeout=0.1, decode_responses=True)
            
            print("Connection successful.")
        except redis.exceptions.RedisError as e:
            print(f"Error: {e}")
            sys.exit(1)

    def execute_command(self, command):
        try:
            parts = command.split()
            redis_command = parts[0].upper()
            
            if redis_command == 'HSET':
                key = parts[1]
                field_values = parts[2:]
                
                result = self.master.hset(key, mapping=dict(zip(field_values[::2], field_values[1::2])))
            else:  # Can be expanded for other commands
                args = parts[1:]
                result = self.master.execute_command(redis_command, *args)
            
            print(f"Command running: {command}")
            print(f"Result: {result}")
        except redis.exceptions.RedisError as e:
            print(f"Command execution error: {command}")
            print(f"Error: {e}")

    def execute_sql_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    command = line.strip()
                    if command and not command.startswith('--'):  # Discard comments
                        self.execute_command(command)
        except FileNotFoundError:
            print(f"File not found error: {file_path}")
            sys.exit(1)

if __name__ == "__main__":
    executor = RedisSentinelExecutor()
    executor.execute_sql_file("./matcher/example_parsed.sql")
