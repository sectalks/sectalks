echo "Sleeping for 2 seconds for redis to boot up..."
sleep 2
echo "Initializing redis..."
jython /init.py
echo "Starting tomcat..."
catalina.sh run
