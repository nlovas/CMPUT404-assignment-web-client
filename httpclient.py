#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

	def get_host_port(self,url):
		#can sometimes be given 127.0.0.1:8080 ! so break it down and check
		#referenced Ryan Satyabrata's repo to figure out how to check(https://github.com/kobitoko/CMPUT404-assignment-web-client)
		ipPort = url.split(':')
		print ipPort[0:]
		if(len(ipPort) > 1):
			return ipPort[1]
		else:
			return 80	
			

	def getRoot(self, url):
	#check if its an ip or a regular url and return the root, but if it's an ip it will have the port at the end
	#referenced Ryan Satyabrata's repo to figure out how to check(https://github.com/kobitoko/CMPUT404-assignment-web-client)
		pieces = url.split('/')
		#print pieces[0:]
		if(pieces[0] == 'http:' or pieces[0] == 'https:'):
			return pieces[2] 
		else:
			return pieces[0]

	def checkIfIP(self, mayberoot):
		root = mayberoot.split(':')
		if(len(root)>1):
			return root[0]
		else:
			return mayberoot
		
	def afterRoot(self, url, root):
	#get the pages after the root url, if there are any
	#in this case the port # is included for ips, we're looking for whats after it
		pages = url.split('/')
		i = 0
		print "url: " + url + " root: " + root
		print pages[0:]
		#get the parts only after the one that == the root
		for index in range(len(pages)):
			if(pages[index] == root):
				i = index
				break
		
		#how to start a python for loop at a certain spot
		#(http://stackoverflow.com/a/14053750)
		#answered by Inbar Rose on Stack Overflow (http://stackoverflow.com/users/1561176/inbar-rose)
		after = ""
		for index in range(i, len(pages)):
			print index
			if(pages[index] != "" and pages[index]!=root):
				after = after + "/" + pages[index]
		if (after == ""):
			after = '/'			
		return after


	def connect(self, host, port):
		#from the example in https://docs.python.org/2/library/socket.html#socket.socket.connect
		#print "host:" + host + " port: " + str(port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
		return s

	def get_code(self, data):
		return None

	def get_headers(self,data):
		return None

	def get_body(self, data):
		return None

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
		
		rootURL = self.getRoot(url)
		pgs = self.afterRoot(url, rootURL)
		hostPort = self.get_host_port(rootURL)		
		rootURL = self.checkIfIP(rootURL) #get rid of a trailing port number if it's an ip		
		s = self.connect(rootURL,int(hostPort))
		request = "GET" + pgs + "HTTP/1.1\r\n\r\n"
		s.sendall(request)

		response = self.recvall(s)

		code = 500
		body = ""
		return HTTPResponse(code, body)

	def POST(self, url, args=None):
		code = 500
		body = "" #urllib.encode(dictionary) #TODO: put a dcitonary variable here...
		return HTTPResponse(code, body)

	def command(self, url, command="GET", args=None):
		if (command == "POST"):
			print "post!"
			return self.POST( url, args )
		else:
			print "get!"
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
