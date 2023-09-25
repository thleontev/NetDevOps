# GNS3 test
import pexpect

prompt="#"

tln = pexpect.spawn('telnet localhost 5004')
tln.sendline()
tln.expect('[>#]')

tln.sendline("terminal length 0")
tln.expect(prompt)

tln.sendline("show run")
match = tln.expect([prompt, pexpect.TIMEOUT, pexpect.EOF])

tln.before
show_output = tln.before.decode('utf-8')
print(show_output)

tln.close()