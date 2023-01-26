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
        
        string_data = string_data.split("\n")
        first_line = string_data[0].split(" ")
        req_type = first_line[0]
        loc = first_line[1][1:]
        response = ""

        if req_type != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\n\nMethod Not Allowed"
        else:
            curr_dir_path = os.path.dirname(os.path.realpath(__file__))
            root = os.path.join(curr_dir_path, "www")
            path = os.path.join(root, loc)

            # add index.html to paths ending with "/"
            if os.path.isdir(path) and path.endswith("/"):
                path = os.path.join(path, "index.html")

            # to make sure the realpath of the file is inside the root path
            path = os.path.realpath(path)

            # handle invalid file paths
            if path.startswith(root) and not os.path.isdir(path):
                try:
                    with open(path) as f:
                        f_data = f.read()
                        
                        # set content-type
                        content_type = ""
                        _, file_extension = os.path.splitext(path)

                        if file_extension == ".html":
                            content_type = "Content-Type: text/html"
                        elif file_extension == ".css":
                            content_type = "Content-Type: text/css"
                        
                        response = "HTTP/1.1 200 OK\r\n" + content_type + "\n\n" + f_data
                except FileNotFoundError:
                    response = "HTTP/1.1 404 NOT FOUND\n\n404 File Not Found"
            # if realpath of the file is not inside the root path
            elif not path.startswith(root):
                response = "HTTP/1.1 404 NOT FOUND\n\n404 File Not Found"
            # if directory exists and does not have a "/" at the end
            elif os.path.isdir(path):
                location = f"/{loc}/"
                response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {location}\n\n301 Moved Permanently"

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
