echo 'sentinel monitor mymaster 127.0.0.1 6379 1' >> /data/sentinel.conf
echo 'sentinel down-after-milliseconds mymaster 500' >> /data/sentinel.conf
echo 'sentinel failover-timeout mymaster 500' >> /data/sentinel.conf
echo 'sentinel parallel-syncs mymaster 1' >> /data/sentinel.conf
echo 'repl-diskless-sync yes' >> /data/sentinel.conf
echo 'repl-timeout 60' >> /data/sentinel.conf