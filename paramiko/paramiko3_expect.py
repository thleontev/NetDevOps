import socket
import paramiko
from paramiko_expect import SSHClientInteraction


def main():
    # Set login credentials and the server prompt
    HOSTNAME = '172.16.100.100'
    USERNAME = 'cisco'
    PASSWORD = 'cisco'
    ENABLE = 'cisco'
    PROMPT = '[>#]'

    # Use SSH client to login
    try:
        # Create a new SSH client object
        client = paramiko.SSHClient()

        # Set SSH key parameters to auto accept unknown hosts
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the host
        client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD, allow_agent=False, look_for_keys=False)

        # Create a client interaction class which will interact with the host
        with SSHClientInteraction(client, timeout=5, display=False) as interact:
            interact.expect(PROMPT)

            # Run the first command and capture the cleaned output, if you want
            # the output without cleaning, simply grab current_output instead.
            interact.send('enable')
            interact.expect('[Pp]assword')
            interact.send(ENABLE)
            interact.send('terminal length 0')
            interact.expect(PROMPT) 
            interact.send('sh ver')
            interact.expect(PROMPT)
            cmd_output = interact.current_output

            # Send the exit command and expect EOF (a closed session)
            interact.send('exit')
            interact.expect()

        # Print the output of each command
        print(cmd_output)

    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials: %s")
        return
    except paramiko.SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
        return
    except socket.error as e:
        print("Unable to establish SSH connection: %s" % e)
        return
    except Exception as e:
        print(e.args)
        return
    finally:
        try:
            client.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()