DNS spoofing using IOT's
==============
Our idea is to create a new DNS infrastructure that could work in a full synthesis with the existing one. 
This system will provide a higher verification ability without changing the existing DNS hierarchy and the 
protocol mechanism. Moreover, this system will provide more reliable answers since it would be harder for an
 attacker to fake them.

---

## Preparation of the iot’s:

1. Take as much as possible iots devices that support linux system


2. Install linux on the raspberry-pi in this [link](https://thepi.io/how-to-run-raspberry-pi-desktop-on-windows-or-macos/).
          
3. Configure the RPI so that the DNS server will run at boot time. here is a 
   [link]( https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) for the tutorial.       
  
   
4. Check the ips of the iots with the command `ifconfig` and put them in the zone file
 
5. The iots ips has to be fixed (use router configuration to accomplish this)

6. All zone files need to be in the same folder with the dns.py file.

7. In the dns code (in the main) you need to change the path to the right location. 


## Preparation of the mediator:

1. Prepare a zone file with the iots ip.

2. The ips zone file needs to be in the same folder with the mediator.py.

3. In the mediator code, change the path in line 61 to your folder.

## Preparation of the system:

1. Run all iots under the same network.

2. Run the mediator.

3. Send from the client computer the commend:
   Nslookup    ___url____   ____DNS’s ip address__.
   ( "url"  -  the name of the website your searching ,  "DNS’s ip address" -  the ip of the dns you send the query to)

---

### Notes:

- If you want to see the procedure in the mediator you can connect a screen to the computer that runs the mediator.

- If you want to see the procedure in the iot’s you can screen to the iots.



