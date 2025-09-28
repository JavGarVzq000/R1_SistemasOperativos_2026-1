# RETO 1: Monitoreo de Procesos del SO (Usando Python y psutil)

## Objetivo

Analizar los procesos en ejecución en su computadora real.

## Descripción

- Usar la librería `psutil` en Python para obtener la lista de procesos activos en el sistema.
- Mostrar información como **PID**, **nombre del proceso**, **uso de CPU** y **memoria**.
- Simular un cambio de contexto mostrando qué procesos están en ejecución y cuáles en espera.

## Ejemplo de salida esperada

```yaml
PID: 1234 | Proceso: chrome.exe   | Estado: Ejecutándose
PID: 5678 | Proceso: explorer.exe | Estado: Listo
PID: 9101 | Proceso: spotify.exe  | Estado: Bloqueado (esperando I/O)

## ¿Por qué Python?
Python es un lenguaje de programación de alto nivel, interpretado y de código abierto. Destaca 
de entre otros lenguajes por su sintaxis sencilla y legibilidad. Lenguaje de propósito general,
versátil y muy utilizado en desarrollo web y de software, ciencia de datos, aprendizaje automático y
más. Pero, además de su amplia comunidad y su capacidad de ejecutarse en diversas plataformas, este 
lenguaje posee sus bibliotecas extensas, una de ellas (y es la que usamos en este mini-proyecto) es psutil. 

## Uso de la biblioteca psutil
La biblioteca psutil es una herramienta muy útil para un programador cuyo objetivo es análisis y gestión
sobre el sistema de computo en que trabaja, pues posee funcionalidades como las siguientes

- Monitorización del sistema
- Gestión de procesos
- Información de red
- Uso de sensores


Por ello, se utiliza para

- Desarrollo de herramientas de monotorización.
- Optimización y perfilado.
- Automatización de tareas.
- Desarrollo de aplicaciones de seguridad.