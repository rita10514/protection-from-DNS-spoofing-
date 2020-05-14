

import dns.resolver as dr
import os
import time


def read_user_request(path):
    my_resolver = dr.Resolver()
    zones = open(path, 'r')
    lines = zones.readlines()  #go trough all the zones and  saving them in a list
    zones.close()
    numofzones = len(lines)
    zones = open(path, 'w')
    for line in lines:
        #making a request to the dns above to get the ip of the "request"d
        rname, rtype, ip = line.split(maxsplit=2)
        my_resolver.nameservers = ['8.8.8.8'] 
        #defing the dns to be a random ip from the list of ips
        answer='no result'
        try:
           answer = my_resolver.query(rname)#making a request to the dns above to get the ip of the "request"
           answer= str(answer.response.answer[0]).split(' ')[4]
        except:
           zones.write(line)
        
    zones.close()
    return 0


if __name__ == "__main__":

    path = '/home/rita/Downloads/zones.txt'

    try:
        while True:
            read_user_request(path)
            time.sleep(3600)
    except KeyboardInterrupt:
        pass  
    

