import pexpect
import re
from pprint import pprint


def send_show_command(ip, username, password, enable, commands, prompt="#"):
    with pexpect.spawn(f"ssh -o KexAlgorithms=diffie-hellman-group14-sha1 -o HostkeyAlgorithms=+ssh-rsa -o Ciphers=aes128-ctr {username}@{ip}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        enable_status = ssh.expect([">", "#"])
        if enable_status == 0:
            ssh.sendline("enable")
            ssh.expect("[Pp]assword")
            ssh.sendline(enable)
            ssh.expect(prompt)

        ssh.sendline("terminal length 0")
        ssh.expect(prompt)

        result = {}
        for command in commands:
            ssh.sendline(command)
            match = ssh.expect([prompt, pexpect.TIMEOUT, pexpect.EOF])
            if match == 1:
                print(
                    f"Символ {prompt} не найден в выводе. Полученный вывод записан в словарь"
                )
            if match == 2:
                print("Соединение разорвано со стороны сервера")
                return result
            else:
                output = ssh.before
                result[command] = output.replace("\r\n", "\n")
        return result


if __name__ == "__main__":
    devices = ["172.16.100.100", "172.16.100.102"]
    commands = ["sh clock", "sh int desc"]
    for ip in devices:
        result = send_show_command(ip, "cisco", "cisco", "cisco", commands)
        pprint(result, width=120)