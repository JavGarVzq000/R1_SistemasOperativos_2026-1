# =========================================================================
# Monitoreo de Procesos del SO (Usando Python y psutil)
# Si uso_cpu es 0.00%, el estado debe ser 'Listo (en espera)'.
# =========================================================================

# Solicitamos las librerías que necesitamos
import psutil  # Librería para interactuar, monitorear y gestionar los procesos 
import time    
import tkinter as tk  # Librería principal para la interfaz gráfica.
from tkinter import ttk # Usada para la tabla (Treeview) y Progressbar.

# Variables globales para la GUI/Interfaz gráfica
app_window = None # Ventana principal de la aplicación.
tree_view = None    # Tabla para mostrar los procesos.
status_label = None  # Etiqueta para mostrar la última actualización.
etiqueta_cpu = None      # Etiqueta para el texto de uso de CPU.
barra_cpu = None        # Barra de progreso de CPU.
etiqueta_mem = None      # Etiqueta para el texto de uso de Memoria.
barra_mem = None        # Barra de progreso de Memoria.




#Definimos el mapeo de estados como una variable global (o constante) para traducir los estados internod de psutil (que reflejan el SO) a un formato legible.

ESTADOS_SIMULADOS = {
    'running': 'Ejecutándose',              # Proceso usando la CPU activamente.
    'sleeping': 'Listo (en espera)',       # Estado por defecto cuando el SO lo reporta como "durmiendo".
    'waiting': 'Bloqueado (esperando I/O)', # Proceso esperando una operación de Entrada/Salida.
    'zombie': 'Zombie (terminado)'          # Proceso terminado, pero que aún tiene una entrada en la tabla de procesos.
    # Nota: El estado 'Listo (en espera)' también se aplicará por lógica de CPU 0.00%
}
    

# =========================================================================
# Funcionalidad del Monitor de procesos
# =========================================================================

def obtener_y_mostrar_proceso(proc):
    # Esta función extrae los datos de un proceso individual, realiza conversiones (bytes a MB)
    # y aplica la lógica de simulación de estado para devolver una tupla lista para la GUI.
    
    try:
        # Extracción de campos obligatorios. pid es el ID del proceso, name es el nombre del proceso.
        pid = proc.info['pid']
        nombre = proc.info['name']
        
        # MANEJO DE USO DE CPU
        uso_cpu_raw = proc.info['cpu_percent']
        uso_cpu = uso_cpu_raw if uso_cpu_raw is not None else 0.0

        # MANEJO DE USO DE MEMORIA (en MB)
        mem_info = proc.info['memory_info']
        if mem_info is not None:
            uso_memoria = mem_info.rss / (1024 * 1024)
        # Convertir bytes a MB debido a que rss está en bytes y se requiere convertir a MB. Resident Set Size (RSS) es la cantidad de memoria física (RAM) que un proceso está usando.
       
        else:
            uso_memoria = 0.0
            
        # LÓGICA DE ESTADO
        estado_real = proc.status()
        
        if estado_real == 'zombie':
            estado_simulado = ESTADOS_SIMULADOS['zombie']
        elif uso_cpu == 0.0:
            estado_simulado = 'Listo (En espera)'
        else:
            estado_simulado = ESTADOS_SIMULADOS.get(estado_real, estado_real)

        
        # INTERFAZ: se devuelven los datos para la inserción en la tabla.
        return (
            str(pid), 
            nombre, 
            f"{uso_cpu:.2f}%", 
            f"{uso_memoria:.2f} MB", 
            estado_simulado
        )

        
    # Manejo de excepciones
    except (psutil.NoSuchProcess, psutil.AccessDenied, Exception):
        return None # Devuelve None si hay error


def actualizar_tabla():
    # Función principal que actualiza la tabla de procesos y las barras de progreso de acuerdo con la información de la función anterior obtener_y_mostrar_proceso. Actualiza el Treeview, las barras y la hora.
    

    global tree_view, app_window, status_label 
    global etiqueta_cpu, barra_cpu, etiqueta_mem, barra_mem

    
    #Limpiar la tabla de procesos anteriores
    for i in tree_view.get_children():
        tree_view.delete(i)

   
    ## LÓGICA DE PROCESOS: Inicia la iteración sobre todos los procesos activos del sistema. proc representa cada proceso individual y se itera en la función psutil.process_iter.
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        datos_proceso = obtener_y_mostrar_proceso(proc)       
        if datos_proceso:
            # Insertar los datos del proceso en la tabla
            tree_view.insert('', tk.END, values=datos_proceso)

    # Barras de progreso y etiquetas de CPU y Memoria
    # Uso de CPU (global)
    cpu_percent = psutil.cpu_percent(interval=None)
    etiqueta_cpu.config(text=f"Uso de CPU: {cpu_percent:.1f}%")
    barra_cpu.config(value=cpu_percent)

    # Uso de Memoria (global). Obtiene el objeto de información de memoria virtual
    virtual_mem = psutil.virtual_memory()
    mem_percent = virtual_mem.percent
    #Convierte los valores de bytes a Gigabytes (GB) para la etiqueta.
    mem_used_gb = virtual_mem.used / (1024 ** 3)
    mem_total_gb = virtual_mem.total / (1024 ** 3)
    
    # Actualizar la etiqueta y barra de memoria
    etiqueta_mem.config(text=f"Uso de Memoria: {mem_percent:.1f}% ({mem_used_gb:.2f} GB de {mem_total_gb:.2f} GB)")
    barra_mem.config(value=mem_percent)
            
    # Actualizar la hora de la última actualización cada 2 segundos
    current_time = time.strftime("%H:%M:%S")
    if status_label:
        status_label.config(text=f"Última actualización: {current_time} | Intervalo: 2 segundos")

    #Programar la siguiente actualización automática cda 2 segundos (2000 ms)
    app_window.after(2000, actualizar_tabla)

# =========================================================================
# Construcción de la interfaz gráfica 
# =========================================================================

# INTERFAZ: Estilo personalizado para las barras de progreso
def configurar_estilos():
    style = ttk.Style()
    
    # Estilo base para las barras
    style.configure('CPU.Horizontal.TProgressbar', troughcolor='#E0E0E0', background='#2ecc71', thickness=15)

    # Estilo para la barra de Memoria
    style.configure('MEM.Horizontal.TProgressbar', troughcolor='#E0E0E0', background='#2ecc71', thickness=15)


def monitorear_procesos():
    # Esta función inicializa todos los elementos gráficos de la GUI (ventana, barras de CPU/Memoria, y la tabla de procesos).
    # Solo crea el esqueleto visual; la actualización de datos ocurre en la función 'actualizar_datos'.
    
    global app_window, tree_view, status_label
    global etiqueta_cpu, barra_cpu, etiqueta_mem, barra_mem

    # Ventana Principal
    app_window = tk.Tk()
    app_window.title("Monitor de Procesos del SO")
    app_window.geometry("850x550") 

    # Llamada a la función que configura el estilo personalizado para las barras
    configurar_estilos()
    
    # Título y Estado (Top) 
    top_frame = tk.Frame(app_window)
    top_frame.pack(pady=10, fill='x')

    title_label = tk.Label(top_frame, text="Monitor de Procesos del Sistema Operativo", font=("Arial", 16, "bold"))
    title_label.pack(side=tk.TOP, pady=5)  

    status_label = tk.Label(top_frame, text="Última actualización: --:--:-- | Intervalo: 2 segundos", font=("Arial", 10))
    status_label.pack(side=tk.TOP, pady=(0, 5))


    #  Barras Horizontales Superiores 
    bars_container_frame = tk.Frame(app_window)
    # Este contenedor ahora ocupará todo el ancho para las barras horizontales.
    bars_container_frame.pack(fill='x', padx=15, pady=(5, 15))

    #  Barra de CPU 
    cpu_frame = tk.Frame(bars_container_frame)
    cpu_frame.pack(side=tk.TOP, fill='x', pady=(0, 5))
    
    # Etiqueta de CPU 
    etiqueta_cpu = ttk.Label(cpu_frame, text="Uso de CPU: --.-%", width=35)
    etiqueta_cpu.pack(side=tk.LEFT, anchor='w')
    
    # Barra de Progreso de CPU 
    barra_cpu = ttk.Progressbar(cpu_frame, style='CPU.Horizontal.TProgressbar', 
                                 orient='horizontal', mode='determinate')
    # Expand=True permite que la barra llene el espacio restante
    barra_cpu.pack(side=tk.LEFT, fill='x', expand=True, padx=(10, 0)) 

    #  Barra de Memoria 
    mem_frame = tk.Frame(bars_container_frame)
    mem_frame.pack(side=tk.TOP, fill='x', pady=(5, 0))

    # Etiqueta de Memoria 
    etiqueta_mem = ttk.Label(mem_frame, text="Uso de Memoria: --.-%", width=35)
    etiqueta_mem.pack(side=tk.LEFT, anchor='w')
    
    # Barra de Progreso de Memoria 
    barra_mem = ttk.Progressbar(mem_frame, style='MEM.Horizontal.TProgressbar', 
                                 orient='horizontal', mode='determinate')
    barra_mem.pack(side=tk.LEFT, fill='x', expand=True, padx=(10, 0))
    
    
    # Tabla de Procesos (Bottom) 
    table_frame = tk.Frame(app_window)
    table_frame.pack(expand=True, fill='both', padx=10, pady=(0, 10))

    # Definición de Columnas para el Treeview (Tabla)
    columnas = ('PID', 'Proceso', 'CPU', 'Memoria', 'Estado')
    tree_view = ttk.Treeview(table_frame, columns=columnas, show='headings')

    # Configuración del encabezado y ancho de las columnas
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

    #  Agregar Scrollbar 
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree_view.yview)
    tree_view.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_view.pack(expand=True, fill='both')

    #  Iniciar el ciclo de actualización y el bucle principal de Tkinter
    actualizar_tabla()
    app_window.mainloop()


# Punto de entrada estándar de Python
if __name__ == "__main__":
    monitorear_procesos()