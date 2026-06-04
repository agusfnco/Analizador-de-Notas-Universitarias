# -*- coding: utf-8 -*-
"""
Interfaz Gráfica de Usuario (gui.py)
------------------------------------
Implementa la interfaz visual usando tkinter para el Sistema de Seguimiento Académico.
Utiliza logica.py para realizar las operaciones y main.py como punto de entrada.
Soporta ejecución directa con datos de ejemplo en caso de que logica.py no esté disponible.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import builtins
import estadisticas

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
    def __init__(self, root, materias, guardar_callback=None):
        """
        Inicializa la ventana principal de la interfaz gráfica.
        
        Parámetros:
        - root (tk.Tk): Instancia de la ventana principal de Tkinter.
        - materias (list): Lista de diccionarios con la información académica.
        - guardar_callback (callable, opcional): Función de retorno para auto-guardar cambios.
        """
        self.root = root
        self.materias = materias
        self.guardar_callback = guardar_callback
        
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
        self.root.grid_rowconfigure(1, weight=0)
        
        # Crear los paneles
        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_panel_inferior()
        
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
        btn_agregar_materia.pack(fill="x", pady=(0, 5))

        # Sub-fila: Modificar y Eliminar materia (en paralelo)
        fila_abm_materia = tk.Frame(self.left_frame, bg="#ffffff")
        fila_abm_materia.pack(fill="x", pady=(0, 15))
        fila_abm_materia.grid_columnconfigure(0, weight=1, uniform="abm_m")
        fila_abm_materia.grid_columnconfigure(1, weight=1, uniform="abm_m")

        btn_mod_materia = self.crear_boton_naranja(
            fila_abm_materia,
            text="Modificar",
            command=self.manejador_modificar_materia
        )
        btn_mod_materia.grid(row=0, column=0, padx=(0, 3), sticky="ew")

        btn_del_materia = self.crear_boton_rojo(
            fila_abm_materia,
            text="Eliminar",
            command=self.manejador_eliminar_materia
        )
        btn_del_materia.grid(row=0, column=1, padx=(3, 0), sticky="ew")

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
        self.entry_nota.pack(fill="x", pady=(0, 5))

        # Botón Agregar Nota
        btn_agregar_nota = self.crear_boton_estilizado(
            self.left_frame,
            text="Agregar nota",
            command=self.manejador_agregar_nota
        )
        btn_agregar_nota.pack(fill="x", pady=(0, 5))

        # Sub-fila: Modificar y Eliminar nota (en paralelo)
        fila_abm_nota = tk.Frame(self.left_frame, bg="#ffffff")
        fila_abm_nota.pack(fill="x")
        fila_abm_nota.grid_columnconfigure(0, weight=1, uniform="abm_n")
        fila_abm_nota.grid_columnconfigure(1, weight=1, uniform="abm_n")

        btn_mod_nota = self.crear_boton_naranja(
            fila_abm_nota,
            text="Modificar nota",
            command=self.manejador_modificar_nota
        )
        btn_mod_nota.grid(row=0, column=0, padx=(0, 3), sticky="ew")

        btn_del_nota = self.crear_boton_rojo(
            fila_abm_nota,
            text="Eliminar nota",
            command=self.manejador_eliminar_nota
        )
        btn_del_nota.grid(row=0, column=1, padx=(3, 0), sticky="ew")

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

    def crear_boton_rojo(self, parent, text, command):
        """
        Crea un botón estilizado rojo (#e74c3c) para acciones de eliminación (Baja).
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg="#e74c3c",
            fg="#ffffff",
            activebackground="#c0392b",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=8,
            pady=5
        )

        def on_enter(e): btn.config(bg="#c0392b")
        def on_leave(e): btn.config(bg="#e74c3c")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def crear_boton_naranja(self, parent, text, command):
        """
        Crea un botón estilizado naranja (#e67e22) para acciones de modificación.
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg="#e67e22",
            fg="#ffffff",
            activebackground="#ca6f1e",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=8,
            pady=5
        )

        def on_enter(e): btn.config(bg="#ca6f1e")
        def on_leave(e): btn.config(bg="#e67e22")
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
            if self.guardar_callback:
                self.guardar_callback()
        finally:
            # Restaurar el input original siempre
            builtins.input = original_input
            
        # Limpiar campos y refrescar lista
        self.entry_nombre.delete(0, tk.END)
        self.entry_cuatrimestre.delete(0, tk.END)
        self.entry_anio.delete(0, tk.END)
        self.refrescar_lista()

    def manejador_eliminar_materia(self):
        """
        Baja de materia: pide confirmación y elimina la materia seleccionada
        con todas sus notas. Guarda automáticamente.
        """
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Seleccioná una materia de la lista para eliminarla.")
            return

        idx = seleccion[0]
        materia = self.materias[idx]
        confirmado = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que querés eliminar '{materia['nombre']}' y todas sus notas?\n\nEsta acción no se puede deshacer."
        )
        if not confirmado:
            return

        # Eliminar la materia de la lista en memoria
        del self.materias[idx]

        # Auto-guardar y refrescar
        if self.guardar_callback:
            self.guardar_callback()
        self.refrescar_lista()
        messagebox.showinfo("Eliminación exitosa", f"La materia '{materia['nombre']}' fue eliminada correctamente.")

    def manejador_modificar_materia(self):
        """
        Modificación de materia: abre una ventana Toplevel modal con los
        datos actuales pre-cargados. Al confirmar, actualiza la lista y guarda.
        """
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Seleccioná una materia de la lista para modificarla.")
            return

        idx = seleccion[0]
        materia = self.materias[idx]

        # Crear ventana modal
        top = tk.Toplevel(self.root)
        top.title("Modificar Materia")
        top.geometry("360x280")
        top.configure(bg="#ffffff")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()  # Modal: bloquea la ventana padre mientras está abierta

        frame = tk.Frame(top, bg="#ffffff", padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Modificar Materia", font=("Segoe UI", 12, "bold"), fg="#2c3e50", bg="#ffffff").pack(anchor="w", pady=(0, 15))

        # Campo Nombre pre-llenado
        tk.Label(frame, text="Nombre:", font=self.font_main, bg="#ffffff", fg="#333333").pack(anchor="w")
        entry_mod_nombre = self.crear_entry_estilizado(frame)
        entry_mod_nombre.insert(0, materia["nombre"])
        entry_mod_nombre.pack(fill="x", pady=(0, 8))

        # Campo Cuatrimestre pre-llenado
        tk.Label(frame, text="Cuatrimestre:", font=self.font_main, bg="#ffffff", fg="#333333").pack(anchor="w")
        entry_mod_cuat = self.crear_entry_estilizado(frame)
        entry_mod_cuat.insert(0, str(materia.get("cuatrimestre", "")))
        entry_mod_cuat.pack(fill="x", pady=(0, 8))

        # Campo Año pre-llenado
        tk.Label(frame, text="Año:", font=self.font_main, bg="#ffffff", fg="#333333").pack(anchor="w")
        entry_mod_anio = self.crear_entry_estilizado(frame)
        entry_mod_anio.insert(0, str(materia.get("año", "")))
        entry_mod_anio.pack(fill="x", pady=(0, 15))

        def confirmar_modificacion():
            nuevo_nombre = entry_mod_nombre.get().strip()
            nuevo_cuat_raw = entry_mod_cuat.get().strip()
            nuevo_anio_raw = entry_mod_anio.get().strip()

            # Validaciones
            if not nuevo_nombre or not nuevo_cuat_raw or not nuevo_anio_raw:
                messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.", parent=top)
                return
            try:
                nuevo_cuat = int(nuevo_cuat_raw)
            except ValueError:
                messagebox.showerror("Error de formato", "El cuatrimestre debe ser un número entero.", parent=top)
                return
            try:
                nuevo_anio = int(nuevo_anio_raw)
            except ValueError:
                messagebox.showerror("Error de formato", "El año debe ser un número entero.", parent=top)
                return

            # Aplicar los cambios al diccionario en memoria
            materia["nombre"] = nuevo_nombre
            materia["cuatrimestre"] = nuevo_cuat
            materia["año"] = nuevo_anio

            # Auto-guardar y refrescar
            if self.guardar_callback:
                self.guardar_callback()
            self.refrescar_lista()
            top.destroy()

        # Fila de botones Confirmar / Cancelar
        fila_btns = tk.Frame(frame, bg="#ffffff")
        fila_btns.pack(fill="x")
        self.crear_boton_estilizado(fila_btns, text="Confirmar", command=confirmar_modificacion).pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.crear_boton_rojo(fila_btns, text="Cancelar", command=top.destroy).pack(side="left", expand=True, fill="x", padx=(4, 0))

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
            if self.guardar_callback:
                self.guardar_callback()
        finally:
            # Restaurar el input original siempre
            builtins.input = original_input
            
        # Limpiar campo y refrescar lista
        self.entry_nota.delete(0, tk.END)
        self.refrescar_lista()

    def _abrir_selector_notas(self, titulo, texto_boton, callback_accion):
        """
        Abre una ventana Toplevel con un Listbox de las notas de la materia
        seleccionada. Llama a callback_accion(top, idx_materia, idx_nota)
        cuando el usuario confirma. Uso compartido por Eliminar y Modificar nota.
        """
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Seleccioná una materia de la lista primero.")
            return None

        idx_materia = seleccion[0]
        materia = self.materias[idx_materia]
        notas = materia.get("notas", [])

        if not notas:
            messagebox.showwarning("Sin notas", f"'{materia['nombre']}' no tiene notas registradas.")
            return None

        top = tk.Toplevel(self.root)
        top.title(titulo)
        top.geometry("320x300")
        top.configure(bg="#ffffff")
        top.resizable(False, False)
        top.transient(self.root)
        top.grab_set()

        frame = tk.Frame(top, bg="#ffffff", padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Materia: {materia['nombre']}", font=self.font_bold, fg="#2c3e50", bg="#ffffff").pack(anchor="w", pady=(0, 8))
        tk.Label(frame, text="Seleccioná una nota:", font=self.font_main, bg="#ffffff", fg="#333333").pack(anchor="w")

        # Listbox de notas numeradas
        lb_notas = tk.Listbox(
            frame,
            font=self.font_main,
            bg="#f9f9f9",
            fg="#333333",
            selectbackground="#4a90d9",
            selectforeground="#ffffff",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#dcdcdc",
            activestyle="none",
            height=6
        )
        for i, n in enumerate(notas, start=1):
            lb_notas.insert(tk.END, f"{i}. {n}")
        lb_notas.pack(fill="both", expand=True, pady=(4, 12))

        def on_accion():
            sel_nota = lb_notas.curselection()
            if not sel_nota:
                messagebox.showwarning("Sin selección", "Seleccioná una nota de la lista.", parent=top)
                return
            callback_accion(top, idx_materia, sel_nota[0], lb_notas)

        fila_btns = tk.Frame(frame, bg="#ffffff")
        fila_btns.pack(fill="x")
        accion_btn = tk.Button(
            fila_btns, text=texto_boton,
            command=on_accion,
            font=("Segoe UI", 9, "bold"),
            bg="#4a90d9" if "Modificar" in texto_boton else "#e74c3c",
            fg="#ffffff", relief="flat", bd=0, cursor="hand2", padx=8, pady=5
        )
        accion_btn.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.crear_boton_rojo(fila_btns, text="Cancelar", command=top.destroy).pack(side="left", expand=True, fill="x", padx=(4, 0))

        return top

    def manejador_eliminar_nota(self):
        """
        Baja de nota: muestra las notas de la materia seleccionada y,
        tras confirmación, elimina la nota elegida. Guarda automáticamente.
        """
        def hacer_baja(top, idx_materia, idx_nota, lb_notas):
            materia = self.materias[idx_materia]
            nota_valor = materia["notas"][idx_nota]
            confirmado = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Eliminar la nota {nota_valor} de '{materia['nombre']}'?",
                parent=top
            )
            if not confirmado:
                return
            del materia["notas"][idx_nota]
            if self.guardar_callback:
                self.guardar_callback()
            self.refrescar_lista()
            top.destroy()

        self._abrir_selector_notas("Eliminar Nota", "Eliminar nota", hacer_baja)

    def manejador_modificar_nota(self):
        """
        Modificación de nota: muestra las notas de la materia seleccionada,
        pre-llena el nuevo valor y actualiza al confirmar. Guarda automáticamente.
        """
        def hacer_modificacion(top, idx_materia, idx_nota, lb_notas):
            materia = self.materias[idx_materia]
            valor_actual = materia["notas"][idx_nota]

            # Ventana secundaria sobre el selector para ingresar el nuevo valor
            top2 = tk.Toplevel(top)
            top2.title("Nueva nota")
            top2.geometry("280x160")
            top2.configure(bg="#ffffff")
            top2.resizable(False, False)
            top2.transient(top)
            top2.grab_set()

            f2 = tk.Frame(top2, bg="#ffffff", padx=16, pady=16)
            f2.pack(fill="both", expand=True)

            tk.Label(f2, text=f"Valor actual: {valor_actual}", font=self.font_bold, bg="#ffffff", fg="#7f8c8d").pack(anchor="w", pady=(0, 8))
            tk.Label(f2, text="Nueva nota (1-10):", font=self.font_main, bg="#ffffff", fg="#333333").pack(anchor="w")
            entry_nueva_nota = self.crear_entry_estilizado(f2)
            entry_nueva_nota.insert(0, str(valor_actual))
            entry_nueva_nota.pack(fill="x", pady=(4, 12))

            def confirmar_nueva_nota():
                raw = entry_nueva_nota.get().strip()
                if not raw:
                    messagebox.showwarning("Campo vacío", "Ingresá un valor para la nota.", parent=top2)
                    return
                try:
                    nueva = float(raw.replace(",", "."))
                    if not (1 <= nueva <= 10):
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Nota inválida", "La nota debe ser un número entre 1 y 10.", parent=top2)
                    return
                # Convertir a entero si es un decimal .0
                if nueva == int(nueva):
                    nueva = int(nueva)
                materia["notas"][idx_nota] = nueva
                if self.guardar_callback:
                    self.guardar_callback()
                self.refrescar_lista()
                top2.destroy()
                top.destroy()

            fila_btns2 = tk.Frame(f2, bg="#ffffff")
            fila_btns2.pack(fill="x")
            self.crear_boton_estilizado(fila_btns2, text="Confirmar", command=confirmar_nueva_nota).pack(side="left", expand=True, fill="x", padx=(0, 4))
            self.crear_boton_rojo(fila_btns2, text="Cancelar", command=top2.destroy).pack(side="left", expand=True, fill="x", padx=(4, 0))

        self._abrir_selector_notas("Modificar Nota", "Modificar nota", hacer_modificacion)

    def crear_panel_inferior(self):
        """
        Crea el panel inferior con los botones para las estadísticas, gráficos y exportaciones.
        """
        self.bottom_frame = tk.Frame(
            self.root, 
            bg="#ffffff", 
            padx=12, 
            pady=12,
            highlightbackground="#e0e0e0", 
            highlightthickness=1,
            bd=0
        )
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))
        
        # Configurar 5 columnas con pesos uniformes para que los botones tengan la misma anchura
        for col_idx in range(5):
            self.bottom_frame.grid_columnconfigure(col_idx, weight=1, uniform="bottom_group")
            
        # Botón 1: Ver promedios
        self.btn_promedios = self.crear_boton_verde(
            self.bottom_frame,
            text="Ver promedios",
            command=self.mostrar_grafico_promedios
        )
        self.btn_promedios.grid(row=0, column=0, padx=4, sticky="ew")
        
        # Botón 2: Distribución de notas
        self.btn_distribucion = self.crear_boton_verde(
            self.bottom_frame,
            text="Distribución notas",
            command=self.mostrar_grafico_distribucion
        )
        self.btn_distribucion.grid(row=0, column=1, padx=4, sticky="ew")
        
        # Botón 3: Ver estadísticas
        self.btn_stats = self.crear_boton_verde(
            self.bottom_frame,
            text="Ver estadísticas",
            command=self.mostrar_estadisticas
        )
        self.btn_stats.grid(row=0, column=2, padx=4, sticky="ew")
        
        # Botón 4: Exportar CSV
        self.btn_csv = self.crear_boton_verde(
            self.bottom_frame,
            text="Exportar CSV",
            command=self.exportar_a_csv
        )
        self.btn_csv.grid(row=0, column=3, padx=4, sticky="ew")
        
        # Botón 5: Exportar PDF
        self.btn_pdf = self.crear_boton_verde(
            self.bottom_frame,
            text="Exportar PDF",
            command=self.exportar_a_pdf
        )
        self.btn_pdf.grid(row=0, column=4, padx=4, sticky="ew")

    def crear_boton_verde(self, parent, text, command):
        """
        Crea un botón estilizado verde (#5cb85c) con animaciones de hover.
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg="#5cb85c",
            fg="#ffffff",
            activebackground="#4cae4c",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=6
        )
        
        def on_enter(e):
            btn.config(bg="#4cae4c")
            
        def on_leave(e):
            btn.config(bg="#5cb85c")
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def mostrar_grafico_promedios(self):
        """
        Invoca la función de graficación de promedios individuales.
        """
        estadisticas.graficar_promedios(self.materias, self.root)

    def mostrar_grafico_distribucion(self):
        """
        Invoca la función de graficación de la distribución de notas de la carrera.
        """
        estadisticas.graficar_distribucion(self.materias, self.root)

    def mostrar_estadisticas(self):
        """
        Calcula las estadísticas descriptivas y abre una ventana secundaria Toplevel
        para mostrarlas de forma tabulada y muy legible.
        """
        stats = estadisticas.calcular_stats(self.materias)
        
        top = tk.Toplevel(self.root)
        top.title("Estadísticas Generales de Carrera")
        top.geometry("380x320")
        top.configure(bg="#ffffff")
        top.resizable(False, False)
        top.transient(self.root)
        
        frame_stats = tk.Frame(top, bg="#ffffff", padx=20, pady=20)
        frame_stats.pack(fill="both", expand=True)
        
        lbl_titulo_stats = tk.Label(
            frame_stats, 
            text="Estadísticas Académicas", 
            font=("Segoe UI", 12, "bold"), 
            fg="#2c3e50", 
            bg="#ffffff"
        )
        lbl_titulo_stats.pack(anchor="w", pady=(0, 15))
        
        stats_text = (
            f"• Promedio General:  {stats['promedio_general']:.2f}\n\n"
            f"• Nota Máxima:  {stats['nota_maxima']}\n"
            f"• Nota Mínima:  {stats['nota_minima']}\n"
            f"• Desvío Estándar:  {stats['desvio_estandar']:.2f}\n\n"
            f"• Mejor Materia:  {stats['mejor_materia'] or 'N/A'}\n\n"
            f"• Materias Aprobadas (Prom >= 6):  {stats['aprobadas']}\n"
            f"• Materias En Curso:  {stats['desaprobadas']}\n\n"
            f"• Total de Materias:  {stats['total_materias']}\n"
            f"• Total de Notas Registradas:  {stats['total_notas']}"
        )
        
        lbl_info = tk.Label(
            frame_stats,
            text=stats_text,
            font=("Segoe UI", 10),
            fg="#333333",
            bg="#ffffff",
            justify="left",
            anchor="w"
        )
        lbl_info.pack(fill="both", expand=True)
        
        btn_cerrar = tk.Button(
            frame_stats, 
            text="Cerrar", 
            command=top.destroy,
            font=("Segoe UI", 10, "bold"), 
            bg="#4a90d9", 
            fg="#ffffff", 
            activebackground="#357abd", 
            activeforeground="#ffffff", 
            relief="flat", 
            bd=0, 
            cursor="hand2", 
            padx=15, 
            pady=6
        )
        
        def on_enter(e): btn_cerrar.config(bg="#357abd")
        def on_leave(e): btn_cerrar.config(bg="#4a90d9")
        btn_cerrar.bind("<Enter>", on_enter)
        btn_cerrar.bind("<Leave>", on_leave)
        btn_cerrar.pack(anchor="e", pady=(10, 0))

    def exportar_a_csv(self):
        """
        Muestra el cuadro de diálogo para guardar el archivo y llama a exportar_csv().
        """
        if not self.materias:
            messagebox.showwarning("Sin datos", "No hay materias registradas para exportar.")
            return
            
        ruta = filedialog.asksaveasfilename(
            parent=self.root,
            title="Exportar a CSV",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        
        if not ruta:
            return  # Cancelado por el usuario
            
        exito = estadisticas.exportar_csv(self.materias, ruta)
        if exito:
            messagebox.showinfo("Exportación exitosa", f"Los datos han sido exportados correctamente a CSV en:\n{ruta}")
        else:
            messagebox.showerror("Error de exportación", "Ocurrió un error al intentar guardar el archivo CSV.")

    def exportar_a_pdf(self):
        """
        Muestra el cuadro de diálogo para guardar el archivo y llama a exportar_pdf().
        """
        if not self.materias:
            messagebox.showwarning("Sin datos", "No hay materias registradas para exportar.")
            return
            
        ruta = filedialog.asksaveasfilename(
            parent=self.root,
            title="Exportar a PDF",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if not ruta:
            return  # Cancelado por el usuario
            
        exito = estadisticas.exportar_pdf(self.materias, ruta)
        if exito:
            messagebox.showinfo("Exportación exitosa", f"El reporte académico ha sido exportado correctamente a PDF en:\n{ruta}")
        else:
            messagebox.showerror("Error de exportación", "Ocurrió un error al intentar generar el archivo PDF.")


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
