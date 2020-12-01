import paramiko
import pathlib
import scp
import os

### ------ Connect through ssh to the remote server ------ ###

# specify working directory

work_dir = pathlib.Path(__file__).parent.absolute()

# Define ssh parameters
remote_server_hostname = ""
remote_server_username = ""
remote_server_password = ""

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#ssh.connect('<hostname>', username='<username>', password='<password>')

ssh.connect(remote_server_hostname, username=remote_server_username, password=remote_server_password)


stdin, stdout, stderr = ssh.exec_command("mkdir ~/by_python_script/")

#print (stdout.readlines())

scp1 = scp.SCPClient(ssh.get_transport())

file_to_send = str(work_dir) + "/firewall_rules.sh"
print(file_to_send)

scp1.put(file_to_send, '~/by_python_script/firewall_rules.sh')




scp1.close()
ssh.close()
