# joblist="151X_D110 151X_D116 151X_D121 151pre3_only48136 151pre3_SC8Nano"
joblist="151pre3_L1EGupdate1"
revision=7am
RESUBMIT=$1

for job in $joblist; do
    if [[ $RESUBMIT == "TRUE" ]]; then
	echo Resubmitting $job
	source scripts/resubmitSubmission.sh V45_reL1wTT_$job |& tee logs/resubmit_${job}_${revision}.log
    else
	echo Checking $job
	source scripts/checkSubmission.sh V45_reL1wTT_$job |& tee logs/check_${job}_${revision}.log
    fi
done

if [[ $RESUBMIT == "TRUE" ]]; then
    echo Done # do nothing
else
    for job in $joblist; do
	echo Summary for $job:
	grep -r "finished" logs/check_${job}_${revision}.log
	grep -r "   failed" logs/check_${job}_${revision}.log
	grep -r "running" logs/check_${job}_${revision}.log
    done
fi

