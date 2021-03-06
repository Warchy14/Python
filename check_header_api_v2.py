#!/usr/bin/env python2.7

import urllib2,sys,ssl
import os,time,socket,platform
from optparse import OptionParser

#Class colors headers
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[93m'
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# Client headers to send to the server during the request.
client_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0)\
 Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,\
 application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US;q=0.8,en;q=0.3',
    'Upgrade-Insecure-Requests': 1
 }


# Security headers dictionnary 
sec_headers = {
    'x-xss-protection': 'warning',
    'X-Frame-Options': 'warning',
    'x-content-type-options': 'warning',
    'Strict-Transport-Security': 'error',
    'Content-Security-Policy': 'warning',
    'feature-policy': 'warning',
}

# Information headers dictionnary
information_headers = {
    'X-Powered-By',
    'Server',
    'X-AspNetMvc-Version',
    'X-AspNet-Version',
    'X-Generated-By',
    'Cookie',
   
}

# Cache headers dictionnary
cache_headers = {
    'Cache-Control',
    'Pragma',
    'Last-Modified'
    'Expires',
    'Content-Type',
    'ETag'
}

#API Headers
api_headers = {
	'X-Permitted-Cross-Domain-Policies',
    'Referrer-Policy',
    'Feature-Policy',
    'Access-Control-Allow-Origin'
}


#Headers input empty
headers = {}

#Loading animation
def loading():

    user_os = platform.system()

    if user_os == 'Linux' or user_os == 'Darwin':
        user_clean = 'clear'
    else:
        user_clean = 'cls'

    i = 0
    while i <= 5:
        print "[|] Start Scanning "
        time.sleep(0.1)
        os.system(user_clean)
        print "[/] Start Scanning ."
        time.sleep(0.1)
        os.system(user_clean)
        print "[-] Start Scanning .."
        time.sleep(0.1)
        os.system(user_clean)
        print "[\] Start Scanning ..."
        time.sleep(0.1)
        if i == 5:
            time.sleep(0.1)
            os.system(user_clean)
            print "[+] Scanning "
            return
        os.system(user_clean)
        i += 1

#Banner
def banner():
    print
    print "======================================================================================================================================================================="
    print """
		 __    __  .___________.___________..______       __    __   _______     ___       _______   _______ .______          _______.
		|  |  |  | |           |           ||   _  \     |  |  |  | |   ____|   /   \     |       \ |   ____||   _  \        /       |
		|  |__|  | `---|  |----`---|  |----`|  |_)  |    |  |__|  | |  |__     /  ^  \    |  .--.  ||  |__   |  |_)  |      |   (----`
		|   __   |     |  |        |  |     |   ___/     |   __   | |   __|   /  /_\  \   |  |  |  ||   __|  |      /        \   \    
		|  |  |  |     |  |        |  |     |  |         |  |  |  | |  |____ /  _____  \  |  '--'  ||  |____ |  |\  \----.----)   |   
		|__|  |__|     |__|        |__|     | _|         |__|  |__| |_______/__/     \__\ |_______/ |_______|| _| `._____|_______/    
                                                                                                                              

									Author : Pierre-Marie Quantin                                             
                  							Year   : 24/08/2019

      """                                                                  
    print ""

#Colors code
def colorize(string, alert):
    color = {
        'error':    bcolors.FAIL + string + bcolors.ENDC,
        'warning':  bcolors.WARNING + string + bcolors.ENDC,
        'ok':       bcolors.OKGREEN + string + bcolors.ENDC,
        'info':     bcolors.OKBLUE + string + bcolors.ENDC
    }
    return color[alert] if alert in color else string

#Header analyse and split
def parse_headers(hdrs):
    map(lambda header: headers.update((header.rstrip().split(':', 1),)), hdrs)

#Add port in the target url
def append_port(target, port):
    return target[:-1] + ':' + port + '/' \
        if target[-1:] == '/' \
        else target + ':' + port + '/'

#Check if SSL certificat is OK
def get_unsafe_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

#Print error if URL is KO
def print_error(e):
    if isinstance(e, ValueError):
        print "Unknown url type"

    if isinstance(e, urllib2.HTTPError):
            print "[!] URL Returned an HTTP error: {}".format(
                colorize(str(e.code), 'error'))

    if isinstance(e, urllib2.URLError):
            if "CERTIFICATE_VERIFY_FAILED" in str(e.reason):
                print "SSL: Certificate validation error.\nIf you want to \
    ignore it run the program with the \"-d\" option."
            else:
                print "Target host seems to be unreachable"

#Check if target is OK
def check_target(target, options):
    ssldisabled = options.ssldisabled
 
    response = None

    try:
        request = urllib2.Request(target, headers=client_headers)

        # Set HTTP method to HEAD
        method = 'HEAD'
        request.get_method = lambda: method
        
        # Set certificate validation
        if ssldisabled:
            context = get_unsafe_context()
            response = urllib2.urlopen(request, timeout=10, context=context)
        else:
            response = urllib2.urlopen(request, timeout=10)

    except Exception as e:
        print_error(e)
        sys.exit(1)

    if response is not None:
        return response
    print "Couldn't read a response from server."
    sys.exit(3)

#Check if target support HTTPS for HSTS Header (Strict-Transport-Security)
def is_https(target):
    return target.startswith('https://')

#Global report with target and options 
def report(target, safe, unsafe, infohead, cachecontrol,apihead):
    print
    print "-------------------------------------------------------"
    print "Headers analyzed for {}".format(colorize(target, 'info'))
    print
    print "{} security headers enabled".format(colorize(str(safe), 'ok'))
    print
    print "{} security headers missing".format(colorize(str(unsafe), 'error'))
    print
    if infohead > 0 :
    	print "{} information headers".format(colorize(str(infohead), 'info'))
    	print
    if cachecontrol >0 :
    	print "{} cache control headers".format(colorize(str(cachecontrol), 'info'))
    	print
    if apihead >0 :
    	print "{} API headers".format(colorize(str(cachecontrol), 'info'))
    	print
    print "======================================================================================================================================================================="
    print ""


def main(options, targets):
    # Getting options
    port = options.port
    information = options.information
    cache_control = options.cache_control
    api = options.api
    
    loading()
    banner()

    for target in targets:
        if port is not None:
            target = append_port(target, port)
        
        safe = 0
        unsafe = 0
        infohead = 0
        cachecontrol = 0
        apihead = 0

        # Check if target is valid
        response = check_target(target, options)
        rUrl = response.geturl()

        print "Effective URL: {}".format(colorize(rUrl, 'info'))
        parse_headers(response.info().headers)

        for safeh in sec_headers:
            if safeh in headers:
                safe += 1

                # X-XSS-Protection Should be enabled
                if safeh == 'X-XSS-Protection' and headers.get(safeh) == '0':
                    print "Header {} is enabled (Value: {})".format(colorize(safeh, 'ok'), colorize(headers.get(safeh), 'warning'))
                    print "X-XSS-Protection is disabled"

                # Printing global message if security header is enabled
                else:
                    print "Header {} is enabled (Value: {})".format(colorize(safeh, 'ok'), headers.get(safeh))
            else:
                unsafe += 1

                # HSTS works only with HTTPS url
                if safeh == 'Strict-Transport-Security' and not is_https(rUrl):
                    unsafe -= 1
                    continue
                print 'Missing security header: {}'.format(colorize(safeh, sec_headers.get(safeh)))

        if information:
            i_chk = False
            for infoh in information_headers:
                if infoh in headers:
                    i_chk = True
                    infohead += 1
                    print 
                    print "-------------------------------------------------------"
                    print "Information header: \
header {} is enabled (Value: {})".format(colorize(infoh, 'info'), headers.get(infoh))
            	
            if not i_chk:
                print
                print "-------------------------------------------------------"
                print "No information  header detected"
                infohead = 0
        if cache_control:
            c_chk = False
            for cacheh in cache_headers:
                if cacheh in headers:
                    c_chk = True
                    cachecontrol += 1
                    print
                    print "-------------------------------------------------------"
                    print "Cache control header {} is enabled \
(Value: {})".format(colorize(cacheh, 'info'),headers.get(cacheh))
            if not c_chk:
                print
                print "-------------------------------------------------------"
                print "No caching headers detected"

        if api:
            a_chk = False
            for apih in api_headers:
                if apih in headers:
                    a_chk = True
                    apihead += 1
                    print
                    print "-------------------------------------------------------"
                    print "API header {} is enabled \
(Value: {})".format(colorize(apih, 'info'),headers.get(apih))
            if not a_chk:
                print
                print "-------------------------------------------------------"
                print "No API header detected"

        report(rUrl, safe, unsafe, infohead,cachecontrol,apihead)


if __name__ == "__main__":

    parser = OptionParser("Usage: %prog <url> [options]", prog=sys.argv[0])

    parser.add_option("-p", "--port", dest="port",
                      help="Set a custom port to connect to",
                      metavar="PORT")
    parser.add_option('-d', "--disable-ssl-check", dest="ssldisabled",default=False,
                      help="Disable SSL/TLS certificate validation",
                      action="store_true")
    parser.add_option("-i", "--information", dest="information", default=False,
                      help="Display information headers",
                      action="store_true")
    parser.add_option("-c", "--caching", dest="cache_control", default=False,
                      help="Display caching headers",
                      action="store_true")
    parser.add_option("-a", "--api", dest="api", default=False,
    				  help="Display api headers",
    				  action="store_true")

    (options, args) = parser.parse_args()

    if len(args) < 1 :
        parser.print_help()
        sys.exit(1)

    t1 = time.time()

    main(options, args)

    t2 = time.time()

    diff = t2 - t1

    print "Execution time: %s secondes " % round(diff,1)
    print
