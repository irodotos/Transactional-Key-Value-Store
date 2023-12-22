from http.server import BaseHTTPRequestHandler, HTTPServer

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8000


class handler_class(BaseHTTPRequestHandler):

    def apply_res(self):
        self.send_response(200)
        self.end_headers()
        
        if "Content-Length" in self.headers:
            body = self.rfile.read(int(self.headers['Content-Length'])).decode("UTF-8")
        else:
            body = ""
        self.wfile.write(bytes("{} request from {} \n Headers:\n {} \n Path: {} \n Body: {} \n".format(self.command , self.client_address , self.headers , self.path , str(body)) , "UTF-8"))

    def do_GET(self):
        self.apply_res()
        
    def do_POST(self):
        self.apply_res()
    
    def do_PUT(self):
        self.apply_res()
    
    def do_DELETE(self):
        self.apply_res()

    def do_HEAD(self):
        self.apply_res()

    def do_OPTIONS(self):
        self.apply_res()
    
    def do_PATCH(self):
        self.apply_res()
    

def run():
    server_address = (SERVER_IP , SERVER_PORT)
    httpd = HTTPServer(server_address, handler_class)
    print("server at {} and port: {}".format(SERVER_IP , SERVER_PORT))
    try:
        httpd.serve_forever()
    except: KeyboardInterrupt
    httpd.server_close()

if __name__ == "__main__":
    run()