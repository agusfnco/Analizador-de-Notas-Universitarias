# -*- coding: utf-8 -*-
"""
Módulo de Lógica de Negocio (logica.py)
--------------------------------------
Contiene las funciones principales para gestionar las materias, verlas,
agregar notas y calcular el promedio general.

Decisión de diseño:
Este archivo aísla la lógica interna del sistema de la persistencia en disco
y de la interfaz de consola, facilitando pruebas y mantenimiento futuro.
"""

def agregar_materia(materias):
    """
    Pide al usuario los datos de una nueva materia (nombre, cuatrimestre y año) 
    a través del input de consola y agrega un nuevo diccionario con estos datos 
    a la lista de materias.
    
    Parámetros:
    - materias (list): Lista de diccionarios donde cada uno representa una materia.
    """
    print("\n=== AGREGAR NUEVA MATERIA ===")
    
    # Solicitar el nombre de la materia, quitando espacios extra al principio y al final
    nombre = input("Ingrese el nombre de la materia (ej. Análisis Matemático I): ").strip()
    if not nombre:
        print("Error: El nombre de la materia no puede estar vacío.")
        return

    # Solicitar el cuatrimestre con validación de tipo numérico entero
    try:
        cuatrimestre = int(input("Ingrese el cuatrimestre (número entero, ej. 1 o 2): "))
    except ValueError:
        print("Error: El cuatrimestre debe ser un número entero.")
        return

    # Solicitar el año con validación de tipo numérico entero
    try:
        anio = int(input("Ingrese el año de cursada (número entero, ej. 2024): "))
    except ValueError:
        print("Error: El año debe ser un número entero.")
        return

    # Creamos la materia con la estructura de diccionario requerida
    # Las notas se inicializan como una lista vacía
    nueva_materia = {
        "nombre": nombre,
        "cuatrimestre": cuatrimestre,
        "año": anio,
        "notas": []
    }

    # Agregamos el diccionario a la lista principal recibida por parámetro
    materias.append(nueva_materia)
    print(f"\n¡La materia '{nombre}' fue registrada exitosamente!")


def ver_materias(materias):
    """
    Muestra en pantalla todas las materias registradas y sus respectivas notas.
    Si la lista está vacía, le informa al usuario para evitar pantallas en blanco.
    
    Parámetros:
    - materias (list): Lista de diccionarios con la información académica.
    """
    print("\n=== MATERIAS REGISTRADAS ===")
    
    # Validación: si no hay materias cargadas en la lista, avisamos y salimos
    if not materias:
        print("No hay materias registradas en el sistema todavía.")
        print("Por favor, agregue una materia usando la opción 1 del menú.")
        return

    # Recorremos la lista y formateamos la salida para que sea legible
    for index, materia in enumerate(materias, start=1):
        nombre = materia["nombre"]
        cuatrimestre = materia["cuatrimestre"]
        anio = materia["año"]
        notas = materia["notas"]
        
        # Mostramos las notas separadas por comas, o una aclaración si no hay ninguna
        if notas:
            notas_str = ", ".join(str(nota) for nota in notas)
        else:
            notas_str = "Sin notas registradas"
            
        print(f"{index}. {nombre}")
        print(f"   Año: {anio} | Cuatrimestre: {cuatrimestre} | Notas: [{notas_str}]")
        print("-" * 50)


def agregar_nota(materias):
    """
    Busca una materia por su nombre en la lista y le añade una nueva nota.
    Valida la existencia de materias, la existencia de la materia buscada 
    y que la nota sea un número real/entero entre 1 y 10.
    
    Parámetros:
    - materias (list): Lista de diccionarios con la información académica.
    """
    print("\n=== AGREGAR NOTA A MATERIA ===")
    
    # Validación: si no hay materias, no podemos agregar notas
    if not materias:
        print("No hay materias registradas en el sistema. Registre una materia primero.")
        return

    # Pedimos el nombre de la materia a buscar
    busqueda = input("Ingrese el nombre de la materia: ").strip()
    
    # Buscamos la materia ignorando mayúsculas/minúsculas para mejorar la experiencia de usuario
    materia_encontrada = None
    for materia in materias:
        if materia["nombre"].lower() == busqueda.lower():
            materia_encontrada = materia
            break

    # Si no la encontramos, avisamos al usuario
    if not materia_encontrada:
        print(f"Error: No se encontró la materia '{busqueda}'. Verifique el nombre e intente de nuevo.")
        return

    # Pedimos la nota y la validamos
    nota_input = input("Ingrese la nota obtenida (número entre 1 y 10): ").strip()
    
    try:
        # Reemplazamos la coma por el punto por si el usuario ingresa un decimal como "7,5"
        nota_filtrada = nota_input.replace(",", ".")
        nota = float(nota_filtrada)
        
        # Validamos que la nota esté dentro del rango académico permitido (1 a 10)
        if 1 <= nota <= 10:
            # Si el número es decimal pero equivale a un entero (ej: 8.0), lo convertimos a entero para estética
            if nota.is_integer():
                nota = int(nota)
                
            # Agregamos la nota a la lista de notas de la materia seleccionada
            materia_encontrada["notas"].append(nota)
            print(f"\n¡Nota {nota} agregada con éxito a '{materia_encontrada['nombre']}'!")
        else:
            print("Error: La nota debe ser un número entre 1 y 10.")
    except ValueError:
        print("Error: El valor ingresado no es un número válido.")


def calcular_promedio(materias):
    """
    Suma todas las notas cargadas en todas las materias y calcula el promedio
    general de la carrera. Valida si hay materias o si hay notas registradas.
    
    Parámetros:
    - materias (list): Lista de diccionarios con la información académica.
    """
    print("\n=== CALCULAR PROMEDIO GENERAL ===")
    
    # Validación: si no hay materias, no hay promedio que calcular
    if not materias:
        print("No hay materias registradas en el sistema. Agregue materias para calcular el promedio.")
        return

    # Recolectamos todas las notas de todas las materias en una sola lista
    todas_las_notas = []
    for materia in materias:
        todas_las_notas.extend(materia["notas"])

    # Validación: si hay materias pero ninguna tiene notas, no podemos dividir por cero
    if not todas_las_notas:
        print("No se encontraron notas registradas en ninguna de las materias.")
        print("Agregue notas primero usando la opción 3 del menú.")
        return

    # Calculamos el promedio general sumando todo y dividiendo por la cantidad
    promedio = sum(todas_las_notas) / len(todas_las_notas)
    
    print(f"Total de notas evaluadas: {len(todas_las_notas)}")
    print(f"Promedio general actual: {promedio:.2f}")
