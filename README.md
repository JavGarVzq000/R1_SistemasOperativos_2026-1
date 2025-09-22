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
