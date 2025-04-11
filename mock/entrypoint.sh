#!/bin/bash

# Frequenzbereich in Sekunden (z. B. 1 bis 10)
LOG_INTERVAL_RANGE="1 10"

LOG_LEVELS=("INFO" "WARNING" "ERROR")
MESSAGES=(
  "Service started"
  "Health check passed"
  "Received command"
  "Processed request"
  "Unexpected input"
  "Retrying connection"
  "Connection successful"
  "Low disk space warning"
  "Operation timed out"
  "Heartbeat"
)

echo "Starting logger for container: $HOSTNAME"
echo "Log interval range: ${LOG_INTERVAL_RANGE}s"

while true; do
  LEVEL=${LOG_LEVELS[$((RANDOM % ${#LOG_LEVELS[@]}))]}
  MSG=${MESSAGES[$((RANDOM % ${#MESSAGES[@]}))]}
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

  echo "[$TIMESTAMP] [$LEVEL] [$HOSTNAME] $MSG"

  MIN=$(echo "$LOG_INTERVAL_RANGE" | cut -d' ' -f1)
  MAX=$(echo "$LOG_INTERVAL_RANGE" | cut -d' ' -f2)
  SLEEP_TIME=$((RANDOM % (MAX - MIN + 1) + MIN))
  sleep "$SLEEP_TIME"
done
