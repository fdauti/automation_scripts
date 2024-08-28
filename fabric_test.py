from click import echo
from fabric import *
import time
import logging

start = time.time()

hosts = ('192.168.254.250', '192.168.255.2') 
#hosts = ('192.168.248.74', '192.168.249.134', '192.168.254.108') #'192.168.255.68', 
mygroup = ThreadingGroup(*hosts, user='admin', port=22, connect_kwargs={'password':'admin','look_for_keys':False}) #1s
#mygroup = SerialGroup(*hosts, user='admin', port=22, connect_kwargs={'password':'admin','look_for_keys':False}) #2.5s

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(thread)d:%(asctime)s:%(message)s',filename='ssh_test/fabric.log', filemode='w')
results = mygroup.run("version")
print(results)

end = time.time()
print("The time of execution of above program is :", end-start)

# for k,v in results.items():
#   print (k,v)

# def test_connection():
#   try: 
#       logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(threadName)s:%(asctime)s:%(message)s',filename='ssh_test/fabric.log', filemode='w')
#       result = group.run("version", echo=True)
#       if result.failed:
#         print ("This failed", result)
#       else:
#         print ("This succeded", result)
#   except Exception as e:
#     print(e)

# if __name__ == "__main__":
#     start = time.time()
#     test_connection()
#     end = time.time()
#     print("The time of execution of above program is :", end-start)