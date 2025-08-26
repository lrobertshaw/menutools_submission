SHORTREL=$1
BASEREL=${2:-"151pre3"}

cp submit_v45wTT_$BASEREL.yaml submit_v45wTT_$SHORTREL.yaml
sed -i "s/$BASEREL/$SHORTREL/g" submit_v45wTT_$SHORTREL.yaml
