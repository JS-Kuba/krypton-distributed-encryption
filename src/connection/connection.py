import os
import json
import paramiko


class ConnectionManager:
    """
    Class for establishing connection with other hosts and distributing the workload.
    """

    remote_app_dir = "/home/student/krypton"
    hosts_json_path = "./hosts.json"

    def __init__(self):
        with open(self.hosts_json_path) as f:
            # Load the JSON data
            self.hosts = ['lada13@lada.eti.pg.gda.pl'] #json.load(f)

    @classmethod
    def execute_command(cls, host, command):
        """
        Manages remote hosts with use of ssh
        """
        try:
            os.system(f'ssh {host} {command}')
        except Exception as e:
            print(e)

    @classmethod
    def distribute_application(cls):
        """
        Connects to each of the provided hosts, makes a directory where the program is going to be stored,
        sends krypton app, and runs it.
        """
        
        for host in cls.hosts:
            try:
                cls.execute_command(host, f"mkdir {cls.remote_app_dir}")
                os.system(f"scp krypton.py {host}:{cls.remote_app_dir}")
                cls.execute_command(host, f"python {cls.remote_app_dir}/krypton.py")
            except Exception as e:
                print(f"Could not set up the host, there was an issue with: {e}.")

    @classmethod
    def echo_test(cls):
        """
        Method used for testing if connection can be established and simple action can be done.
        """
        for host in cls.hosts:
            try:
                cls.execute_command(host, f'echo I am alive!')
            except Exception as e:
                print(f"Could not set up the host, there was an issue with: {e}.")


    #to be finished
    def establish_section():
        # Create an SSH client
        ssh = paramiko.SSHClient()

        # Automatically add the server's host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh.connect('ip', username='user', password='pass')

        # Execute a command on the remote server
        stdin, stdout, stderr = ssh.exec_command('ls')

        # Print the output of the command
        print(stdout.read().decode())

        # Close the SSH connection
        ssh.close()









    


