import serial.tools.list_ports

print('Search...')
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
    print('Find port '+ port.device)