RELEASE=$1

RELEASEDIR=/eos/user/r/roward/CMS/phase2/CMSSW_testing/$RELEASE
cd $RELEASEDIR
cmsenv
cd ~/CMS/Phase2/Submissions/submission/

echo CMSSW local release: $CMSSW_BASE
echo CMSSW source release: $CMSSW_RELEASE_BASE
