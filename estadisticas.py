# -*- coding: utf-8 -*-
"""
Módulo de Estadísticas y Exportación (estadisticas.py)
-----------------------------------------------------
Proporciona funciones para calcular estadísticas descriptivas, graficar promedios y
distribución de notas, y exportar datos académicos en formatos CSV y PDF.
"""

import statistics
import csv
import tkinter as tk

# Intentamos importar matplotlib de forma condicional para manejar su ausencia
try:
    # pyrefly: ignore [missing-import]
    import matplotlib
    # Evitar problemas de hilos configurando un backend compatible con Tkinter
    matplotlib.use("TkAgg")
    # pyrefly: ignore [missing-import]
    import matplotlib.pyplot as plt
    # pyrefly: ignore [missing-import]
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False

# Intentamos importar reportlab de forma condicional
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from datetime import datetime
    REPORTLAB_DISPONIBLE = True
except ImportError:
    REPORTLAB_DISPONIBLE = False


def calcular_stats(materias):
    """
    Calcula estadísticas descriptivas generales de la carrera a partir de la lista de materias.
    
    Parámetros:
    - materias (list): Lista de diccionarios con la información de materias y notas.
    
    Retorna:
    - dict: Diccionario con estadísticas calculadas.
    """
    # Inicialización por defecto en caso de no haber notas
    stats_vacias = {
        "promedio_general": 0.0,
        "nota_maxima": 0.0,
        "nota_minima": 0.0,
        "desvio_estandar": 0.0,
        "mejor_materia": "",
        "aprobadas": 0,
        "desaprobadas": len(materias),
        "total_materias": len(materias),
        "total_notas": 0
    }
    
    if not materias:
        return stats_vacias
        
    # Recopilar todas las notas de todas las materias
    todas_las_notas = []
    for materia in materias:
        todas_las_notas.extend(materia.get("notas", []))
        
    total_notas = len(todas_las_notas)
    
    # Si no hay notas cargadas en absoluto, retornar la estructura base
    if total_notas == 0:
        return stats_vacias
        
    # Cálculos estadísticos generales de notas
    promedio_general = round(sum(todas_las_notas) / total_notas, 2)
    nota_maxima = max(todas_las_notas)
    nota_minima = min(todas_las_notas)
    
    # Desvío estándar muestral (requiere al menos 2 notas)
    if total_notas >= 2:
        desvio_estandar = round(statistics.stdev(todas_las_notas), 2)
    else:
        desvio_estandar = 0.0
        
    # Calcular mejor materia e índices de aprobación
    mejor_materia = ""
    max_promedio_materia = -1.0
    aprobadas = 0
    desaprobadas = 0
    
    for materia in materias:
        notas_materia = materia.get("notas", [])
        promedio_materia = sum(notas_materia) / len(notas_materia) if notas_materia else 0.0
        
        # Evaluar mejor promedio propio
        if notas_materia and promedio_materia > max_promedio_materia:
            max_promedio_materia = promedio_materia
            mejor_materia = materia["nombre"]
            
        # Evaluar aprobación (promedio >= 6)
        if promedio_materia >= 6:
            aprobadas += 1
        else:
            desaprobadas += 1
            
    return {
        "promedio_general": promedio_general,
        "nota_maxima": nota_maxima,
        "nota_minima": nota_minima,
        "desvio_estandar": desvio_estandar,
        "mejor_materia": mejor_materia,
        "aprobadas": aprobadas,
        "desaprobadas": desaprobadas,
        "total_materias": len(materias),
        "total_notas": total_notas
    }


def graficar_promedios(materias, ventana_padre):
    """
    Muestra una ventana Toplevel con un gráfico de barras horizontal de los promedios por materia.
    
    Parámetros:
    - materias (list): Lista de materias.
    - ventana_padre (tk.Tk/tk.Toplevel): Ventana de Tkinter sobre la cual se monta la Toplevel.
    """
    import tkinter.messagebox as messagebox
    
    # Control de dependencia
    if not MATPLOTLIB_DISPONIBLE:
        messagebox.showerror(
            "Biblioteca Faltante",
            "Para poder ver los gráficos, es necesario instalar la biblioteca 'matplotlib'.\n\n"
            "Instálela ejecutando:\npip install matplotlib"
        )
        return
        
    if not materias:
        messagebox.showwarning("Sin datos", "No hay materias registradas para graficar.")
        return
        
    # Obtener nombres y calcular promedios
    nombres = []
    promedios = []
    for m in materias:
        nombres.append(m["nombre"])
        notas = m.get("notas", [])
        promedios.append(sum(notas) / len(notas) if notas else 0.0)
        
    # Crear la ventana secundaria
    top = tk.Toplevel(ventana_padre)
    top.title("Gráfico de Promedios por Materia")
    top.geometry("650x450")
    top.configure(bg="#ffffff")
    top.transient(ventana_padre)  # Mantiene la ventana siempre por encima del padre
    
    # Crear la figura del gráfico
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    
    # Dibujar las barras horizontales
    y_pos = range(len(nombres))
    ax.barh(y_pos, promedios, color="#4a90d9", height=0.6, align="center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(nombres, fontsize=9)
    ax.invert_yaxis()  # Mostrar la primera materia en la parte superior
    
    # Línea vertical punteada roja en promedio=6 (umbral de aprobación)
    ax.axvline(x=6.0, color="red", linestyle="--", linewidth=1.5, label="Umbral de Aprobación (6.0)")
    
    # Etiquetas y títulos en español
    ax.set_xlabel("Promedio de Notas", fontsize=10, fontweight="bold", labelpad=10)
    ax.set_title("Promedio por Materia", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlim(0, 10)
    ax.set_xticks(range(11))
    ax.grid(axis="x", linestyle=":", alpha=0.6)
    ax.legend(loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#cccccc")
    
    plt.tight_layout()
    
    # Embeber la figura de matplotlib en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Liberar memoria de matplotlib al cerrar la ventana secundaria
    def al_cerrar():
        plt.close(fig)
        top.destroy()
        
    top.protocol("WM_DELETE_WINDOW", al_cerrar)


def graficar_distribucion(materias, ventana_padre):
    """
    Muestra una ventana Toplevel con el histograma de frecuencias de todas las notas.
    
    Parámetros:
    - materias (list): Lista de materias.
    - ventana_padre (tk.Tk/tk.Toplevel): Ventana principal.
    """
    import tkinter.messagebox as messagebox
    
    # Control de dependencia
    if not MATPLOTLIB_DISPONIBLE:
        messagebox.showerror(
            "Biblioteca Faltante",
            "Para poder ver los gráficos, es necesario instalar la biblioteca 'matplotlib'.\n\n"
            "Instálela ejecutando:\npip install matplotlib"
        )
        return
        
    # Recopilar todas las notas
    todas_las_notas = []
    for m in materias:
        todas_las_notas.extend(m.get("notas", []))
        
    if not todas_las_notas:
        messagebox.showwarning("Sin notas", "No hay notas cargadas para visualizar la distribución.")
        return
        
    # Crear la ventana secundaria
    top = tk.Toplevel(ventana_padre)
    top.title("Distribución de Notas")
    top.geometry("650x450")
    top.configure(bg="#ffffff")
    top.transient(ventana_padre)
    
    # Crear figura del gráfico
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    
    # Configurar los límites de las barras centradas en cada nota (1 al 10)
    bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5]
    
    # Dibujar histograma
    ax.hist(todas_las_notas, bins=bins, color="#5cb85c", edgecolor="#ffffff", rwidth=0.85, align="mid")
    
    # Configurar ejes y títulos
    ax.set_xlabel("Calificación (Nota)", fontsize=10, fontweight="bold", labelpad=10)
    ax.set_ylabel("Frecuencia (Cantidad)", fontsize=10, fontweight="bold", labelpad=10)
    ax.set_title("Distribución de Notas", fontsize=12, fontweight="bold", pad=15)
    ax.set_xticks(range(1, 11))
    ax.set_xlim(0.5, 10.5)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    
    plt.tight_layout()
    
    # Embeber en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Liberar memoria de matplotlib al cerrar la ventana secundaria
    def al_cerrar():
        plt.close(fig)
        top.destroy()
        
    top.protocol("WM_DELETE_WINDOW", al_cerrar)


def exportar_csv(materias, ruta):
    """
    Exporta todas las notas individuales cargadas a un archivo CSV estructurado.
    
    Parámetros:
    - materias (list): Lista de materias.
    - ruta (str): Ruta absoluta donde se guardará el archivo.
    
    Retorna:
    - bool: True si la exportación fue exitosa, False en caso contrario.
    
    Nota: Se usa punto y coma (;) como separador para compatibilidad con Excel
    en Windows con configuración regional en español/latinoamérica.
    """
    try:
        # utf-8-sig incluye el BOM (Byte Order Mark) para que Excel detecte
        # automáticamente el encoding y muestre los caracteres especiales correctamente
        with open(ruta, mode="w", newline="", encoding="utf-8-sig") as archivo:
            # Punto y coma como delimitador: es el estándar de CSV en Excel en español
            writer = csv.writer(archivo, delimiter=";")
            # Cabeceras del archivo CSV
            writer.writerow(["Materia", "Cuatrimestre", "Año", "Nota", "Índice"])
            
            for materia in materias:
                nombre = materia["nombre"]
                cuatrimestre = materia.get("cuatrimestre", "")
                anio = materia.get("año", "")
                notas = materia.get("notas", [])
                for index, nota in enumerate(notas, start=1):
                    writer.writerow([nombre, cuatrimestre, anio, nota, index])
                    
        return True
    except Exception as e:
        print(f"Error al escribir el archivo CSV: {e}")
        return False


def exportar_pdf(materias, ruta):
    """
    Exporta un informe académico consolidado en formato PDF usando ReportLab.
    
    Parámetros:
    - materias (list): Lista de materias.
    - ruta (str): Ruta absoluta del archivo PDF.
    
    Retorna:
    - bool: True si la exportación fue exitosa, False en caso de error o biblioteca no instalada.
    """
    import tkinter.messagebox as messagebox
    
    # Control de dependencia
    if not REPORTLAB_DISPONIBLE:
        messagebox.showerror(
            "Biblioteca Faltante",
            "Para poder exportar a PDF, es necesario instalar la biblioteca 'reportlab'.\n\n"
            "Instálela ejecutando:\npip install reportlab"
        )
        return False
        
    try:
        # Configurar documento
        doc = SimpleDocTemplate(
            ruta, 
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados para el reporte
        style_title = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#2c3e50"),
            alignment=1,  # Centrado
            spaceAfter=6
        )
        
        style_subtitle = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=colors.HexColor("#7f8c8d"),
            alignment=1,
            spaceAfter=25
        )
        
        style_h2 = ParagraphStyle(
            "ReportH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#2c3e50"),
            spaceBefore=15,
            spaceAfter=8
        )
        
        # 1. Encabezado del reporte
        story.append(Paragraph("Resumen Académico", style_title))
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        story.append(Paragraph(f"Generado el: {fecha_actual}", style_subtitle))
        
        # 2. Sección: Tabla de materias
        story.append(Paragraph("Detalle de Materias", style_h2))
        
        tabla_datos = [["Materia", "Notas registradas", "Promedio", "Estado"]]
        for m in materias:
            nombre = m["nombre"]
            notas = m.get("notas", [])
            notas_str = ", ".join(str(n) for n in notas) if notas else "Sin notas"
            promedio = sum(notas) / len(notas) if notas else 0.0
            estado = "Aprobada" if promedio >= 6 else "En curso"
            tabla_datos.append([nombre, notas_str, f"{promedio:.2f}", estado])
            
        # Creamos y configuramos la tabla de materias
        t_materias = Table(tabla_datos, colWidths=[200, 130, 75, 75])
        t_style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4a90d9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ALIGN", (0, 1), (0, -1), "LEFT"),  # Nombre de materia alineado a la izquierda
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
        ]
        
        # Añadir alternancia de colores a las filas
        for idx in range(1, len(tabla_datos)):
            color_fila = colors.HexColor("#ffffff") if idx % 2 != 0 else colors.HexColor("#f9f9f9")
            t_style.append(("BACKGROUND", (0, idx), (-1, idx), color_fila))
            
        t_materias.setStyle(TableStyle(t_style))
        story.append(t_materias)
        
        # Separación
        story.append(Spacer(1, 20))
        
        # 3. Sección: Cuadro de estadísticas generales
        story.append(Paragraph("Estadísticas Generales", style_h2))
        
        stats = calcular_stats(materias)
        stats_datos = [
            ["Métrica de Carrera", "Valor Calculado"],
            ["Promedio General de Notas", f"{stats['promedio_general']:.2f}"],
            ["Calificación Máxima", str(stats['nota_maxima'])],
            ["Calificación Mínima", str(stats['nota_minima'])],
            ["Desvío Estándar", f"{stats['desvio_estandar']:.2f}"],
            ["Materia con Mayor Promedio", stats['mejor_materia'] or "N/A"],
            ["Materias Aprobadas (Prom >= 6)", str(stats['aprobadas'])],
            ["Materias En Curso/Desaprobadas", str(stats['desaprobadas'])],
            ["Cantidad Total de Materias", str(stats['total_materias'])],
            ["Cantidad Total de Notas", str(stats['total_notas'])]
        ]
        
        t_stats = Table(stats_datos, colWidths=[240, 240])
        t_stats.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5f5f5")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),  # Valores alineados a la derecha
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("PADDING", (0, 0), (-1, -1), 6)
        ]))
        story.append(t_stats)
        
        # Compilación del reporte
        doc.build(story)
        return True
    except Exception as e:
        print(f"Error al escribir el reporte PDF: {e}")
        return False

# --------------------------------══════════════════════════════════════
# Comandos de instalación para las dependencias necesarias:
# pip install matplotlib reportlab
# --------------------------------══════════════════════════════════════
