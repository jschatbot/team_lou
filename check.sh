#!/bin/sh
cd `dirname $0`
count=`ps -ef | grep chatbot.py | grep -v grep | wc -l`
str=`ps -ef | grep chatbot.py | grep -v grep`
if [ $count = 0 ]; then
	echo "Run!";
	sudo nohup ./team_lou/run.sh > out.log 2> error.log &
else
	echo "Already up!";
	echo $str
fi

