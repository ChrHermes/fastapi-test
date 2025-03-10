#!/bin/bash

echo "--- Image erstellen ---"
docker buildx build --platform linux/arm/v7 -t gcn-mgmt-armv7:latest --load .
echo "--- Image exportieren ---"
docker save gcn-mgmt-armv7:latest -o ./prod/gcn-mgmt-armv7.tar

echo "--- Archiv erstellen ---"
tar czvf gcn-mgmt.tar.gz -C ./prod .

echo "--- Archiv an Controller senden ---"
sshpass -p gridcal scp gcn-mgmt.tar.gz root@192.168.1.2:/media/sd/