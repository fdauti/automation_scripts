import textfsm, paramiko, tempfile, time, yaml, json

# Connection info
ip = '192.168.254.108' 
user = 'admin'
pwd = 'admin'

dump_file = '/home/labuser/DEV/co_op/_main/dump.yml'
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

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

yml_string = json.dumps(yml_list[1]) #!!!!!
yml_json = json.loads(yml_string)
txtfsm_val = json_extract(yml_json, 'textfsm')
r_string = r''''''
for i in txtfsm_val:
    r_string += i
print(r_string)

# template_show_chassis_chassis_status = r"""Value MODEL (\S+)
# Value RELEASE (.*)
# Value SERIAL (.*)
# Value MLFB (\S+)

# Start
#   ^\s+model\s+${MODEL}
#   ^\s+mlfb\s+${MLFB} 
#   ^\s+rox release\s+"${RELEASE}"
#   ^\s+system serial number\s+${SERIAL} -> Record
# """

def parse_textfsm(template, output):
# Define the text processing template for cmd output.

    # Create temp file to hold template.
    tmp = tempfile.NamedTemporaryFile(delete=False)

    # Write template to file for textfsm.
    with open(tmp.name, 'w') as f:
        f.write(template)

    # Get read handle for textfsm.
    with open(tmp.name, 'r') as f:
        # Instantiate a new TextFSM wrapper.
        fsm = textfsm.TextFSM(f)
        # Parse the output text according to template rules.
        fsm_results = fsm.ParseText(output)
        # Convert to list of dictionaries since TextFSM may return multiple
        # 'row' results.
        parsed = [dict(zip(fsm.header, row)) for row in fsm_results]

    # Return the parsed data.
    return parsed

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

# Get show version output.
output_t0 = cmd(command="show chassis chassis-status")

# Parse the show clock details.
parsed_t0 = parse_textfsm(template=r_string, output=output_t0)

# Wait for a second to let clock advance.
time.sleep(2)

print(parsed_t0)

# output_t1 = cmd(command="...")
# parsed_t1 = parse_textfsm(template=..., output=output_t1)
# print(parsed_t1)