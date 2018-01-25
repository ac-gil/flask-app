#!/bin/bash
echo "----------------------------"
echo 
echo "QUERYING CAR BY ID=1"
echo 
echo "-----------------------------"
curl -i http://app:5000/car/1
echo "-----------------------------"
echo 
echo "QUERYING ALL THE CARS"
echo 
echo "-----------------------------"
curl -i http://app:5000/car
echo "-----------------------------"
echo 
echo "ADDIND CAR TO DATABASE"
echo 
echo "-----------------------------"
curl -i -d '{"make":"Seat", "model":"Cordoba", "year":"2003", "chassis_id":"12345F"}' -H "Content-Type: application/json" -X POST http://app:5000/car
echo
echo "-----------------------------"
echo 
echo "SEE THE RESULT OF ADDITION"
echo 
echo "-----------------------------"
curl -i http://app:5000/car
echo "-----------------------------"
echo 
echo "AVR PRICE OF SEAT CORDOBA Y. 2003"
echo 
echo "-----------------------------"
curl -i -d '{"make":"Seat", "model":"Cordoba", "year":"2003"}' -H "Content-Type: application/json" -X POST http://app:5000/avgprice
echo
echo "-----------------------------"
echo 
echo "AVR PRICE OF NISSAN MICRA Y. 2004"
echo 
echo "-----------------------------"
curl -i -d '{"make":"Nissan", "model":"Micra", "year":"2004"}' -H "Content-Type: application/json" -X POST http://app:5000/avgprice
echo
echo "-----------------------------"
echo 
