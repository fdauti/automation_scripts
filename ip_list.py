import re
def valid_ip(ip):
    '''Function to validate IPv4 format in IP list using regex
    '''
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        return ip
    else:
        print('wrong ip')

def valid_port(port):
    '''Function to validate SSH port range
    '''
    if port.isdecimal():
        return port
    else:
        print("wrong ssh port format:", port)

#Get a list of IPs to run the main ip session function on
#e.g [['192.168.254.78', 'root', 'admin'], '192.168.254.86']
ip_list = []
with open('../_main/files/ip_list.yml') as f: #/home/labuser/DEV/co_op/_main/
    try: 
        for line in f.readlines():
            #print(line.rstrip().partition('#')[0])
            print(len(line.partition('#')[0].rstrip().split(',')))
            if line[0].isdecimal() == False:
                #Skip lines not starting with a number
                pass
            elif len(line.partition('#')[0].rstrip().split(',')) == 1:
                #Check to see if only IP is provided, skip comments at the end of line
                ip = line.partition('#')[0].rstrip()
                if valid_ip(ip):
                    ip_list.append(ip)
            elif len(line.partition('#')[0].rstrip().split(',')) == 3:
                #IP, username, password and optional port number provided
                ip = line.partition('#')[0].rstrip().split(',')
                if valid_ip(ip[0]):
                    ip_list.append(ip)
            elif len(line.partition('#')[0].rstrip().split(',')) == 4:
                ip = line.partition('#')[0].rstrip().split(',')
                if valid_ip(ip[0]): 
                    if ip[3].isnumeric():
                        ip_list.append(ip)
                    else:
                        print(f"Not a valid port definition: {ip[3]} in {ip}")
            elif len(line.partition('#')[0].rstrip().split(',')) > 4:
                ip = line.partition('#')[0].rstrip().split(',')
                print(f"Not a valid definition, check ambiguous ',' in the line: {ip}")
    except FileNotFoundError as err:
        print("Missing IP list file!")
    except Exception as ex:
        print(ex)

print(ip_list)