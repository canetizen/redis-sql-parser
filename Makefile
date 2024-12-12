# Redis Cluster commands
cluster-up:
	python3 ./matcher/matcher.py
	docker-compose -f ./cluster/docker-compose-cluster.yml up -d

cluster-down:
	docker-compose -f ./cluster/docker-compose-cluster.yml down --volumes

create-cluster:
	@echo "Creating Redis cluster..."
	@docker exec -it can_redis_node1 redis-cli --cluster create can_redis_node1:6379 can_redis_node2:6380 can_redis_node3:6381 --cluster-replicas 0

cluster-clean:
	@make cluster-down
	@docker system prune -f --filter label=com.docker.compose.project=redis-cluster
	@rm -f ./matcher/example_parsed.sql

add-data-cluster:
	@/bin/python3 ./cluster/python_sql_parser-cluster.py
# Redis Sentinel commands

sentinel-up:
	python3 ./matcher/matcher.py
	docker-compose -f ./sentinel/docker-compose-sentinel.yml up -d

sentinel-down:
	docker-compose -f ./sentinel/docker-compose-sentinel.yml down --volumes

sentinel-clean:
	@make sentinel-down
	@docker system prune -f --filter label=com.docker.compose.project=redis-sentinel
	@rm -f ./matcher/example_parsed.sql

add-data-sentinel:
	@/bin/python3 ./sentinel/python_sql_parser-sentinel.py

# Common commands
build-module:
	@/bin/python3 ./matcher/matcher.py

clean: cluster-clean sentinel-clean

# Combined commands
cluster-all: build-module cluster-up create-cluster add-data-cluster

sentinel-all: build-module sentinel-up add-data-sentinel

.PHONY: cluster-up cluster-down create-cluster cluster-clean sentinel-up sentinel-down sentinel-clean build-module add-data-sentinel clean cluster-all sentinel-all add-data-cluster