#!/bin/bash

target_folder="/root/Desktop/Navigation"

purge_queue()
{
	python "$target_folder/send_purge_linux.py"
}

pointsfile="$target_folder/RecordGPSPoints.txt"
mapfile="$target_folder/new.map"
finishedfile="$target_folder/finished.txt"
lastgoalfile="$target_folder/lastGoalRecorded.txt"
lasthaltfile="$target_folder/lastHaltAfterGoal.txt"

while true;
do	
	while [ ! -f "$finishedfile" ]; 
	do
		./LinuxClient
		if [ -f "$pointsfile" ]
		then
			./test_mapCreation
		fi
	done
	./LinuxClient2
	while [ -f "$mapfile" ];
	do
		./LinuxClient2
	done
done 
	
