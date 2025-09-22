import psutil
import time

# Definimos los estados de los procesos
estados_simulados = {
    'running': 'Ejecutándose',
    'sleeping': 'Listo (en espera)',
    'waiting': 'Bloqueado (esperando I/O)',
    'zombie': 'Zombie (terminado)'
}

print("Monitoreo de Procesos (Presione Ctrl+C para salir)\n")

try:
    while True:
        # Limpiamos la pantalla
        print("\033[H\033[J")

        # Obtenemos todos los procesos
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                # Obtenemos la información de cada proceso
                pid = proc.info['pid']
                nombre = proc.info['name']
                
                # ⚠️ MANEJO DEL ERROR DE CPU AQUÍ ⚠️
                uso_cpu_raw = proc.info['cpu_percent']
                if uso_cpu_raw is not None:
                    uso_cpu = uso_cpu_raw
                else:
                    uso_cpu = 0.0  # Asignamos 0.0 si la información de CPU no está disponible

                # Manejo del error de Memoria (como en la solución anterior)
                mem_info = proc.info['memory_info']
                if mem_info is not None:
                    uso_memoria = mem_info.rss / (1024 * 1024)
                else:
                    uso_memoria = 0.0

                # Obtenemos el estado real y lo mapeamos
                estado_real = proc.status()
                estado_simulado = estados_simulados.get(estado_real, estado_real)

                # Mostramos la información
                print(f"PID: {pid:<5} | Proceso: {nombre:<25} | CPU: {uso_cpu:<5.2f}% | Memoria: {uso_memoria:.2f} MB | Estado: {estado_simulado}")

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Esperamos antes de la próxima actualización
        time.sleep(2)

except KeyboardInterrupt:
    print("\nMonitoreo detenido.")
    