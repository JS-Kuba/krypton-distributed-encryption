import os

# List of hostnames or IP addresses
hosts = ["172.168.10.1", "172.168.10.2", "172.168.10.3"]

# List of usernames corresponding to the hosts
usernames = ["ubuntu", "ubuntu", "ubuntu"]

# Path to the app.py file
app_file = "app.py"

# Remote destination directory on the hosts
remote_dir = "/path/to/remote/directory/"

# Loop through each host and copy the app.py file
for host, username in zip(hosts, usernames):
    print(f"Copying app.py to {username}@{host}...")
    os.system(f"scp {app_file} {username}@{host}:{remote_dir}")

# Loop through each host and run the app.py file
for host, username in zip(hosts, usernames):
    print(f"Running app.py on {username}@{host}...")
    os.system(f"ssh {username}@{host} 'cd {remote_dir} && python app.py &'")
