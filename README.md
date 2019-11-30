# Scylla
 Scylla is an intelligent WAF whose rules are automatically updated based on threats received, detected by machine learning, in addition to other new forms of analysis.

# How to install?
 Run `pip3 install -r requirements.txt`, then set scylla.conf file ( in config/scylla.conf ) with your server ip and port, if you want to make a stronger configuration then check the other parameteres and also config/variables.conf and scylla_dependencies/WAF/waf.conf, then run `python3 scylla.py`, a proxy server will be executed in the setted port.
 
 # web interface
  Django web interface is in (default) 8080 port. You can change it in scylla.conf.
  Default creds are scylla/pestillo. WE STRONGLY RECOMMEND TO CREATE A NEW ACCOUNT ( /admin )
  
 # scylla machine learning
 The main goal of scylla is to implement a functional ML, as an extra feature
