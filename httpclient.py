#!/usr/bin/env python
# coding: utf-8
# Copyright 2017 Abram Hindle, https://github.com/tywtyw2002, https://github.com/treedust, and Nicole Lovas
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
	#from the example in https://docs.python.org/2/library/socket.html#socket.socket.connect

        cskt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = int(port)
	cskt.connect(( host,port ))
        return cskt

    def get_code(self, data):
	parts = data.split(" ")
	kode = parts[1]
	return kode

    def get_headers(self,data):
	headers = data.split('\r\n\r\n')
	return headers[0]

    def get_body(self, data):
	parts = data.split('\r\n\r\n')
	bodi = parts[1]        
	return bodi

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
	#I had to redo this sooo many times and just restarted so. There's no function calls for this.
	#get the host
	pieces = url.split('http://')
	hostwpnpgs = pieces[1]
	splitslash = hostwpnpgs.split('/')
	hostwp = splitslash[0]
	#but if it has a port in it, get the port and shorten the url
	port = 80

	if(':' in hostwp):
#referenced Ryan Satyabrata's repo to figure out how to check if there's a port in the url(https://github.com/kobitoko/CMPUT404-assignment-web-client)
		spltport = hostwp.split(':')		
		port = spltport[1]
		root = spltport[0]
	else:
		root = hostwp #there's no port in the url

	port = int(port)
	
	#get the stuff after the hostname, if there is anything
	pages = "/"
#how to start a python for loop at a certain spot
		#(http://stackoverflow.com/a/14053750)
#answered by Inbar Rose on Stack Overflow (http://stackoverflow.com/users/1561176/inbar-rose)
	for item in range(1, len(splitslash)):
		pages = pages + splitslash[item] + '/'
	pages = pages[:-1] # How to remove the last character from a string (http://stackoverflow.com/a/15478161) on Stack Overflow (http://stackoverflow.com/users/2110805/cyrille)

	header = "GET " + pages + " HTTP/1.1\r\nHost: " + root + "\r\n" + "Accept: */*\r\n\r\n"
	
	clnt = self.connect(root, port)
	clnt.sendall(header)
	response = self.recvall(clnt)

	print response
	
	code = self.get_code(response)
	body = self.get_body(response)
	
	code = int(code)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):

	pieces = url.split('http://')
	hostwpnpgs = pieces[1]
	splitslash = hostwpnpgs.split('/')
	hostwp = splitslash[0]
	#but if it has a port in it, get the port and shorten the url
	port = 80

	if(':' in hostwp):
		spltport = hostwp.split(':')		
		port = spltport[1]
		root = spltport[0]
	else:
		root = hostwp #there's no port in the url

	port = int(port)
#get the stuff after the hostname, if there is anything
	pages = "/"
	for item in range(1, len(splitslash)):
		pages = pages + splitslash[item] + '/'
	pages = pages[:-1] # How to remove the last character from a string (http://stackoverflow.com/a/15478161) on Stack Overflow (http://stackoverflow.com/users/2110805/cyrille)
	clnt = self.connect(root, port)
	poster = "POST " + pages + " HTTP/1.1\r\nHost: " + root + "\r\n"

	#referenced Ryan Satyabrata's repo to figure out how to handle args(https://github.com/kobitoko/CMPUT404-assignment-web-client)
	encargs = ""
	if(args != None):
		encargs = urllib.urlencode(args)
	#information on application/x-www-form-urlencoded (https://www.w3.org/TR/html401/interact/forms.html)
	ctype = "content-type: application/x-www-form-urlencoded\r\n" 
	clen = "content-length: " + str(len(encargs)) + "\r\n"
	hnbody = poster + clen + ctype + "\r\n" + encargs + "\r\n\r\n"
	
	clnt.sendall(hnbody)
	response = self.recvall(clnt)
	header = self.get_headers(response)
	
	print response

	code = self.get_code(response)
	body = self.get_body(response)
	code = int(code)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
