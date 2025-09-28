import psutil
import time
import tkinter as tk
from tkinter import ttk

# =========================================================================
# (Omitimos ESTADOS_SIMULADOS y obtener_y_mostrar_proceso ya que la GUI solo mostrará el uso del SISTEMA)
# Si quieres mostrar procesos individuales, necesitarías un widget Treeview o un Listbox.
# =========================================================================

# Frecuencia de actualización de la GUI en milisegundos (2000 ms = 2 segundos)
TIEMPO_REFRESCO_MS = 2000

def actualizar_monitoreo(root, cpu_bar, mem_bar, cpu_label, mem_label):
    """
    Función: actualizar_monitoreo
    Responsabilidad: Obtiene los valores globales de CPU y memoria del sistema y actualiza los widgets de la GUI.
    """
    try:
        # 1. Obtener Uso de CPU del Sistema
        # psutil.cpu_percent(interval=None) devuelve el uso desde la última llamada (ideal para bucles)
        uso_cpu = psutil.cpu_percent(interval=None) 
        
        # 2. Obtener Uso de Memoria del Sistema
        mem_info = psutil.virtual_memory()
        uso_memoria_porcentaje = mem_info.percent
        
        # 3. Actualizar Widgets (Barras de Progreso)
        cpu_bar['value'] = uso_cpu       # Establece el valor de la barra de CPU
        mem_bar['value'] = uso_memoria_porcentaje # Establece el valor de la barra de Memoria
        
        # 4. Actualizar Widgets (Etiquetas de Texto)
        cpu_label.config(text=f"Uso de CPU: {uso_cpu:.1f}%")
        # Muestra el uso total en GB/MB para mayor detalle
        mem_label.config(text=f"Memoria Usada: {mem_info.used / (1024**3):.2f} GB ({uso_memoria_porcentaje:.1f}%)")
        
    except Exception as e:
        print(f"Error durante la actualización: {e}")
    
    # 5. Programar la Próxima Actualización
    # root.after(tiempo, función, *args) llama a la función después del tiempo especificado.
    root.after(TIEMPO_REFRESCO_MS, actualizar_monitoreo, root, cpu_bar, mem_bar, cpu_label, mem_label)


def crear_interfaz_principal():
    """
    Función: crear_interfaz_principal
    Responsabilidad: Inicializa la ventana de Tkinter y crea todos los widgets.
    """
    # 1. Configuración de la Ventana Principal
    root = tk.Tk()
    root.title("Monitoreo de Recursos del Sistema")
    # Agregamos padding para que la ventana se vea mejor
    root.geometry("400x180")
    
    # 2. Creación de Etiquetas y Barras de Progreso (CPU)
    
    # Etiqueta de Título
    ttk.Label(root, text="Monitoreo de Recursos", font=("Arial", 14, "bold")).pack(pady=10)
    
    # Etiqueta de CPU (Contendrá el texto de porcentaje)
    cpu_label = ttk.Label(root, text="Uso de CPU: --.-%")
    cpu_label.pack(pady=(5, 2), padx=10, anchor='w')
    
    # Barra de Progreso de CPU (style=progressbar para Tkinter)
    cpu_bar = ttk.Progressbar(root, orient='horizontal', length=380, mode='determinate')
    cpu_bar.pack(pady=5, padx=10)
    
    # 3. Creación de Etiquetas y Barras de Progreso (Memoria)
    
    # Etiqueta de Memoria (Contendrá el texto de porcentaje y GB)
    mem_label = ttk.Label(root, text="Memoria Usada: --.-%")
    mem_label.pack(pady=(5, 2), padx=10, anchor='w')
    
    # Barra de Progreso de Memoria
    mem_bar = ttk.Progressbar(root, orient='horizontal', length=380, mode='determinate')
    mem_bar.pack(pady=5, padx=10)
    
    # 4. Iniciar el Monitoreo
    # Llamamos a la función de actualización la primera vez. Ella se encargará de programarse a sí misma.
    actualizar_monitoreo(root, cpu_bar, mem_bar, cpu_label, mem_label)
    
    # 5. Iniciar el Bucle Principal de Tkinter
    root.mainloop()


# Punto de entrada estándar de Python
if __name__ == "__main__":
    # Llama a la función que crea y gestiona la GUI.
    crear_interfaz_principal()