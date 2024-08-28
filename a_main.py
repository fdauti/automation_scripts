from schema import Schema, Or, Optional, SchemaError, And, Use
from io import StringIO
import paramiko, time, yaml, logging, json, textfsm
import concurrent.futures
from pythonping import ping
from icmplib import traceroute

class NetddLog():
   def __init__(self, name, format="%(asctime)s|%(name)s|%(funcName)s|%(threadName)s|%(levelname)s: %(message)s", level=logging.DEBUG): #%(funcName)s %(threadName)s
      self.name = name
      self.level = level
      self.format = format
       
      #Logger configuration.
      self.formatter = logging.Formatter(self.format)
      self.log_capture_string = StringIO()
      self.ch_logger = logging.StreamHandler(self.log_capture_string)
      self.ch_logger.setFormatter(self.formatter)
      self.logger = logging.getLogger(name)
      self.logger.setLevel(self.level)
      self.logger.addHandler(self.ch_logger)

   def debug(self, msg, extra=None):
      self.logger.debug(msg, extra=extra)
   def info(self, msg, extra=None):
      self.logger.info(msg, extra=extra)
   def error(self, msg, extra=None):
      self.logger.error(msg, extra=extra)
   def warning(self, msg, extra=None):
    self.logger.warning(msg, extra=extra)

#Parse the yaml dump file, raise any syntax error
#Add each separate yaml doc inside the dump file to a list
dump_file = '/home/labuser/DEV/co-op/yaml/dump.yml'
yml_list = []
with open(dump_file, 'r') as file:
    try:
        yml_data = yaml.safe_load_all(file) #generator obj.
        for yml_doc in yml_data:
            yml_list.append(yml_doc)
    except yaml.YAMLError as ye:
        print("Syntax error in Yaml dump file:")
        print(ye)

#Define a separate schema for each type of yaml doc.
ycli_schema = Schema({
"type": "ycli",
"version": lambda n: n>0,
"name": str,
"detect": [
{ "name": str },
{ Optional("ssh"): [
    { Or("Server", "Cypher"): str }
    ]
},
{ Optional("banner"): None, "contains": str },
{ Optional("commands"): [
    { "cmd": str },
    { Optional("cmd"): str, "contains": str }
    ]
}
],
Optional("cli"): [
{ "cmd": str },
{ "cmd": str, Optional("match"): [
    { Or("existing", "new", ignore_extra_keys=True) },
    { Optional("existing"): str },
    { Optional("new"): str, "textfsm": str },
    { Optional("new"): str, "contains": str }
    ]
},
{ "cmd": str, Optional("runif"): [
    { "ipsm": str, "contains": None }
    ]
},
{ "cmd": str },
{ "cmd": str },
{ "cmd": str }
]
})
ylib_schema = Schema({
"type": "ylib",
"version": lambda n: n>0,
"name": str,
Optional('import'): [
{ "name": str, "list":[
        str,
    ]
}
],
Optional('match'): { "textfsm": str }
})
ycfg_schema = Schema({
"type": "ycfg",
"version": lambda n: n>0,
"name": str,
})
yvis_schema = Schema({
"type": "yvis",
"version": lambda n: n>0,
"name": str,
})

#Add each yaml doc. to a separate list based on its type
#Validate each yaml doc. separately based on its type
ycli_list=[]
ylib_list=[]
ycfg_list=[]
yvis_list=[]

for i in range(len(yml_list)):
    if yml_list[i]['type'] == 'ycli':
        try:
            ycli_schema.validate(yml_list[i])
            print(f"Ycli schema for '{yml_list[i]['name']}' is valid.")
            ycli_list.append(yml_list[i])
            #print(ycli_list)
        except SchemaError as se:
            print(f"Ycli schema for '{yml_list[i]['name']}' is invalid.")
            print(se)
    elif yml_list[i]['type'] == 'ylib':
        try:
            ylib_schema.validate(yml_list[i])
            print(f"Ylib schema for '{yml_list[i]['name']}' is valid.")
            ylib_list.append(yml_list[i])
            #print(ylib_list)
        except SchemaError as se:
            print(f"Ylib schema for '{yml_list[i]['name']}' is invalid.")
            print(se)
    elif yml_list[i]['type'] == 'ycfg':
        try:
            ycfg_schema.validate(yml_list[i])
            print(f"Ycfg schema for '{yml_list[i]['name']}' is valid.")
            ycfg_list.append(yml_list[i])
            #print(ycfg_list)
        except SchemaError as se:
            print(f"Ycfg schema for '{yml_list[i]['name']}' is invalid.")
            print(se)
    elif yml_list[i]['type'] == 'yvis':
        try:
            yvis_schema.validate(yml_list[i])
            print(f"Yvis schema for '{yml_list[i]['name']}' is valid.")
            yvis_list.append(yml_list[i])
            #print(yvis_list)
        except SchemaError as se:
            print(f"Yvis schema for '{yml_list[i]['name']}' is invalid.")
            print(se)
    else:
        print(f"Unknown type of yaml document in '{yml_list[i]['name']}'")

ipsl = []
ipsm = {}

# test_logger = NetddLog("TEST")
# test_logger.info("Writting to the log")
# log_contents = test_logger.log_capture_string.getvalue()
# ipsl.append(log_contents)

def ip_probe():

    def ping_ip(device):
        try: 
            my_payload=1500
            while 64 <= my_payload <= 1500:
                result = ping(device, count=5, df=True, payload=str(my_payload))
                if result.success:
                    break
                else:
                    my_payload -= 200
            print(result)

            # json_ping = (json.dumps({"hostIP":result.address,"packets_sent":result.packets_sent,"packets_received":result.packets_received}))
            # print(json_ping)

        except Exception as err:
            print("Error inside the ping_ip function!")
            print(err)

    ping_ip(device)


    def traceroute_ip(device):
        try:
            hops = traceroute(device,count=2)
            print('Distance/TTL  \t  Address  \t\t  Average round-trip time')
            for hop in hops:
                print(f'{hop.distance}  \t\t  {hop.address}  \t  {hop.avg_rtt} ms')

            json_tr = (json.dumps({"IP":hop.address,"Hop":hop.distance,"Avg_rtt":hop.avg_rtt}))
            print(json_tr)

        except traceroute.SocketPermissionError:
            print(" privileges are insufficient to create the socket")
        except Exception as err:
            print("Error inside the traceroute_ip function!")
            print(err)

    traceroute_ip(device)
    

with open('/home/labuser/DEV/ossdemo/yaml/ip_list.txt') as f:
    try:
        for line in f:
            if line.startswith('#') or len(line.split()) == 0:
                #Skip comment or empty line in the ip_list file
                pass
            elif len(line.strip().split(',')) == 4:
                device, username, password, port = line.strip().split(',')
                ip_probe()
            elif len(line.strip().split(',')) == 3:
                device, username, password = line.strip().split(',')
                ip_probe()
            else:
                device = line.strip()
                ip_probe()
    except FileNotFoundError:
        print("File with list of IPs not found!")
    except:
        print("IP list format format not correct")
        print("Correct syntax is: IP(required),Username,Password,Port")


def ssh_Terminal(device, username, password, port=22):

    def sshConnect(device, username, password, port):
        ssh_logger = NetddLog('PARAMIKO')

        client = paramiko.SSHClient()
        client.set_log_channel('PARAMIKO')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(device, username=username, password=password, port=port, look_for_keys=False, allow_agent=False)
        print(f'Successfully connected to {device}')

        chan = client.invoke_shell()
        print('Interactive SSH session established')
        #chan.send('\n')
        time.sleep(2)
        resp = chan.recv(5000).decode("utf-8")

        log_contents = ssh_logger.log_capture_string.getvalue()
        #print(log_contents.strip()) #prints the list line by line

        global ipsl
        ipsl.append(log_contents)
        return resp

    sshConnect(device, username, password, port)


# from pprint import pprint
# #pprint(ipsl, width=120)

# #print("\n",ipsl,"\n", sep='')
# for i in ipsl:
#     print(i)


# if __name__ == "__main__":
#     start = time.time()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         executor.submit(netdd('192.168.255.68','admin','admin','22'))
#         executor.submit(netdd('192.168.254.108','admin','admin','22'))
#     end = time.time()
#     print("Execution time:", end-start)

#dump ipsl dictionary into a json object
# ipsl_json = json.dumps(ipsl)
# print(ipsl_json)

# for i in range(len(ycli_list)):
#    if 'detect' in ycli_list[i].keys():
#       print('Detect')

# def getBanner():
#    banner_list = []

#    banner_list.append(ycli_list[i]['detect'][2]['banner'][0]['contains'])
#    print(banner_list)
#    return banner_list

# for i in log_contents.split('\n'):
#     print(i)

# def detectBanner():
#     if loaded_ycli['detect'][1]['banner'] in output:
#         print("Target OS of the device is:", loaded_ycli['detect'][0]['name'])
#         return "ROS"
#     else:
#         print("Target OS of the device is Unkown!")

#if __name__ == "__main__":
   # sshTest('192.168.255.68','admin','admin','22')
   # sshTest('192.168.254.108','admin','admin','22')
   # print(ipsl)
#     detectBanner()


#print(yml_list[0]['detect'][2]['banner'][0]['contains'])
# validated = config_schema.validate(yml_list[0])
# print(validated) #dict

# print(ycli_list[0]['detect'][2]['banner'][0]['contains'])
# def readBanner(ycli_list):
#     for i in ycli_list:

#Or("ycli","ylib","ycfg","yvis")
#Check if each yaml docs. confirm to the configuration schema
# for i in range(len(yml_list)):
#     try:
#         config_schema.validate(yml_list[i])
#         print(f"Schema for '{yml_list[i]['name']}' is valid.")
#     except SchemaError as se:
#         print(f"Schema for '{yml_list[i]['name']}' is invalid.")
#         print(se)