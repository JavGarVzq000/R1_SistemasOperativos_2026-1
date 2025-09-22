import psutil

# Uso de CPU
print("Uso de CPU (%):", psutil.cpu_percent(interval=1))

# Uso de Memoria
mem = psutil.virtual_memory()
print("Memoria total:", mem.total)
print("Memoria disponible:", mem.available)
print("Uso de memoria (%):", mem.percent)

# Información del disco
disk = psutil.disk_usage('/')
print("Uso del disco (%):", disk.percent)

# Información de red
net = psutil.net_io_counters()
print("Bytes enviados:", net.bytes_sent)
print("Bytes recibidos:", net.bytes_recv)

