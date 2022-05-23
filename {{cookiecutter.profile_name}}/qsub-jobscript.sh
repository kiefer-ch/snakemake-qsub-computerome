#!/usr/bin/env bash
# properties = {properties}

# print cluster job id
echo "Running cluster job $JOB_ID"
echo "-----------------------------"

# run the job command
( {exec_job} )
EXIT_STATUS=$?  # get the exit status

# print resource consumption
echo "-----------------------------"
qstat -f -1 $JOB_ID | grep '^    resources_used.'

# print exit status
echo "-----------------------------"
echo "EXIT_STATUS: $EXIT_STATUS"

# exit with captured exit status
exit $EXIT_STATUS
