import paramiko
import pathlib
import scp
import os

### ------ Connect through ssh to the remote server ------ ###

# specify working directory

work_dir = pathlib.Path(__file__).parent.absolute()

# Define ssh parameters
host_server_hostname = "192.168.1.81"
host_server_username = "webmaster"
host_server_password = "webmaster"

host_ssh = paramiko.SSHClient()

host_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#host_ssh.connect('<hostname>', username='<username>', password='<password>')

host_ssh.connect(host_server_hostname, username=host_server_username, password=host_server_password)


stdin, stdout, stderr = host_ssh.exec_command("mkdir ~/by_python_script/")

#print (stdout.readlines())

scp1 = scp.SCPClient(host_ssh.get_transport())

file_to_send = str(work_dir) + "/firewall_rules.sh"
print(file_to_send)

scp1.put(file_to_send, '~/by_python_script/firewall_rules.sh')

host_ssh.exec_command("chmod +x ~/by_python_script/firewall_rules.sh")
host_ssh.exec_command("cd ~/by_python_script/ && ./firewall_rules.sh")


scp1.close()

# Nested ssh connection

vmtunnel = host_ssh.get_transport()

dest_add = ('192.168.122.20', 22)
local_add = ('192.168.1.81', 22)

vmchannel = vmtunnel.open_channel("direct-tcpip", dest_add, local_add)

guest_ssh = paramiko.SSHClient()
guest_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
guest_ssh.connect('192.168.122.20', username='ubuntu', password='ubuntu', sock=vmchannel)

stdin, stdout, stderr = guest_ssh.exec_command("mkdir ~/by_python_script/")

#print (stdout.readlines())

scp2 = scp.SCPClient(guest_ssh.get_transport())

file_to_send = str(work_dir) + "/firewall_rules.sh"
print(file_to_send)

scp2.put(file_to_send, '~/by_python_script/firewall_rules.sh')

guest_ssh.exec_command("chmod +x ~/by_python_script/firewall_rules.sh")
guest_ssh.exec_command("cd ~/by_python_script/ && ./firewall_rules.sh")


scp2.close()
guest_ssh.close()

host_ssh.close()
