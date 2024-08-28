import textfsm, paramiko, tempfile, time, yaml, json, io

# Connection info
ip = '192.168.254.108' 
user = 'admin'
pwd = 'admin'

dump_file = '/home/labuser/DEV/co_op/v2/dump.yml'
yml_list = []
with open(dump_file, 'r') as file:
   try:
      yml_data = yaml.safe_load_all(file) #generator obj.
      for yml_doc in yml_data:
         yml_list.append(yml_doc)
    #   yml_dict = next(islice(yml_data, None))
    #   print(yml_dict)
   except yaml.YAMLError as ye:
      print("Syntax error in Yaml configuration file:")
      print(ye)

# def json_extract(obj, key):
#     """Recursively fetch values from nested JSON."""
#     arr = []

#     def extract(obj, arr, key):
#         """Recursively search for values of key in JSON tree."""
#         if isinstance(obj, dict):
#             for k, v in obj.items():
#                 if isinstance(v, (dict, list)):
#                     extract(v, arr, key)
#                 elif k == key:
#                     arr.append(v)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract(item, arr, key)
#         return arr

#     values = extract(obj, arr, key)
#     return values

# yml_string = json.dumps(yml_list[1]) #!!!!!
# yml_json = json.loads(yml_string)

# #Extract 'textfsm' from json object
# txtfsm_val = json_extract(yml_json, 'textfsm')

# #define a r_string to use as template
# r_string = r''''''
# for i in txtfsm_val:
#     r_string += i


def parse_textfsm(template, cmd):
    '''Function for parsing cmd output based on a textfsm template
    '''
    # Create file object in memory
    f = io.StringIO(template)
    # Instantiate a new TextFSM wrapper.
    fsm = textfsm.TextFSM(f)
    # Parse the output text according to template rules.
    fsm_results = fsm.ParseText(output)
    #print(fsm_results) #[['RX1400', 'ROX 2.14.1 (2021-07-26 17:40)', 'RUMF121002717', '6GK60140AM2']]
    # Convert results to list of dictionaries based on template headers
    parsed = [dict(zip(fsm.header, row)) for row in fsm_results]
    #[{'MODEL': 'RX1400', 'RELEASE': 'ROX 2.14.1 (2021-07-26 17:40)', 'SERIAL': 'RUMF121002717', 'MLFB': '6GK60140AM2'}]
    return parsed[0]

# Define a function that we'll use to execute and return CLI output.
def cmd(command):
    """
    Runs a CLI command on a given SSH session, returning output.
    """
    # Create new paramiko instance
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=pwd, port=22, look_for_keys=False, allow_agent=False)
    # Run command and get stdin, stdout, std err streams.
    stdin, stdout, stderr = ssh.exec_command(command)
    # Close this handle, not using it.
    stdin.close()
    # Read regular stdout and std err
    output_ok = stdout.read()
    output_err = stderr.read()
    # Return error text if exist else regular std out.
    # Convert to utf-8 string since python3 paramiko gives byte object
    if output_err:
        return output_err.decode('utf-8')
    else:
        return output_ok.decode('utf-8')

# Get cmd output
output = cmd(command="show chassis chassis-status")

txtfsm_temp = yml_list[1]['match'][0]['textfsm']
#print(txtfsm_temp)
# Parse the cmd output
parsed_output = parse_textfsm(txtfsm_temp, output)

#time.sleep(2)
print(parsed_output)