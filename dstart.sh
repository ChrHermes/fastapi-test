#!/bin/bash

dd if=/dev/zero of=./data/gcn.db bs=1K count=21543
docker build --rm -t gcn-mgmt .
docker-compose up -d && docker-compose logs -f