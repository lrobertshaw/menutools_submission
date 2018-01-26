#!/bin/bash

CLUSTERID=$1
PROCID=$2

source params.sh


BATCH_DIR=${PWD}


echo "CLUSTER:" ${CLUSTERID}
echo "PROC-ID" ${PROCID}
echo 'TASKCONFDIR' ${ABSTASKCONFDIR}
echo 'OUT-DIR' ${OUTDIR}
echo 'OUTPUT-FILE' ${OUTFILE}

cd ${ABSTASKCONFDIR}
eval `scram runtime -sh`
edmConfigDump job_config_${PROCID}.py > ${BATCH_DIR}/job_config.py
cd ${BATCH_DIR}
ls
cmsRun job_config.py
ls -la

extension="${OUTFILE##*.}"
filename="${OUTFILE%.*}"
OUTTARGET="${OUTDIR}/${filename}_${PROCID}.${extension}"
cp ${OUTFILE} ${OUTTARGET}
