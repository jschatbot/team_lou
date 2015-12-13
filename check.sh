#!/bin/sh
cd `dirname $0`
count=`ps -ef | grep chatbot.py | grep -v grep | wc -l`
if [ $count = 0 ]; then
	echo "Run!";
	sudo nohup ./team_lou/run.sh &
else
	echo "Already up!";
fi

