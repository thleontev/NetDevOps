import pexpect
import re
from pprint import pprint
import json

api_user = "admin"
api_password = "pfihm0mWpqqelf6788thE7dlPklvjhC5MH9EWnjuLFl25d0IPIG8lpO5IJAA86VI"

def send_show_command(ip, port, username, password, enable, commands, prompt="#"):
    with pexpect.spawn(f"telnet {ip} {port}", timeout=10, encoding="utf-8") as tln:
        tln.sendline()
        enable_status = tln.expect([">", "#"])
        if enable_status == 0:
            tln.sendline("enable")
            tln.expect("[Pp]assword")
            tln.sendline(enable)
            tln.expect(prompt)

        tln.sendline("terminal length 0")
        tln.expect(prompt)

        result = {}
        for command in commands:
            tln.sendline(command)
            match = tln.expect([prompt, pexpect.TIMEOUT, pexpect.EOF])
            if match == 1:
                print(
                    f"Символ {prompt} не найден в выводе. Полученный вывод записан в словарь"
                )
            if match == 2:
                print("Соединение разорвано со стороны сервера")
                return result
            else:
                output = tln.before
                result[command] = output.replace("\r\n", "\n")
        return result


if __name__ == "__main__":
    # get opened project
    l_projects = []
    api = pexpect.spawn(f"curl --user {api_user}:{api_password} http://localhost:3080/v2/projects", timeout=10, encoding="utf-8")
    api.expect(pexpect.EOF)
    json_obj = api.before
    obj = json.loads(json_obj)
    for item in obj:
        if item['status']=="opened":
            l_projects.append({'status':item['status'], 'project_id':item['project_id'], 'filename':item['filename']})
    api.close
    
    # get list of nodes
    l_nodes = []
    project_id = l_projects[0]['project_id']
    api = pexpect.spawn(f"curl --user {api_user}:{api_password} http://localhost:3080/v2/projects/{project_id}/nodes", timeout=10, encoding="utf-8")
    api.expect(pexpect.EOF)
    json_obj = api.before
    obj = json.loads(json_obj)
    for item in obj:
         if item['status']=="started":
            l_nodes.append({'node_id':item['node_id'], 'name':item['name'], 'status':item['status'], 'console_host':item['console_host'], 'console_type':item['console_type'],  'console':item['console']})    
    api.close

    commands = ["sh run"]
    for item in l_nodes:
        if str(item['console']).strip() !='None':
            print("> Connect to ...",item['name'], item['console'])
            result = send_show_command(item['console_host'], item['console'], "cisco", "cisco", "cisco", commands)
            with open(f"{str(item['name']).strip()}_conf.txt", "w") as f:
                f.write(str(result[commands[0]]))
