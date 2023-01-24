#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        string_data = self.data.decode("utf-8")
        # print(string_data)
        
        string_data = string_data.split("\n")
        filename = string_data[0].split(" ")[1]
        # print("filename: ", filename)

        response = ""

        # homepage index.html
        if filename == "/":
            filename = "/index.html"

        path = "www" + filename
        is_dir = False
        content_type = ""

        # set content-type
        filename, file_extension = os.path.splitext(path)
        
        if file_extension == ".html":
            content_type = "Content-Type: text/html"
        elif file_extension == ".css":
            content_type = "Content-Type: text/css"

        if os.path.isdir("path"):
            is_dir = True

        try:
            with open(path) as f:
                f_data = f.read()
                response = "HTTP/1.1 200 OK\r\n" + content_type + "\n\n" + f_data
        except FileNotFoundError:
            response = "HTTP/1.1 404 NOT FOUND\n\nFile Not Found"

        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray(response,'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
