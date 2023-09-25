import pexpect

#ssh = pexpect.spawn('ssh cisco@172.16.100.100')
ssh = pexpect.spawn('ssh -o KexAlgorithms=diffie-hellman-group14-sha1 -o HostkeyAlgorithms=+ssh-rsa -o Ciphers=aes128-ctr cisco@172.16.100.100')
ssh.expect('[Pp]assword')
ssh.sendline('cisco')
ssh.expect('[>#]')

ssh.sendline('enable')
ssh.expect('[Pp]assword')
ssh.sendline('cisco')
ssh.expect('[>#]')

ssh.sendline('sh ip int br')
ssh.expect('#')

ssh.before
show_output = ssh.before.decode('utf-8')
print(show_output)

ssh.close()