#!/bin/bash

YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SERVICES=(resources crawler-service analysis-service)

function deploy () {
  for SERVICE in "${SERVICES[@]}"
  do
    printf "${YELLOW}----------[ deploying $SERVICE ]----------${NC}\n"
    cd $SERVICE
    if [ -f package.json ]; then
      npm install
    fi
    serverless deploy
    cd ..
  done
}

deploy
