#!/bin/bash

[ -f .env ] && source .env

function bloxseer_dockercompose_refresh() {
  docker-compose up -d --force-recreate  --remove-orphans
}
