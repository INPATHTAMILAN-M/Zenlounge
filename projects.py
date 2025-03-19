import paramiko
import json
import os

# Define server details
servers = [
    {"name": "PADANI", "host": "64.227.146.5", "user": "root", "key": "~/.ssh/padani_key"},
    {"name": "134.209.148.230", "host": "134.209.148.230", "user": "root", "key": "~/.ssh/compass-key"},
    {"name": "121.200.52.133", "host": "121.200.52.133", "user": "Administrator", "key": None},
    {"name": "143.110.245.135", "host": "143.110.245.135", "user": "root", "key": None},
    {"name": "172.16.151.15", "host": "172.16.151.15", "user": "Administrator", "key": None},
    {"name": "CHIT", "host": "43.205.162.126", "user": "ubuntu", "key": "~/.ssh/sree-thangam-jewellery.pem"},
    {"name": "64.227.130.151", "host": "64.227.130.151", "user": "root", "key": "~/.ssh/vipassana-key"},
    {"name": "159.65.156.20", "host": "159.65.156.20", "user": "root", "key": "~/.ssh/ssh_key"},
    {"name": "142.93.217.128", "host": "142.93.217.128", "user": "root", "key": "~/.ssh/ssh_key"}
]

# Command to list directories
LIST_DIR_CMD = "ls -1"

# Store results
output = {"servers": []}

def get_projects_via_ssh(server):
    """Connects via SSH and fetches project names."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key_path = os.path.expanduser(server["key"]) if server["key"] else None
        ssh.connect(server["host"], username=server["user"], key_filename=key_path, timeout=10)

        projects = {}
        for path_type, path in {"frontend": "/var/www/", "backend": "/home/"}.items():
            stdin, stdout, stderr = ssh.exec_command(f"{LIST_DIR_CMD} {path} 2>/dev/null")
            projects[path_type] = stdout.read().decode().splitlines() or []

        output["servers"].append({"name": server["name"], "host": server["host"], "projects": projects})
    
    except Exception as e:
        print(f"Failed to connect to {server['name']} ({server['host']}): {e}")
    
    finally:
        ssh.close()

# Process all servers
for server in servers:
    get_projects_via_ssh(server)

# Save to JSON file
with open("projects.json", "w") as f:
    json.dump(output, f, indent=4)

# Print JSON output
print(json.dumps(output, indent=4))
