SHORTREL=$1

cp submit_v45wTT_151pre3.yaml submit_v45wTT_$SHORTREL.yaml
sed -i "s/151pre3/$SHORTREL/g" submit_v45wTT_$SHORTREL.yaml
