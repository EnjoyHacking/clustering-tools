#!/bin/bash

# Get the vector representation of payload using byte embeddings
python payload_vectorization.py ../related_files/http/http_merge_64_1000_byteEmbedding.txt ../related_files/http/http_merge_64_1000.hex ../related_files/http/http_merge_64_1000_payloadEmbedding.txt

# Execute k-means clustering algorithm
#python kmeans.py ../related_files/http/http_merge_64_1000_payloadEmbedding.txt 10 ../related_files/http/http_merge_64_1000_assignment.txt
