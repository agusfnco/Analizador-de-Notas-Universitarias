# -*- coding: utf-8 -*-
"""
Sistema de Seguimiento Académico v2.0
--------------------------------------
Punto de entrada de la aplicación. Maneja el menú de usuario y la persistencia
de datos utilizando el módulo logica.py, el archivo datos.json y la interfaz gui.py.

Decisión de diseño:
Este archivo ahora inicializa la interfaz gráfica de usuario en lugar del menú
de consola anterior, coordinando la carga inicial de datos desde datos.json y
asegurando el correcto guardado de los datos al cerrar la aplicación.
"""

import json
import tkinter as tk
from gui import AcademicTrackerGUI

# Constante de almacenamiento de datos
ARCHIVO_DATOS = "datos.json"

def cargar_datos():
    """
    Intenta abrir ARCHIVO_DATOS y retornar json.load()
    Si el archivo no existe (FileNotFoundError): retorna []
    Si el archivo existe pero el JSON está malformado (json.JSONDecodeError):
    imprime un aviso y retorna []
    """
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe aún (ej. primera ejecución), retornamos una lista vacía
        return []
    except json.JSONDecodeError:
        # Si la estructura JSON no es válida, advertimos al usuario y devolvemos una lista vacía
        print(f"\n[AVISO] El archivo '{ARCHIVO_DATOS}' existe pero su formato no es válido (malformado).")
        print("Se iniciará el sistema con una lista vacía de materias.")
        return []

def guardar_datos(materias):
    """
    Escribe la lista en ARCHIVO_DATOS con json.dump(), indent=2
    """
    try:
        # Escribimos los datos de manera estructurada con indentación y preservando acentos
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(materias, f, indent=2, ensure_ascii=False)
        print("\n[INFO] ¡Datos guardados exitosamente en datos.json!")
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un error al intentar guardar los datos: {e}")

def main():
    """
    Punto de entrada de la aplicación gráfica.
    Carga los datos iniciales, crea la ventana de Tkinter y establece el protocolo
    de cerrado de ventana para la persistencia automática de los datos.
    """
    # 1. Cargar datos al arrancar
    materias = cargar_datos()
    
    # 2. Inicializar la interfaz de Tkinter
    root = tk.Tk()
    app = AcademicTrackerGUI(root, materias)
    
    # 3. Guardar datos automáticamente cuando se cierra la ventana
    def al_cerrar():
        guardar_datos(materias)
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", al_cerrar)
    
    # 4. Iniciar el bucle de eventos principal
    root.mainloop()

if __name__ == "__main__":
    main()
