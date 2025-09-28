# =========================================================================
# Monitoreo de Procesos del SO (Usando Python y psutil)
# Modificación: Si uso_cpu es 0.00%, el estado debe ser 'Listo (en espera)'.

#cambios 
# =========================================================================

# Solicitamos las librerías que necesitamos
import psutil  # Librería fundamental para interactuar, monitorear y gestionar los procesos activos del sistema.
import time    # Librería para introducir pausas en el script (simular el refresco de monitoreo).

# 1. Definimos el mapeo de estados como una variable global (o constante)
# Traduce los estados internos de psutil (que reflejan el SO) a un formato legible
ESTADOS_SIMULADOS = {
    'running': 'Ejecutándose',              # Proceso usando la CPU activamente.
    'sleeping': 'Listo (esn espera)',        # Estado por defecto cuando el SO lo reporta como "durmiendo".
    'waiting': 'Bloqueado (esperando I/O)', # Proceso esperando una operación de Entrada/Salida.
    'zombie': 'Zombie (terminado)'          # Proceso terminado, pero que aún tiene una entrada en la tabla de procesos.
    # Nota: El estado 'Listo (en espera)' también se aplicará por lógica de CPU 0.00%
}


def obtener_y_mostrar_proceso(proc):
    """
    Función: obtener_y_mostrar_proceso
    Responsabilidad: Extrae la información detallada de un proceso individual y aplica la nueva lógica de estado.
    """
    try:
        # Intenta obtener la información del proceso. Esto puede fallar si el proceso termina mientras se lee.
        
        # Extracción de campos obligatorios
        pid = proc.info['pid']
        nombre = proc.info['name']
        
        # MANEJO DE USO DE CPU
        uso_cpu_raw = proc.info['cpu_percent']
        uso_cpu = uso_cpu_raw if uso_cpu_raw is not None else 0.0

        # MANEJO DE USO DE MEMORIA (en MB)
        mem_info = proc.info['memory_info']
        if mem_info is not None:
            # Convierte el Resident Set Size (RSS, memoria física usada) de bytes a Megabytes.
            uso_memoria = mem_info.rss / (1024 * 1024)
        else:
            uso_memoria = 0.0
            
        # ===============================================================
        # 4. LÓGICA DE SIMULACIÓN Y ASIGNACIÓN DE ESTADO MODIFICADA
        # ===============================================================
        
        estado_real = proc.status()
        
        # Primero, verifica si el proceso ha terminado. Si es zombie, no hay más lógica.
        if estado_real == 'zombie':
            estado_simulado = ESTADOS_SIMULADOS['zombie']
        
        # Segundo, aplica la regla de correlación: Si el uso de CPU es cero,
        # implica que el proceso está esperando y se encuentra en el estado 'Listo'
        elif uso_cpu == 0.0:
            estado_simulado = 'Listo (En espera)'
        
        # Tercero, si no es Zombie y sí está usando CPU, usa el mapeo original.
        else:
            # Mapea el estado real del SO (Ejecutándose, Bloqueado, etc.)
            estado_simulado = ESTADOS_SIMULADOS.get(estado_real, estado_real)

        # Mostrar la información formateada
        print(f"PID: {pid:<5} | Proceso: {nombre:<25} | CPU: {uso_cpu:<5.2f}% | Memoria: {uso_memoria:.2f} MB | Estado: {estado_simulado}")

    # Manejo de excepciones
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # Captura errores si un proceso termina o si Python no tiene permisos para leerlo.
        # En estos casos, simplemente omitimos el proceso y continuamos con el siguiente.
        pass
    except Exception:
        # Captura cualquier otro error imprevisto para evitar que el script se detenga.
        pass


def monitorear_procesos():
    """
    Función: monitorear_procesos (Función principal)
    Responsabilidad: Contiene el bucle principal, gestiona la limpieza de pantalla y la pausa.
    """
    print("Monitoreo de Procesos (Presione Ctrl+C para salir)\n")
    
    try:
        # Bucle infinito para el monitoreo continuo
        while True:
            # Limpiamos la pantalla
            print("\033[H\033[J")

            # Iteramos sobre todos los procesos activos
            # Pasamos una lista de atributos para optimizar la llamada y obtener solo lo necesario.
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                # Llamamos a la función de detalle para procesar y mostrar cada proceso.
                obtener_y_mostrar_proceso(proc)

            # Esperamos 2 segundos
            time.sleep(2)

    except KeyboardInterrupt:
        # Manejo de la interrupción del usuario (Ctrl+C) para una salida limpia.
        print("\nMonitoreo detenido.")


# Punto de entrada estándar de Python
if __name__ == "__main__":
    # Ejecuta la función principal del monitoreo.
    monitorear_procesos()