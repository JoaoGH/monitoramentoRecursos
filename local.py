import socket, time, json, datetime, platform, psutil, requests, pprint, uuid, platform


servidorDestino = input("Digite o servidor de destino (Nome ou IP e porta): ")


def main():
    # Hostname Info
    hostname = socket.gethostname()

    # sytem info
    system = {
        "name" : platform.system(),
        "version" : platform.release()
    }

    # CPU Info
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory Info
    memory_stats = psutil.virtual_memory()
    memory_total = memory_stats.total
    memory_used = memory_stats.used
    memory_used_percent = memory_stats.percent


    # Disk Info
    disk_info = psutil.disk_partitions()
    disks = []
    for x in disk_info:
        # Try fixes issues with connected 'disk' such as CD-ROMS, Phones, etc.
        try:
            disk = {
                "name" : x.device, 
                "mount_point" : x.mountpoint, 
                "type" : x.fstype, 
                "total_size" : psutil.disk_usage(x.mountpoint).total, 
                "used_size" : psutil.disk_usage(x.mountpoint).used, 
                "percent_used" : psutil.disk_usage(x.mountpoint).percent
            }

            disks.append(disk)

        except:
            print("")

    # Bandwidth Info 
    network_stats = get_bandwidth()

    # Network Info
    nics = []
    ##print("NICs:")
    for name, snic_array in psutil.net_if_addrs().items():
        # Create NIC object
        nic = {
            "name": name,
            "mac": "",
            "address": "",
            "address6": "",
            "netmask": ""
        }
        # Get NiC values
        for snic in snic_array:
            if snic.family == -1:
                nic["mac"] = snic.address
            elif snic.family == 2:
                nic["address"] = snic.address
                nic["netmask"] = snic.netmask
            elif snic.family == 23:
                nic["address6"] = snic.address
        nics.append(nic)
	
    # Set Machine Info
    machine = {
    	"hostname" : hostname,
        "system" : system,
    	"cpu_count" : cpu_count,
    	"cpu_usage" : cpu_usage,
    	"memory_total" : memory_total,
    	"memory_used" : memory_used,
    	"memory_used_percent" : memory_used_percent,
    	"drives" : disks,
    	"network_up" : network_stats["traffic_out"],
    	"network_down" : network_stats["traffic_in"],
        "network_cards": nics
    }

    data = json.dumps(machine)

    send_data(data)

def get_bandwidth():
    # Get net in/out
    net1_out = psutil.net_io_counters().bytes_sent
    net1_in = psutil.net_io_counters().bytes_recv

    time.sleep(1)

    # Get new net in/out
    net2_out = psutil.net_io_counters().bytes_sent
    net2_in = psutil.net_io_counters().bytes_recv

    # Compare and get current speed
    if net1_in > net2_in:
        current_in = 0
    else:
        current_in = net2_in - net1_in
    
    if net1_out > net2_out:
        current_out = 0
    else:
        current_out = net2_out - net1_out
    
    network = {"traffic_in" : current_in, "traffic_out" : current_out}
    return network

def send_data(data):
    # Se der erro 30 vezes consecutivas encerrra
    for attempt in range(30):
        try:
            # endpoint = monitoring server
            endpoint = servidorDestino
            response = requests.post(url = endpoint, data = data)
            if(response.status_code == 200):
                print("Success")
            else:
                print("Error code",response.status_code)
            break
        except requests.exceptions.RequestException as e:
            print("\nPOST Error:\n",e)
            time.sleep(1)
    else:
        # If no connection established for half an hour, kill script
        exit(0)


while True:
	main()
	time.sleep(1)
