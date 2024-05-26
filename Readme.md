
About: 
To implement a log watching solution , this flask app tracks the log in real time and updates the UI in case of any updation.
The log file is hosted on a remote machine (same machine as your server code). The log file is in append-only mode.
It prints the updates in the file as and when they happen and NOT upon page refresh. A background job which runs after every 2 sec (can be further reduced), to push the latest changes on client. 


A Flask app  running on gunicorn wsgi to provide the endpoints to serve to the UI for client. 
Employed Server-sent Event (SSE), to enable a unidirectional “push” of updation events.


how to run 
 => Activate the virtual env cmd : source bin/activate
 => install requerements from requirement.txt 
 => start the redis server(SSE library dependency), cmd => redis-server
 => cmd to run the server ==> gunicorn main:app --worker-class gevent --bind 127.0.0.1:5000 
 => source of logs => log_file.txt
 => check localhost:5000 => to get the msg 'app is working'
endpoints: 
    /monitor => to see the log changes
    /log => after refresh updated lines should be visible
    
