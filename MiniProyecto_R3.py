# =========================================================================
# Monitoreo de Procesos del SO (Usando Python y psutil)
# Modificación: Si uso_cpu es 0.00%, el estado debe ser 'Listo (en espera)'.


# =========================================================================

# Solicitamos las librerías que necesitamos
import psutil  # Librería fundamental para interactuar, monitorear y gestionar los procesos activos del sistema.
import time    # Librería para introducir pausas en el script (simular el refresco de monitoreo).
import tkinter as tk  #Interfaz gráfica
from tkinter import ttk # Tabla 

# INTERFAZ: Variables globales para la GUI.
app_window = None
tree_view = None
status_label = None #Hora de actualización
monitoreo_activo = True # Controla si el ciclo 'after' debe continuar.
boton_detener = None   # Almacena el widget Button de detener/iniciar.
etiqueta_cpu = None     # Etiqueta para el texto de uso de CPU.
barra_cpu = None       # Barra de progreso de CPU.
etiqueta_mem = None     # Etiqueta para el texto de uso de Memoria.
barra_mem = None       # Barra de progreso de Memoria.

# =========================================================================


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

        
         # INTERFAZ: Devolvemos los datos de estados simulados para su inserción en la tabla.
        return (
            str(pid), 
            nombre, 
            f"{uso_cpu:.2f}%", 
            f"{uso_memoria:.2f} MB", 
            estado_simulado
        )

       
        # Mostrar la información formateada --> se modificó para utilizar la librería tkinter #de la interfaz gráfica
        # print(f"PID: {pid:<5} | Proceso: {nombre:<25} | CPU: {uso_cpu:<5.2f}% | Memoria: {uso_memoria:.2f} MB | Estado: {estado_simulado}")

    # Manejo de excepciones
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # Captura errores si un proceso termina o si Python no tiene permisos para leerlo.
        # En estos casos, simplemente omitimos el proceso y continuamos con el siguiente.
        pass
    except Exception:
        # Captura cualquier otro error imprevisto para evitar que el script se detenga.
        pass

# INTERFAZ: Función para manejar el estado del botón Detener/Iniciar.
def alternar_monitoreo():
    global monitoreo_activo, boton_detener
    monitoreo_activo = not monitoreo_activo
    
    if monitoreo_activo:
        boton_detener.config(text="Detener Monitoreo")
        # INTERFAZ: Si se reanuda, llamamos inmediatamente a actualizar_tabla para reiniciar el ciclo 'after'.
        actualizar_tabla() 
    else:
        boton_detener.config(text="Iniciar Monitoreo")
    
    # INTERFAZ: Actualizar la etiqueta de estado general para reflejar la pausa.
    global status_label
    if status_label:
        status_label.config(text=f"Monitoreo: {'ACTIVO' if monitoreo_activo else 'DETENIDO'} | Intervalo: 2 segundos")





def actualizar_tabla(manual_update=False):
    """
    Función: actualizar_tabla.Llama a monitorear_procesos y actualiza el Treeview y la hora.
    Se realiza la actualización automática.
    """
    global tree_view, app_window, status_label, monitoreo_activo
    global etiqueta_cpu, barra_cpu, etiqueta_mem, barra_mem

    # Si el monitoreo está detenido, salimos de la función sin actualizar ni programar el siguiente ciclo.
    if not monitoreo_activo:
        return 
    
    # 1. Limpiar la tabla de procesos anteriores
    for i in tree_view.get_children():
        tree_view.delete(i)

    # 2. Iterar sobre todos los procesos activos y llenarlos
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        datos_proceso = obtener_y_mostrar_proceso(proc)        
        if datos_proceso:
            # 3. Insertar los datos del proceso en la tabla
            tree_view.insert('', tk.END, values=datos_proceso)

    # 3. Barras de progreso y etiquetas de CPU y Memoria
    # Uso de CPU (global)
    cpu_percent = psutil.cpu_percent(interval=None)
    etiqueta_cpu.config(text=f"Uso de CPU: {cpu_percent:.1f}%")
    barra_cpu.config(value=cpu_percent)

    # Uso de Memoria (global)
    virtual_mem = psutil.virtual_memory()
    mem_percent = virtual_mem.percent
    mem_used_gb = virtual_mem.used / (1024 ** 3)
    mem_total_gb = virtual_mem.total / (1024 ** 3)
    
    etiqueta_mem.config(text=f"Memoria Usada: {mem_percent:.1f}% ({mem_used_gb:.2f} GB de {mem_total_gb:.2f} GB)")
    barra_mem.config(value=mem_percent)

            
    #Actualizar la hora de la última actualización
    current_time = time.strftime("%H:%M:%S")
    if status_label:
        status_label.config(text=f"Monitoreo: ACTIVO | Última actualización: {current_time} | Intervalo: 2 segundos")

    # 4. Programar la siguiente actualización automática
    # actualización continua de 2 segundos.
    app_window.after(2000, actualizar_tabla)


def monitorear_procesos():
    """
    Función: monitorear_procesos (Función principal)
    Responsabilidad: Contiene el bucle principal, gestiona la limpieza de pantalla 
    """
    # print("Monitoreo de Procesos (Presione Ctrl+C para salir)\n") -- se modificó para utilizar la librería tkinter de la interfaz gráfica
    
    global app_window, tree_view, status_label, boton_detener
    global etiqueta_cpu, barra_cpu, etiqueta_mem, barra_mem
    # INTERFAZ: Configuración de la ventana principal de la GUI

    # Ventana Principal
    app_window = tk.Tk()
    app_window.title("Monitor de Procesos del SO")
    app_window.geometry("1100x600") 
    top_frame = tk.Frame(app_window)
    top_frame.pack(pady=10, fill='x')

    # header_frame = tk.Frame(app_window)
    # header_frame.pack(pady=15, fill='x')  # Espaciado superior y relleno horizontal IGUAL SE BORRA

     # INTERFAZ: Título 
    title_label = tk.Label(top_frame, text="Monitor de Procesos del Sistema Operativo", font=("Arial", 16, "bold"))
    title_label.pack(side=tk.TOP) 

    # INTERFAZ: Frame para el estado (Etiqueta y Botón)
    status_control_frame = tk.Frame(top_frame)
    status_control_frame.pack(pady=(5, 10), fill='x', padx=10)

    # INTERFAZ: Hora de Actualización
    status_label = tk.Label(status_control_frame, text="Monitoreo: ACTIVO | Última actualización: --:--:-- | Intervalo: 2 segundos", font=("Arial", 10))
    status_label.pack(side=tk.LEFT)


    # INTERFAZ: Botón de Detener/Iniciar Monitoreo. Llama a 'alternar_monitoreo'.
    boton_detener = ttk.Button(status_control_frame, text="Detener Monitoreo", command=alternar_monitoreo)
    boton_detener.pack(side=tk.RIGHT)


    # INTERFAZ: Contenedor de las 2 columnas (Barras y Tabla)
    main_content_frame = tk.Frame(app_window)
    main_content_frame.pack(expand=True, fill='both', padx=10, pady=(0, 10))

    # --- Columna 1: Barras de Progreso (CPU y Memoria) ---
    bars_frame = tk.Frame(main_content_frame)
    bars_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

    # CPU. Etiqueta y Barra
    etiqueta_cpu = ttk.Label(bars_frame, text="Uso de CPU: --.-%", anchor='w')
    etiqueta_cpu.pack(pady=(5, 2), padx=10, fill='x')
    barra_cpu = ttk.Progressbar(bars_frame, orient='vertical', length=100, mode='determinate') 
    barra_cpu.pack(pady=5, padx=10, fill='x')

    # Memoria. Etiqueta y Barra
    etiqueta_mem = ttk.Label(bars_frame, text="Memoria Usada: --.-%", anchor='w')
    etiqueta_mem.pack(pady=(5, 2), padx=10, fill='x')
    barra_mem = ttk.Progressbar(bars_frame, orient='vertical', length=100, mode='determinate') 
    barra_mem.pack(pady=5, padx=10, fill='x')

    # Columna 2: Tabla de Procesos (Treeview) 
    table_frame = tk.Frame(main_content_frame)
    table_frame.pack(side=tk.RIGHT, expand=True, fill='both')

    # 2. Definición de Columnas para el Treeview (Tabla)
    columnas = ('PID', 'Proceso', 'CPU', 'Memoria', 'Estado')
    tree_view = ttk.Treeview(table_frame, columns=columnas, show='headings')

    #  # INTERFAZ: Tabla
    # table_frame = tk.Frame(app_window)
    # table_frame.pack(expand=True, fill='both', padx=10, pady=(0, 10))
    # columnas = ('PID', 'Proceso', 'CPU', 'Memoria', 'Estado')
    # tree_view = ttk.Treeview(table_frame, columns=columnas, show='headings')

    # # INTERFAZ: Configuración del encabezado y ancho de las columnas
    # tree_view.heading('PID', text='PID', anchor=tk.W)
    # tree_view.heading('Proceso', text='Proceso', anchor=tk.W)
    # tree_view.heading('CPU', text='CPU', anchor=tk.W)
    # tree_view.heading('Memoria', text='Memoria', anchor=tk.W)
    # tree_view.heading('Estado', text='Estado', anchor=tk.W)
    
    # tree_view.column('PID', width=80, stretch=tk.NO)
    # tree_view.column('Proceso', width=350, stretch=tk.YES)
    # tree_view.column('CPU', width=80, stretch=tk.NO)
    # tree_view.column('Memoria', width=100, stretch=tk.NO)
    # tree_view.column('Estado', width=150, stretch=tk.NO)

     # 3. Configuración del encabezado y ancho de las columnas
    tree_view.heading('PID', text='PID', anchor=tk.W)
    tree_view.heading('Proceso', text='Proceso', anchor=tk.W)
    tree_view.heading('CPU', text='CPU', anchor=tk.W)
    tree_view.heading('Memoria', text='Memoria', anchor=tk.W)
    tree_view.heading('Estado', text='Estado', anchor=tk.W)
    
    tree_view.column('PID', width=80, stretch=tk.NO)
    tree_view.column('Proceso', width=350, stretch=tk.YES)
    tree_view.column('CPU', width=80, stretch=tk.NO)
    tree_view.column('Memoria', width=100, stretch=tk.NO)
    tree_view.column('Estado', width=150, stretch=tk.NO)

     # INTERFAZ: Agregar Scrollbar 
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree_view.yview)
    tree_view.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_view.pack(expand=True, fill='both')
    
    # Iniciar el ciclo de actualización
    actualizar_tabla()

     #Iniciar el bucle principal de Tkinter
    app_window.mainloop()


    # Se modificó para utilizar la librería tkinter de la interfaz gráfica
    # try:
    #     # Bucle infinito para el monitoreo continuo
    #     while True:
    #         # Limpiamos la pantalla
    #         print("\033[H\033[J")

    #         # Iteramos sobre todos los procesos activos
    #         # Pasamos una lista de atributos para optimizar la llamada y obtener solo lo necesario.
    #         for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
    #             # Llamamos a la función de detalle para procesar y mostrar cada proceso.
    #             obtener_y_mostrar_proceso(proc)

    #         # Esperamos 2 segundos
    #         time.sleep(2)

    # except KeyboardInterrupt:
    #     # Manejo de la interrupción del usuario (Ctrl+C) para una salida limpia.
    #     print("\nMonitoreo detenido.")


# Punto de entrada estándar de Python
if __name__ == "__main__":
    
    # Ejecuta la función principal del monitoreo.
    monitorear_procesos()