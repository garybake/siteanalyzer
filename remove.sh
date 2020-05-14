#!/bin/bash

YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SERVICES=(resources crawler-service analysis-service)

function remove () {
  for SERVICE in "${SERVICES[@]}"
  do
    printf "${YELLOW}----------[ removing $SERVICE ]----------${NC}\n"
    cd $SERVICE
    serverless remove
    cd ..
  done
}

remove