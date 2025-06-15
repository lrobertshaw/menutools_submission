# for sample in $(dasgoclient -query="dataset=/HTo2LongLivedTo2mu2jet*/*Spring24*/GEN-SIM-DIGI-RAW-MINIAOD"); do
#     echo $sample
# done

for sample in $(dasgoclient -query="dataset=/HTo2LongLived*/*Spring24*/GEN-SIM-DIGI-RAW-MINIAOD"); do
    temp=${sample#*/}
    sampleShort=${temp%%_TuneCP5*}
    echo "${sampleShort}_200PU:"
    echo "  input_dataset: $sample"
    echo "  crab: True"
    echo "  splitting_mode: Automatic"
    echo "  splitting_granularity: 200"
    echo "  max_events: -1"
    echo 
done

for sample in $(dasgoclient -query="dataset=/HTo2LongLived*/*Spring24*/GEN-SIM-DIGI-RAW-MINIAOD"); do
    temp=${sample#*/}
    sampleShort=${temp%%_TuneCP5*}
    echo "- ${sampleShort}_200PU"
done

# DY_M50_Spring24_200PU:
#   input_dataset: /DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD
#   crab: True
#   splitting_mode: Automatic
#   splitting_granularity: 200
#   max_events: -1


# temp=${sample#*v45/}  # Remove everything up to and including "v45/"                                                                                       sampleShort=${temp%%_TuneCP5*}  # Remove "_TuneCP5" and everything after
