
pkill -f src/redis-server 
sleep 3s
redis-stable/src/redis-server&
sleep 3s
pkill -f zato
pkill -f gunicorn
sleep 3s
ps -ef | grep -i zato
sudo su - zato -c "cd /opt/zato/env/NewSP/ && ./zato-qs-start.sh"&


