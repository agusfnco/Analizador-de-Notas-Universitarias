# -*- coding: utf-8 -*-
"""
Interfaz Gráfica de Usuario (gui.py)
------------------------------------
Implementa la interfaz visual usando tkinter para el Sistema de Seguimiento Académico.
Utiliza logica.py para realizar las operaciones y main.py como punto de entrada.
Soporta ejecución directa con datos de ejemplo en caso de que logica.py no esté disponible.
"""

import tkinter as tk
from tkinter import messagebox
import builtins

# Intentamos importar la lógica original
try:
    import logica
    LOGICA_DISPONIBLE = True
except ImportError:
    LOGICA_DISPONIBLE = False

# Si la lógica no está disponible, definimos funciones de respaldo idénticas
if not LOGICA_DISPONIBLE:
    def agregar_materia(materias):
        # Lee de la entrada estándar simulada por el mock
        nombre = input().strip()
        cuatrimestre = int(input())
        anio = int(input())
        
        nueva_materia = {
            "nombre": nombre,
            "cuatrimestre": cuatrimestre,
            "año": anio,
            "notas": []
        }
        materias.append(nueva_materia)

    def agregar_nota(materias):
        # Lee de la entrada estándar simulada por el mock
        busqueda = input().strip()
        nota_input = input().strip()
        
        nota = float(nota_input.replace(",", "."))
        if nota.is_integer():
            nota = int(nota)
            
        for materia in materias:
            if materia["nombre"].lower() == busqueda.lower():
                materia["notas"].append(nota)
                break
else:
    from logica import agregar_materia, agregar_nota


class AcademicTrackerGUI:
    def __init__(self, root, materias):
        """
        Inicializa la ventana principal de la interfaz gráfica.
        
        Parámetros:
        - root (tk.Tk): Instancia de la ventana principal de Tkinter.
        - materias (list): Lista de diccionarios con la información académica.
        """
        self.root = root
        self.materias = materias
        
        # Configuración de la ventana principal
        self.root.title("Sistema de Seguimiento Académico")
        self.root.geometry("750x500")
        self.root.configure(bg="#f5f5f5")
        
        # Tipografías limpias y consistentes
        self.font_main = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 10, "bold")
        self.font_title = ("Segoe UI", 12, "bold")
        self.font_small_italic = ("Segoe UI", 9, "italic")
        
        # Configuración de las columnas del grid principal
        self.root.grid_columnconfigure(0, weight=1, uniform="group1")
        self.root.grid_columnconfigure(1, weight=1, uniform="group1")
        self.root.grid_rowconfigure(0, weight=1)
        
        # Crear los paneles
        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        
        # Cargar los datos iniciales
        self.refrescar_lista()

    def crear_panel_izquierdo(self):
        """
        Crea el panel izquierdo que contiene los formularios de entrada.
        """
        # Contenedor del panel izquierdo con estilo de tarjeta moderna
        self.left_frame = tk.Frame(
            self.root, 
            bg="#ffffff", 
            padx=15, 
            pady=15,
            highlightbackground="#e0e0e0", 
            highlightthickness=1,
            bd=0
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 7), pady=15)
        
        # ----------------------------------------------------
        # SECCIÓN: NUEVA MATERIA
        # ----------------------------------------------------
        lbl_seccion_materia = tk.Label(
            self.left_frame, 
            text="Nueva Materia", 
            font=self.font_title, 
            fg="#2c3e50", 
            bg="#ffffff"
        )
        lbl_seccion_materia.pack(anchor="w", pady=(0, 10))
        
        # Campo Nombre
        lbl_nombre = tk.Label(self.left_frame, text="Nombre:", font=self.font_main, bg="#ffffff", fg="#333333")
        lbl_nombre.pack(anchor="w", pady=(2, 0))
        self.entry_nombre = self.crear_entry_estilizado(self.left_frame)
        self.entry_nombre.pack(fill="x", pady=(0, 8))
        
        # Campo Cuatrimestre
        lbl_cuatrimestre = tk.Label(self.left_frame, text="Cuatrimestre (número):", font=self.font_main, bg="#ffffff", fg="#333333")
        lbl_cuatrimestre.pack(anchor="w", pady=(2, 0))
        self.entry_cuatrimestre = self.crear_entry_estilizado(self.left_frame)
        self.entry_cuatrimestre.pack(fill="x", pady=(0, 8))
        
        # Campo Año
        lbl_anio = tk.Label(self.left_frame, text="Año:", font=self.font_main, bg="#ffffff", fg="#333333")
        lbl_anio.pack(anchor="w", pady=(2, 0))
        self.entry_anio = self.crear_entry_estilizado(self.left_frame)
        self.entry_anio.pack(fill="x", pady=(0, 12))
        
        # Botón Agregar Materia
        btn_agregar_materia = self.crear_boton_estilizado(
            self.left_frame, 
            text="Agregar materia", 
            command=self.manejador_agregar_materia
        )
        btn_agregar_materia.pack(fill="x", pady=(0, 15))
        
        # Separador visual entre secciones
        separador = tk.Frame(self.left_frame, height=1, bg="#e0e0e0")
        separador.pack(fill="x", pady=12)
        
        # ----------------------------------------------------
        # SECCIÓN: AGREGAR NOTA
        # ----------------------------------------------------
        lbl_seccion_nota = tk.Label(
            self.left_frame, 
            text="Agregar Nota", 
            font=self.font_title, 
            fg="#2c3e50", 
            bg="#ffffff"
        )
        lbl_seccion_nota.pack(anchor="w", pady=(0, 2))
        
        lbl_info_seleccion = tk.Label(
            self.left_frame, 
            text="Seleccioná una materia de la lista", 
            font=self.font_small_italic, 
            fg="#7f8c8d", 
            bg="#ffffff"
        )
        lbl_info_seleccion.pack(anchor="w", pady=(0, 10))
        
        # Campo Nota
        lbl_nota = tk.Label(self.left_frame, text="Nota (1-10):", font=self.font_main, bg="#ffffff", fg="#333333")
        lbl_nota.pack(anchor="w", pady=(2, 0))
        self.entry_nota = self.crear_entry_estilizado(self.left_frame)
        self.entry_nota.pack(fill="x", pady=(0, 12))
        
        # Botón Agregar Nota
        btn_agregar_nota = self.crear_boton_estilizado(
            self.left_frame, 
            text="Agregar nota", 
            command=self.manejador_agregar_nota
        )
        btn_agregar_nota.pack(fill="x")

    def crear_panel_derecho(self):
        """
        Crea el panel derecho que contiene el Listbox, notas y promedio general.
        """
        # Contenedor del panel derecho con estilo de tarjeta moderna
        self.right_frame = tk.Frame(
            self.root, 
            bg="#ffffff", 
            padx=15, 
            pady=15,
            highlightbackground="#e0e0e0", 
            highlightthickness=1,
            bd=0
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(7, 15), pady=15)
        
        # Título de la sección
        lbl_titulo_materias = tk.Label(
            self.right_frame, 
            text="Materias", 
            font=self.font_title, 
            fg="#2c3e50", 
            bg="#ffffff"
        )
        lbl_titulo_materias.pack(anchor="w", pady=(0, 10))
        
        # Contenedor para el Listbox y su Scrollbar
        self.listbox_container = tk.Frame(self.right_frame, bg="#ffffff")
        self.listbox_container.pack(fill="both", expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.listbox_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # Listbox estilizado
        self.listbox = tk.Listbox(
            self.listbox_container, 
            font=self.font_main,
            bg="#ffffff",
            fg="#333333",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#dcdcdc",
            highlightcolor="#4a90d9",
            selectbackground="#4a90d9",
            selectforeground="#ffffff",
            yscrollcommand=scrollbar.set,
            activestyle="none"
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Enlace del evento de selección
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.actualizar_notas_individuales())
        
        # Título Notas individuales
        lbl_titulo_notas = tk.Label(
            self.right_frame, 
            text="Notas de la materia seleccionada:", 
            font=self.font_bold, 
            fg="#7f8c8d", 
            bg="#ffffff"
        )
        lbl_titulo_notas.pack(anchor="w", pady=(5, 4))
        
        # Contenedor dinámico de notas
        self.label_notas_val = tk.Label(
            self.right_frame, 
            text="Seleccioná una materia para ver sus notas", 
            font=self.font_main, 
            fg="#7f8c8d", 
            bg="#f9f9f9", 
            padx=10, 
            pady=8, 
            anchor="w", 
            justify="left",
            wraplength=300,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#e0e0e0"
        )
        self.label_notas_val.pack(fill="x", pady=(0, 15))
        
        # Separador visual antes del promedio
        separador_prom = tk.Frame(self.right_frame, height=1, bg="#e0e0e0")
        separador_prom.pack(fill="x", pady=(5, 10))
        
        # Promedio General al pie
        self.label_promedio = tk.Label(
            self.right_frame, 
            text="Promedio general: 0.00", 
            font=("Segoe UI", 12, "bold"), 
            fg="#2c3e50", 
            bg="#ffffff"
        )
        self.label_promedio.pack(anchor="e", pady=(2, 0))

    # ----------------------------------------------------
    # MÉTODOS DE SOPORTE Y ESTILO
    # ----------------------------------------------------
    def crear_entry_estilizado(self, parent):
        """
        Crea y retorna un campo de entrada Entry estilizado.
        """
        entry = tk.Entry(
            parent,
            font=self.font_main,
            bg="#f9f9f9",
            fg="#333333",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#dcdcdc",
            highlightcolor="#4a90d9",
            insertbackground="#333333"
        )
        return entry

    def crear_boton_estilizado(self, parent, text, command):
        """
        Crea y retorna un botón plano estilizado con efectos de hover.
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg="#4a90d9",
            fg="#ffffff",
            activebackground="#357abd",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=6
        )
        
        # Efecto visual interactivo (Micro-animación de hover)
        def on_enter(e):
            btn.config(bg="#357abd")
            
        def on_leave(e):
            btn.config(bg="#4a90d9")
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    # ----------------------------------------------------
    # LÓGICA DE CONTROL Y EVENTOS
    # ----------------------------------------------------
    def refrescar_lista(self):
        """
        Limpia y vuelve a cargar los datos en el Listbox, manteniendo
        la selección del usuario si esta sigue existiendo.
        """
        # Guardar la selección previa para no perder el foco visual
        seleccion_previa = self.listbox.curselection()
        nombre_materia_previa = None
        if seleccion_previa:
            nombre_materia_previa = self.materias[seleccion_previa[0]]["nombre"]
            
        self.listbox.delete(0, tk.END)
        
        for materia in self.materias:
            notas = materia.get("notas", [])
            if notas:
                promedio = sum(notas) / len(notas)
                prom_str = f"{promedio:.2f}"
            else:
                prom_str = "0.00"
            self.listbox.insert(tk.END, f"{materia['nombre']} — prom: {prom_str}")
            
        # Intentar restaurar la selección previa
        if nombre_materia_previa:
            for idx, materia in enumerate(self.materias):
                if materia["nombre"] == nombre_materia_previa:
                    self.listbox.selection_set(idx)
                    self.listbox.activate(idx)
                    break
                    
        # Actualizar promedio general y detalles
        self.actualizar_promedio_general()
        self.actualizar_notas_individuales()

    def actualizar_promedio_general(self):
        """
        Recalcula dinámicamente el promedio general sumando todas las notas de todas las materias.
        """
        todas_las_notas = []
        for materia in self.materias:
            todas_las_notas.extend(materia.get("notas", []))
            
        if not todas_las_notas:
            self.label_promedio.config(text="Promedio general: 0.00")
        else:
            promedio = sum(todas_las_notas) / len(todas_las_notas)
            self.label_promedio.config(text=f"Promedio general: {promedio:.2f}")

    def actualizar_notas_individuales(self):
        """
        Muestra la lista de notas individuales de la materia seleccionada en el Listbox,
        junto con el cuatrimestre y el año correspondientes.
        """
        seleccion = self.listbox.curselection()
        if seleccion:
            idx = seleccion[0]
            materia = self.materias[idx]
            notas = materia.get("notas", [])
            anio = materia.get("año", "N/A")
            cuat = materia.get("cuatrimestre", "N/A")
            
            if notas:
                notas_str = f"[{', '.join(str(n) for n in notas)}]"
            else:
                notas_str = "Sin notas registradas"
                
            self.label_notas_val.config(
                text=f"{materia['nombre']} — {cuat}° Cuat. | {anio}\nNotas: {notas_str}", 
                fg="#333333"
            )
        else:
            self.label_notas_val.config(
                text="Seleccioná una materia para ver sus notas", 
                fg="#7f8c8d"
            )

    def manejador_agregar_materia(self):
        """
        Manejador para el evento del botón 'Agregar materia'. Valida las entradas,
        simula la entrada por consola para logica.py y refresca la lista.
        """
        nombre = self.entry_nombre.get().strip()
        cuatrimestre_raw = self.entry_cuatrimestre.get().strip()
        anio_raw = self.entry_anio.get().strip()
        
        # Validación de campos obligatorios vacíos
        if not nombre or not cuatrimestre_raw or not anio_raw:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return
            
        # Validación de tipos
        try:
            int(cuatrimestre_raw)
        except ValueError:
            messagebox.showerror("Error de formato", "El cuatrimestre debe ser un número entero.")
            return
            
        try:
            int(anio_raw)
        except ValueError:
            messagebox.showerror("Error de formato", "El año debe ser un número entero.")
            return
            
        # Monkeypatching de input() para inyectar los datos en logica.agregar_materia sin pedir consola
        respuestas = [nombre, cuatrimestre_raw, anio_raw]
        def mock_input(*args, **kwargs):
            if respuestas:
                return respuestas.pop(0)
            return ""
            
        original_input = builtins.input
        builtins.input = mock_input
        
        try:
            agregar_materia(self.materias)
        finally:
            # Restaurar el input original siempre
            builtins.input = original_input
            
        # Limpiar campos y refrescar lista
        self.entry_nombre.delete(0, tk.END)
        self.entry_cuatrimestre.delete(0, tk.END)
        self.entry_anio.delete(0, tk.END)
        self.refrescar_lista()

    def manejador_agregar_nota(self):
        """
        Manejador para el evento del botón 'Agregar nota'. Valida la materia seleccionada,
        la nota, simula la entrada de consola para logica.py y actualiza la lista.
        """
        seleccion = self.listbox.curselection()
        
        # Validación de selección
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Seleccioná una materia de la lista para agregarle una nota.")
            return
            
        idx = seleccion[0]
        materia_seleccionada = self.materias[idx]
        nota_raw = self.entry_nota.get().strip()
        
        # Validación de campo vacío
        if not nota_raw:
            messagebox.showwarning("Campo vacío", "Debe ingresar una nota.")
            return
            
        # Validación del rango y formato de la nota (1 a 10)
        try:
            nota_filtrada = nota_raw.replace(",", ".")
            nota_val = float(nota_filtrada)
            if not (1 <= nota_val <= 10):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Nota inválida", "La nota debe ser un número válido entre 1 y 10.")
            return
            
        # Monkeypatching de input() para inyectar datos en logica.agregar_nota
        respuestas = [materia_seleccionada["nombre"], nota_raw]
        def mock_input(*args, **kwargs):
            if respuestas:
                return respuestas.pop(0)
            return ""
            
        original_input = builtins.input
        builtins.input = mock_input
        
        try:
            agregar_nota(self.materias)
        finally:
            # Restaurar el input original siempre
            builtins.input = original_input
            
        # Limpiar campo y refrescar lista
        self.entry_nota.delete(0, tk.END)
        self.refrescar_lista()


# Bloque de ejecución directa para pruebas individuales
if __name__ == "__main__":
    print("Ejecutando gui.py en modo independiente (standalone).")
    if not LOGICA_DISPONIBLE:
        print("[Aviso] logica.py no está disponible. Ejecutando con lógica de respaldo integrada.")
        
    # Datos de ejemplo iniciales para probar sin depender de datos persistentes
    datos_ejemplo = [
        {
            "nombre": "Análisis Matemático I",
            "cuatrimestre": 1,
            "año": 2025,
            "notas": [8, 7.5, 9]
        },
        {
            "nombre": "Álgebra Lineal",
            "cuatrimestre": 2,
            "año": 2025,
            "notas": [7, 8]
        },
        {
            "nombre": "Programacion Inicial",
            "cuatrimestre": 1,
            "año": 2026,
            "notas": []
        }
    ]
    
    root = tk.Tk()
    app = AcademicTrackerGUI(root, datos_ejemplo)
    
    # Manejo del cierre de ventana en pruebas
    def al_cerrar():
        print("Cerrando la aplicación independiente. Datos finales:")
        print(datos_ejemplo)
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", al_cerrar)
    root.mainloop()
