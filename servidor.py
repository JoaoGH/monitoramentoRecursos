##tem um atributo apra setar o logging disabled como true
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, json, os.path


def salvaLog(dados):
    nomeMaquina = dados['hostname']
    if(os.path.isfile(nomeMaquina+'.txt')):
        arq = open(nomeMaquina+".txt", "a")
        arq.write("CPU Usage: " + str(dados['cpu_usage']) + "%\n")
        arq.write("Memory Usage: " + str(dados['memory_used_percent']) + "%\n")
        
        arq.write("Drivers:\n")
        for disco in dados['drives']:
            arq.write("\tName: " + disco['name'] + "\n")
            arq.write("\tPercent Usage: " + str(disco['percent_used']) + "%\n")
        
        arq.write("Network Up: " + str(dados['network_up']) + "\n")
        arq.write("Network Down: " + str(dados['network_down']) + "\n")

    else:
        arq = open(nomeMaquina+".txt", "w")
        arq.write("Hostname: " + dados['hostname'] + "\n")
        arq.write("System: " + dados['system']['name'] + " " + dados['system']['version'] + "\n")
        arq.write("CPU Count: " + str(dados['cpu_count']) + "\n")
        arq.write("Memory Total: " + str(dados['memory_total'] / 1e6) + " MB\n")
        
        arq.write("Drivers:\n")
        for disco in dados['drives']:
            arq.write("\tName: " + disco['name'] + "\n")
            arq.write("\tTotalSize: " + str(disco['total_size'] / 1e9) + " GB\n")
        
        arq.write("Network Cards:\n")
        for interfacesRede in dados['network_cards']:
            arq.write("\tName: " + interfacesRede['name'] + "\n")
            arq.write("\tMAC: " + interfacesRede['mac'] + "\n")
            arq.write("\tAddress: " + interfacesRede['address'] + "\n")
    
    #para inserir quebra de linha
    arq.write("\n")

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        dados = json.loads(post_data.decode("utf-8"))

        salvaLog(dados)
        
        self._set_response()


def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
