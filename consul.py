import subprocess
import consul

# Initialize a Consul client
consul_client = consul.Consul()

# Define the service names and their corresponding ports
services = {
    "Logstash": 5141,
    "NodeExporter": 9100,
    "MySQLExporter": 9104,
    "MySQL": 3306
}

# Iterate over the services and their respective ports
for service_name, service_port in services.items():
    # Query Consul for nodes providing the service
    _, nodes = consul_client.catalog.service(service_name)
    
    # Extract node IP addresses
    node_ips = [node['ServiceAddress'] for node in nodes]
    
    # Update firewall rules for each node IP
    for node_ip in node_ips:
        # Define the iptables rule to allow traffic from the node IP to the service port
        iptables_rule = f"iptables -A INPUT -p tcp -s {node_ip} --dport {service_port} -j ACCEPT"
        
        # Check if the rule already exists to avoid duplicates
        rule_exists = subprocess.run(["iptables", "-C", "-L", "INPUT", "-p", "tcp", "-s", node_ip, "--dport", str(service_port), "-j", "ACCEPT"], stdout=subprocess.PIPE).returncode == 0
        
        if not rule_exists:
            # Add the rule to the firewall
            subprocess.run(iptables_rule, shell=True)
            print(f"Added rule for {service_name} on {node_ip}:{service_port}")

# Save the updated iptables rules to persist after reboot (optional)
subprocess.run(["iptables-save"], stdout=subprocess.PIPE)
