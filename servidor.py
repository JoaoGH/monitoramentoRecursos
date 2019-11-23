##tem um atributo apra setar o logging disabled como true
from http.server import BaseHTTPRequestHandler, HTTPServer
from pylive import live_plotter
import logging, json, os.path
import numpy as np

size = 10
vetX = np.linspace(0,1,size+1)[0:-1]
arr = []
for i in range(0, size):
    arr.append(0.00)
y1 = np.array(arr)
y2 = np.array(arr)
y3 = np.array(arr)
y4 = np.array(arr)
line1 = []
line2 = []
line3 = []
line4 = []

def atribuiGrafico(dados):
    cpu = np.float32(dados['cpu_usage'])
    memory = np.float32(dados['memory_used_percent'])
    up = np.float32(dados['network_up'])
    down = np.float32(dados['network_down'])
    
    global y1
    global y2
    global y3
    global y4
    global vetX
    global line1
    global line2
    global line3
    global line4

    y1[-1] = cpu
    y2[-1] = memory
    y3[-1] = up
    y4[-1] = down
    
    line1, line2, line3, line4 = live_plotter(vetX, y1, line1, "CPU Usage", y2, line2, "Memory Usage", y3, line3, "Network Up", y4, line4, "Network Down")
    y1 = np.append(y1[1:],0.0)
    y2 = np.append(y2[1:],0.0)
    y3 = np.append(y3[1:],0.0)
    y4 = np.append(y4[1:],0.0)

def criaCabecalho(dados):
    nomeMaquina = dados['hostname']
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

    arq.write("\n")
    arq.write("CPU Usage(%)\tMemory Usage(%)\t")
    for disco in dados['drives']:
        arq.write("Disco " + disco['name'] + "(%)\t")
    arq.write("Network Up(MB)\tNetwork Down(MB)\n")

    arq.close()

def salvaLog(dados):
    nomeMaquina = dados['hostname']
    if not(os.path.isfile(nomeMaquina+'.txt')):
        criaCabecalho(dados)
    
    arq = open(nomeMaquina+".txt", "a")
    novaLinha = ""
    novaLinha += str(dados['cpu_usage']) + "\t"
    novaLinha += str(dados['memory_used_percent']) + "\t"
    
    for disco in dados['drives']:
        novaLinha += str(disco['percent_used']) + "\t"
    
    novaLinha += str(dados['network_up']/1e6) + "\t"
    novaLinha += str(dados['network_down']/1e6) + "\t"
    
    novaLinha += "\n"
    arq.write(novaLinha)
    arq.close()

    print("Dados:", novaLinha)


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
        

        atribuiGrafico(dados)
        
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
