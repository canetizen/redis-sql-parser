from rediscluster import RedisCluster
import redis
import sys

class RedisClusterExecutor:
    def __init__(self):
        try:
            startup_nodes = [ # Cluster nodes
                {"host": "localhost", "port": "7000"},
                {"host": "localhost", "port": "7001"},
                {"host": "localhost", "port": "7002"}
            ]
            self.cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)
            print("Connection successful.")
        except redis.exceptions.RedisClusterException as e:
            print(f"Error: {e}")
            sys.exit(1)

    def execute_command(self, command):
        try:
            parts = command.split()
            redis_command = parts[0].upper()
            
            if redis_command == 'HSET':
                key = parts[1]
                field_values = parts[2:]
                
                result = self.cluster.hset(key, mapping=dict(zip(field_values[::2], field_values[1::2])))
            else:  # Can be expanded for other commands
                args = parts[1:]
                result = self.cluster.execute_command(redis_command, *args)
            
            print(f"Command running: {command}")
            print(f"Result: {result}")
        except redis.exceptions.RedisClusterException as e:
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
            print(f"File found error: {file_path}")
            sys.exit(1)

if __name__ == "__main__":
    executor = RedisClusterExecutor()
    executor.execute_sql_file("./matcher/example_parsed.sql")