SHORTREL=$1

cp submit_v45wTT_150pre3.yaml submit_v45wTT_$SHORTREL.yaml
sed -i "s/150pre3/$SHORTREL/g" submit_v45wTT_$SHORTREL.yaml
