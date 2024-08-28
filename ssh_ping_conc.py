import concurrent.futures
import paramiko
import subprocess, time, logging

logging.basicConfig(level=logging.INFO, format='%(threadName)s:%(levelname)s:%(asctime)s:%(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(threadName)s:%(asctime)s:%(message)s',filename='/home/labuser/DEV/ossdemo/ssh_test/paramiko_concurrent.log', filemode='w')


def sshTest(ipaddress, deviceUsername, devicePassword, sshPort): 
    try:
        print("Performing SSH Connection to the device")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ipaddress, username=deviceUsername, password=devicePassword, port=sshPort, look_for_keys=False, allow_agent=False)

        stdin, stdout, stderr = client.exec_command("who")
        output = stdout.read()
        return output
    except Exception as ex:
        print(ex)
        #return "failed to connect"

def pingf(ip):
    output = subprocess.check_output(["ping", "-c", "5", ip])
    #return output

def main():
    future_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list.append(executor.submit(pingf, "192.168.255.68"))
        future_list.append(executor.submit(sshTest, "192.168.255.68", "admin", "admin", "22"))
        # future_list.append(executor.submit(pingf, "192.168.248.74"))
        # future_list.append(executor.submit(sshTest, "192.168.248.74", "admin", "admin", "22"))
        # future_list.append(executor.submit(pingf, "192.168.249.134"))
        # future_list.append(executor.submit(sshTest, "192.168.249.134", "admin", "admin", "22"))
        future_list.append(executor.submit(pingf, "192.168.254.108"))
        future_list.append(executor.submit(sshTest, "192.168.254.108", "admin", "admin", "22"))

    #Future is returned as soon as work is completed, not in the order of adding to future_list    
    for future in concurrent.futures.as_completed(future_list):
        print("return value from task:", future.result())

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("The time of execution of above program is :", end-start) #8secd