# -*- coding: utf-8 -*-
"""
Sistema de Seguimiento Académico v2.0
--------------------------------------
Punto de entrada de la aplicación. Maneja el menú de usuario y la persistencia
de datos utilizando el módulo logica.py y el archivo datos.json.

Decisión de diseño:
Este archivo se enfoca exclusivamente en la interacción con el usuario (interfaz de consola)
y el almacenamiento persistente en disco, delegando todo el procesamiento a logica.py.
"""

import json
# Importamos las cuatro funciones desde el nuevo archivo logica.py
from logica import agregar_materia, ver_materias, agregar_nota, calcular_promedio

# 2. Definir ARCHIVO_DATOS = "datos.json" como constante al principio
ARCHIVO_DATOS = "datos.json"

# 3. Función cargar_datos()
def cargar_datos():
    """
    Intenta abrir ARCHIVO_DATOS y retornar json.load()
    Si el archivo no existe (FileNotFoundError): retorna []
    Si el archivo existe pero el JSON está malformado (json.JSONDecodeError):
    imprime un aviso y retorna []
    """
    try:
        # Abrimos el archivo con codificación UTF-8 para garantizar soporte de caracteres especiales
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

# 4. Función guardar_datos(materias)
def guardar_datos(materias):
    """
    Escribe la lista en ARCHIVO_DATOS con json.dump(), indent=2
    """
    try:
        # Escribimos los datos de manera estructurada con indentación y preservando acentos/caracteres especiales
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(materias, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un error al intentar guardar los datos: {e}")

# 5. El menú principal (while True)
def menu():
    """
    Presenta la interfaz de usuario en consola, procesa las opciones y asegura
    la persistencia de los datos al arrancar y al salir.
    """
    # Al arrancar: materias = cargar_datos()
    materias = cargar_datos()
    
    while True:
        print("\n==================================================")
        print("       SISTEMA DE SEGUIMIENTO ACADÉMICO")
        print("==================================================")
        print("1. Agregar nueva materia")
        print("2. Ver materias registradas")
        print("3. Agregar nota a una materia")
        print("4. Calcular promedio general")
        print("5. Salir del programa")
        print("==================================================")
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        # Estructura de control para derivar a las funciones según la opción
        if opcion == "1":
            agregar_materia(materias)
        elif opcion == "2":
            ver_materias(materias)
        elif opcion == "3":
            agregar_nota(materias)
        elif opcion == "4":
            calcular_promedio(materias)
        elif opcion == "5":
            # Al elegir la opción "salir": guardar_datos(materias) y luego break
            guardar_datos(materias)
            print("\n¡Gracias por utilizar el Sistema de Seguimiento Académico!")
            print("Mucho éxito en tu carrera de Estadística y Ciencia de Datos.")
            print("¡Hasta luego!\n")
            break
        else:
            # Validación de opción inválida
            print("\nOpción inválida. Por favor, ingrese un número del 1 al 5.")

# 6. Bloque if __name__ == "__main__"
if __name__ == "__main__":
    menu()
