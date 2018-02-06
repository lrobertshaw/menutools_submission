#!/bin/bash

CLUSTERID=$1
PROCID=$2
source params.sh

echo "CLUSTER:" ${CLUSTERID}
echo "PROC-ID" ${PROCID}
echo 'TASKCONFDIR' ${ABSTASKCONFDIR}
echo 'OUT-DIR' ${OUTDIR}
echo 'OUTPUT-FILE' ${OUTFILE}


BATCH_DIR=${PWD}
echo "Current dir: ${BATCH_DIR}"
ls -l
extension="${OUTFILE##*.}"
filename="${OUTFILE%.*}"
OUTTARGET="${OUTDIR}/${filename}_${PROCID}.${extension}"
cp ${OUTFILE} ${OUTTARGET}
