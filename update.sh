#!/bin/bash
MESSAGE=${1:-"Meeting Update"}

# heroku git:remote  --app sheltered-sierra-31492
git add .
git commit -m "${MESSAGE}"
git push heroku master 
