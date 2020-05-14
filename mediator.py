import random
import signal
import dns.resolver as dr
import os
from dnslib.server import DNSServer
import logging
from dnslib import *
import dnslib
from dnslib.proxy import ProxyResolver
from time import sleep
from scapy.all import DNS,DNSQR,DNSRR,dnsqtypes
from dnslib import DNSLabel, QTYPE, RR, dns

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S'))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

TYPE_LOOKUP = {
    'A': (dns.A, QTYPE.A),
    'AAAA': (dns.AAAA, QTYPE.AAAA),
    'CAA': (dns.CAA, QTYPE.CAA),
    'CNAME': (dns.CNAME, QTYPE.CNAME),
    'DNSKEY': (dns.DNSKEY, QTYPE.DNSKEY),
    'MX': (dns.MX, QTYPE.MX),
    'NAPTR': (dns.NAPTR, QTYPE.NAPTR),
    'NS': (dns.NS, QTYPE.NS),
    'PTR': (dns.PTR, QTYPE.PTR),
    'RRSIG': (dns.RRSIG, QTYPE.RRSIG),
    'SOA': (dns.SOA, QTYPE.SOA),
    'SRV': (dns.SRV, QTYPE.SRV),
    'TXT': (dns.TXT, QTYPE.TXT),
    'SPF': (dns.TXT, QTYPE.TXT),
}

class Record:
    def __init__(self, rname, rtype, args):
        self._rname = DNSLabel(rname)

        rd_cls, self._rtype = TYPE_LOOKUP[rtype]

        if self._rtype == QTYPE.SOA and len(args) == 2:
            # add sensible times to SOA
            args += (SERIAL_NO, 3600, 3600 * 3, 3600 * 24, 3600),

        if self._rtype == QTYPE.TXT and len(args) == 1 and isinstance(args[0], str) and len(args[0]) > 255:
            # wrap long TXT records as per dnslib's docs.
            args = wrap(args[0], 255),

        if self._rtype in (QTYPE.NS, QTYPE.SOA):
            ttl = 3600 * 24
        else:
            ttl = 300
       
        self.rr = RR(
            rname=self._rname,
            rtype=self._rtype,
            rdata=rd_cls(str(*args)),
            ttl=ttl,
        )

class Resolver(ProxyResolver):

    def __init__(self):
        super().__init__(53, 5)


    def read_user_request(self,request, path):
        my_resolver = dr.Resolver()
        dict = {}
        maxvotes = 0
        final_answer = ""
        F = open(path, 'r')

        ips = F.readlines()  #go trough all the dns ips and  saving them in a list
        totalIOTnum = len(ips)
        IOTnum2ask = max(int(totalIOTnum*0.01),7)
        Xcount = 0
        #sending request to rendem dns servers
        i=1
        while i<=IOTnum2ask and Xcount<totalIOTnum:
            random_index = random.randint(0,totalIOTnum-1)
          
        if ips[random_index]!= "X" : # so we woun't get the same ip twice
                i=i+1
                my_resolver.nameservers = [ips[random_index].strip()] #defing the dns to be a random ip from the list of ips
                print("ask " + ips[random_index].strip() + " which answers ")
                ips[random_index] = "X" # so we woun't get the same ip twice
                Xcount=Xcount+1
                try:
                   answer = my_resolver.query(request) #making a request to the dns above to get the ip of the "request"
                except:
                   answer = "no result"
                   i = i - 1

                if answer!="no result":
                    for rdata in answer:
                        print(rdata)
                        if not rdata in dict: #if this ip doesn't exists in the dict add it with count one
                            dict[rdata] = 1
                        else: dict[rdata] = dict[rdata]+1  #if it does exists count++
                        # updating the max count value and the most common answer
                        if maxvotes < dict[rdata]:
                            maxvotes = dict[rdata]
                            final_answer = rdata



                        
                        for key,val in dict.items():
                            print(key , "=>" , val)
                        print("\n")

                else:
                    print(answer+"\n")

        if final_answer == '': 
           final_answer = '204.74.99.100'
        return final_answer


    def resolve(self, request, handler):
        path = '/home/rita/Downloads/ips.txt'
        rname = str(request.questions[0].get_qname())[:-1]
        args = self.read_user_request(rname, path)
        args = (args,)
       
        #assert d.opencode == 0,d.opencode
        #assert dnsqtypes[d[DNSQR].qtype] == 'A',d[DNSQR].qtype 
        rtype='A'
        record = Record(rname, rtype, args)
        reply = request.reply()
        reply.add_answer(record.rr)


    
        #type_name = QTYPE[request.q.qtype]
        #reply = request.reply()
        #reply.add_answer(answer)

        if reply.rr:
            #logger.info('found zone for %s[%s], %d replies', request.q.qname, type_name, len(reply.rr))
            return reply

        return super().resolve(request, handler)

def handle_sig(signum, frame):
    logger.info('pid=%d, got signal: %s, stopping...', os.getpid(), signal.Signals(signum).name)
    exit(0)


if __name__ == "__main__":

   

    signal.signal(signal.SIGTERM, handle_sig)
    port = int(os.getenv('PORT', 53))
    resolver = Resolver()
    udp_server = DNSServer(resolver, port=port)
    udp_server.start_thread()

    try:
        while udp_server.isAlive():
            sleep(1)
    except KeyboardInterrupt:
        pass
