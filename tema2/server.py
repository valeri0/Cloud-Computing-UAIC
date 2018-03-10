from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import re
import json
from ShoeRepository import ShoeRepository
from Shoe import Shoe


class CustomRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.repository = ShoeRepository()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):

        response_message = None

        # tratam ruta /shoes
        if self.path == "/shoes":
            response_message = self.repository.get_all_shoes()
            self.send_response(200)

        # tratam ruta /shoes/id
        if re.match("/shoes/[A-Z0-9]{6}", self.path):
            _id = self.path[7:]

            response_message = self.repository.get_shoe_by_id(_id)
            self.send_response(200)

            if response_message is None:
                response_message = json.dumps({'response': 'NO SHOE WITH ID ' + _id})
                self.send_response(404)

            if len(_id) > 6:
                response_message = json.dumps({'response': 'INVALID_ROUTE'})
                self.send_response(404)

        if response_message is None:
            response_message = json.dumps({'response': 'INVALID_ROUTE'})
            self.send_response(404)

        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))

    def do_POST(self):

        if self.path != "/shoes":
            self.send_response(404)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': 'INVALID_ROUTE'}).encode('utf-8'))


        else:

            content_len = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_len)

            data = json.loads(post_body)

            response_message = "["

            for new_shoe in data:
                _new_shoe_created = self.repository.add_shoe_to_list(
                    Shoe(new_shoe['brand'], new_shoe['model'], new_shoe['size']))
                response_message += _new_shoe_created + ","
            response_message = response_message[:-1] + "]"

            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(response_message.encode('utf-8'))

    def do_PUT(self):

        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        if self.path == "/shoes":

            response_message = "["

            for shoe in data:
                response_message += self.repository.update_shoe_by_id(shoe['id'], brand=shoe['brand'],
                                                                      model=shoe['model'], size=shoe['size']) + ","

            response_message = response_message[:-1] + "]"

            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(response_message.encode('utf-8'))



        elif re.match("/shoes/[A-Z0-9]{6}", self.path):
            _id = self.path[7:]

            if len(_id) > 6:
                self.send_response(404)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps({'response': 'INVALID_ROUTE'}).encode('utf-8'))

            else:

                if self.repository.get_shoe_by_id(_id) is None:
                    response_message = self.repository.add_shoe_to_list(
                        Shoe(data['brand'], data['model'], data['size']))

                else:
                    response_message = self.repository.update_shoe_by_id(_id, model=data['model'], brand=data['brand'],
                                                                         size=data['size'])

                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(response_message.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': 'INVALID_ROUTE'}).encode('utf-8'))

    def do_DELETE(self):
        if self.path == "/shoes":

            self.repository.delete_all_shoes()

            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': 'DELETED_ALL_THE_SHOES'}).encode('utf-8'))



        elif re.match("/shoes/[A-Z0-9]{6}", self.path):
            _id = self.path[7:]

            if len(_id) > 6:
                self.send_response(404)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps({'response': 'INVALID_ROUTE'}).encode('utf-8'))

            else:

                response_message = json.dumps({'response':'SHOE_WITH_ID_'+_id+'_DOES_NOT_EXIST'})
                self.send_response(404)

                if self.repository.delete_shoe_by_id(_id) is not None:
                    self.send_response(200)
                    response_message = json.dumps({'response':'DELETED_SHOE_WITH_ID_'+_id})

                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(response_message.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': 'INVALID_ROUTE'}).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    my_server = server_class(server_address, handler_class)

    my_server.serve_forever()


run()
