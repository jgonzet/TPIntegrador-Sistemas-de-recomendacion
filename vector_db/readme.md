``` bash
docker pull opensearchproject/opensearch

docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -d -v C:\Users\jose_\Documents\ITBADL\TPS\TP2Rep\vector_db\db_data:/usr/share/opensearch/data opensearchproject/opensearch:latest

docker exec -it opensearch-node /bin/bash

docker kill 
```
