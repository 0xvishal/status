# status

## Automating Firewall rules updates on consul catalog Data.  We are going to achieve this solution using python.
Step1: Install following package   $ pip install python-consul

Step2: Prepare the python script(consul.py)     Here we are using iptables to update firewall rules.   The above script can perform following work.  1. Connects to Consul and retrieves the service information for each specified service.
2. Extracts the IP addresses of nodes providing each service
3. Uses iptables to add a rule allowing traffic from each node to the corresponding service port.
4. Checks if the rule already exists to avoid duplicates. 5. Optionally, saves the updated iptables rules to persist after a reboot.  Note: You can schedule this script to run periodically or integrate it with your infrastructure automation tools to keep your firewall rules up-to-date based on Consul catalog data
