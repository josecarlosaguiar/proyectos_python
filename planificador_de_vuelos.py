import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3


# Función para crear la ventana del plan de vuelo
def crear_plan_de_vuelo_ventana():
    # Crear la ventana principal
    nueva_ruta_ventana = tk.Toplevel()  # Usamos Toplevel en lugar de Tk para evitar múltiples ventanas raíz
    nueva_ruta_ventana.title("Crear nuevo plan de vuelo")
    nueva_ruta_ventana.geometry("600x400")

    # Función interna para guardar la ruta
    def guardar_ruta():
        # Obtener los valores ingresados
        origen = entry_origen.get().strip()
        destino = entry_destino.get().strip()

        # Validar que los campos no estén vacíos
        if not origen or not destino:
            messagebox.showerror("Error", "Los campos de origen y destino no pueden estar vacíos")
            return

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('rutas.db')
            cursor = conn.cursor()

            # Insertar la nueva ruta
            cursor.execute("INSERT INTO rutas (origen, destino) VALUES (?, ?)", (origen, destino))

            # Obtener el ID de la ruta recién creada
            ruta_id = cursor.lastrowid

            # Guardar los cambios y cerrar la conexión
            conn.commit()
            conn.close()

            # Cerrar esta ventana
            nueva_ruta_ventana.destroy()

            # Abrir la ventana para agregar waypoints
            add_waypoints_window(ruta_id, origen, destino)

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo guardar la ruta: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    # Crear los elementos de la interfaz
    frame = ttk.Frame(nueva_ruta_ventana, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Crear etiqueta y campo para el origen
    ttk.Label(frame, text="Origen:", font=("Arial", 12)).pack(pady=5, anchor=tk.W)
    entry_origen = ttk.Entry(frame, width=40)
    entry_origen.pack(pady=5, fill=tk.X)

    # Crear etiqueta y campo para el destino
    ttk.Label(frame, text="Destino:", font=("Arial", 12)).pack(pady=5, anchor=tk.W)
    entry_destino = ttk.Entry(frame, width=40)
    entry_destino.pack(pady=5, fill=tk.X)

    # Añadir un botón para guardar
    btn_save = ttk.Button(
        frame,
        text="Crear nuevo plan de vuelo",
        command=guardar_ruta,
        style="Accent.TButton"  # Estilo personalizado para destacar el botón
    )
    btn_save.pack(pady=40)

    # Configurar un estilo personalizado para el botón
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 12, "bold"))


# Función para mostrar la lista de planes de vuelo y permitir cargarlos
def cargar_planes_de_vuelo_ventana():
    """
    Crea una ventana que muestra los planes de vuelo guardados y
    permite al usuario seleccionar uno para cargarlo
    """
    # Crear la ventana de carga
    ventana_carga = tk.Toplevel()
    ventana_carga.title("Cargar Plan de Vuelo")
    ventana_carga.geometry("800x500")

    # Marco principal
    frame = ttk.Frame(ventana_carga, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Etiqueta de instrucción
    ttk.Label(
        frame,
        text="Seleccione un plan de vuelo para cargar:",
        font=("Arial", 12, "bold")
    ).pack(pady=(0, 10), anchor=tk.W)

    # Crear un marco para contener el Treeview y la barra de desplazamiento
    tree_frame = ttk.Frame(frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Crear un Treeview para mostrar las rutas
    tree_columns = ("id", "origen", "destino")
    tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

    # Configurar las columnas
    tree.heading("id", text="ID")
    tree.heading("origen", text="Origen")
    tree.heading("destino", text="Destino")

    # Ajustar el ancho de las columnas
    tree.column("id", width=50, anchor=tk.CENTER)
    tree.column("origen", width=300, anchor=tk.W)
    tree.column("destino", width=300, anchor=tk.W)

    # Añadir barra de desplazamiento
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Colocar el Treeview y la barra de desplazamiento
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    # Función para cargar las rutas desde la base de datos al Treeview
    def cargar_rutas_en_treeview():
        # Limpiar el Treeview
        for item in tree.get_children():
            tree.delete(item)

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('rutas.db')
            cursor = conn.cursor()

            # Obtener todas las rutas
            cursor.execute("SELECT id, origen, destino FROM rutas ORDER BY id DESC")
            rutas = cursor.fetchall()

            # Cerrar la conexión
            conn.close()

            # Insertar las rutas en el Treeview
            for ruta in rutas:
                tree.insert("", "end", values=ruta)

            # Mostrar un mensaje si no hay rutas
            if not rutas:
                messagebox.showinfo("Información", "No hay planes de vuelo guardados")

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudieron cargar las rutas: {e}")

    # Función para visualizar la ruta seleccionada
    def visualizar_ruta_seleccionada():
        # Obtener el elemento seleccionado
        seleccion = tree.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un plan de vuelo")
            return

        # Obtener los valores del elemento seleccionado
        ruta_id = tree.item(seleccion[0], "values")[0]
        origen = tree.item(seleccion[0], "values")[1]
        destino = tree.item(seleccion[0], "values")[2]

        try:
            # Conectar a la base de datos para obtener los waypoints
            conn = sqlite3.connect('rutas.db')
            cursor = conn.cursor()

            # Obtener los waypoints de la ruta
            cursor.execute("SELECT waypoint FROM waypoints WHERE ruta_id = ? ORDER BY id", (ruta_id,))
            waypoints = [wp[0] for wp in cursor.fetchall()]

            # Cerrar la conexión
            conn.close()

            # Cerrar la ventana de carga
            ventana_carga.destroy()

            # Visualizar la ruta (esto dependerá de cómo quieras visualizarla)
            visualizar_plan_de_vuelo(ruta_id, origen, destino, waypoints)

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudieron cargar los waypoints: {e}")

    # Función para eliminar una ruta
    def eliminar_ruta_seleccionada():
        # Obtener el elemento seleccionado
        seleccion = tree.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un plan de vuelo")
            return

        # Confirmar la eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este plan de vuelo?"):
            return

        # Obtener el ID de la ruta
        ruta_id = tree.item(seleccion[0], "values")[0]

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('rutas.db')
            cursor = conn.cursor()

            # Eliminar los waypoints asociados a la ruta
            cursor.execute("DELETE FROM waypoints WHERE ruta_id = ?", (ruta_id,))

            # Eliminar la ruta
            cursor.execute("DELETE FROM rutas WHERE id = ?", (ruta_id,))

            # Guardar los cambios y cerrar la conexión
            conn.commit()
            conn.close()

            # Actualizar el Treeview
            cargar_rutas_en_treeview()

            messagebox.showinfo("Éxito", "Plan de vuelo eliminado correctamente")

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar el plan de vuelo: {e}")

    # Función para editar una ruta seleccionada
    def editar_ruta_seleccionada():
        # Obtener el elemento seleccionado
        seleccion = tree.selection()

        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un plan de vuelo")
            return

        # Obtener los valores del elemento seleccionado
        ruta_id = tree.item(seleccion[0], "values")[0]
        origen = tree.item(seleccion[0], "values")[1]
        destino = tree.item(seleccion[0], "values")[2]

        # Cerrar la ventana de carga
        ventana_carga.destroy()

        # Abrir la ventana para editar waypoints
        editar_waypoints_window(ruta_id, origen, destino)

    # Marco para los botones
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20, fill=tk.X)

    # Botón para visualizar la ruta
    ttk.Button(
        button_frame,
        text="Visualizar Plan",
        command=visualizar_ruta_seleccionada,
        style="Accent.TButton"
    ).pack(side=tk.LEFT, padx=(0, 10))

    # Botón para editar la ruta
    ttk.Button(
        button_frame,
        text="Editar Plan",
        command=editar_ruta_seleccionada
    ).pack(side=tk.LEFT, padx=(0, 10))

    # Botón para eliminar la ruta
    ttk.Button(
        button_frame,
        text="Eliminar Plan",
        command=eliminar_ruta_seleccionada
    ).pack(side=tk.LEFT)

    # Botón para refrescar la lista
    ttk.Button(
        button_frame,
        text="Refrescar Lista",
        command=cargar_rutas_en_treeview
    ).pack(side=tk.RIGHT)

    # Cargar las rutas al iniciar
    cargar_rutas_en_treeview()


# Función para agregar waypoints a una nueva ruta
def add_waypoints_window(ruta_id, origen, destino):
    """
    Abre una ventana para añadir waypoints a una ruta recién creada.

    Parámetros:
    ruta_id (int): ID de la ruta en la base de datos
    origen (str): Punto de origen de la ruta
    destino (str): Punto de destino de la ruta
    """
    # Crear la ventana para añadir waypoints
    ventana_waypoints = tk.Toplevel()
    ventana_waypoints.title(f"Añadir waypoints: {origen} → {destino}")
    ventana_waypoints.geometry("700x500")

    # Marco principal
    frame = ttk.Frame(ventana_waypoints, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Etiqueta de instrucción
    ttk.Label(
        frame,
        text=f"Añada waypoints para la ruta {origen} → {destino}:",
        font=("Arial", 12, "bold")
    ).pack(pady=(0, 10), anchor=tk.W)

    # Marco para la lista de waypoints
    list_frame = ttk.Frame(frame)
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # Crear un Listbox para los waypoints
    waypoints_listbox = tk.Listbox(list_frame, font=("Arial", 11), height=10)
    waypoints_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de desplazamiento para el Listbox
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=waypoints_listbox.yview)
    waypoints_listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Marco para los controles
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill=tk.X, pady=10)

    # Entrada para el nuevo waypoint
    ttk.Label(control_frame, text="Nuevo waypoint:").pack(side=tk.LEFT)
    entry_waypoint = ttk.Entry(control_frame, width=40)
    entry_waypoint.pack(side=tk.LEFT, padx=5)

    # Lista para almacenar los waypoints
    waypoints = []

    # Función para añadir un waypoint a la lista
    def agregar_waypoint():
        waypoint = entry_waypoint.get().strip()

        if not waypoint:
            messagebox.showwarning("Advertencia", "Por favor, introduzca un waypoint")
            return

        waypoints.append(waypoint)
        waypoints_listbox.insert(tk.END, waypoint)
        entry_waypoint.delete(0, tk.END)
        entry_waypoint.focus()

    # Función para eliminar un waypoint seleccionado
    def eliminar_waypoint():
        seleccionado = waypoints_listbox.curselection()

        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un waypoint para eliminar")
            return

        # Obtener el índice seleccionado
        indice = seleccionado[0]

        # Eliminar de la lista y del Listbox
        waypoints.pop(indice)
        waypoints_listbox.delete(indice)

    # Función para guardar todos los waypoints en la base de datos
    def guardar_waypoints():
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('rutas.db')
            cursor = conn.cursor()

            # Insertar cada waypoint
            for waypoint in waypoints:
                cursor.execute("INSERT INTO waypoints (ruta_id, waypoint) VALUES (?, ?)",
                               (ruta_id, waypoint))

            # Guardar los cambios y cerrar la conexión
            conn.commit()
            conn.close()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Se han guardado {len(waypoints)} waypoints para la ruta")

            # Cerrar la ventana
            ventana_waypoints.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudieron guardar los waypoints: {e}")

    # Botones para agregar y eliminar waypoints
    ttk.Button(control_frame, text="Añadir", command=agregar_waypoint).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="Eliminar", command=eliminar_waypoint).pack(side=tk.LEFT, padx=5)

    # Marco para los botones de acción
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20, fill=tk.X)

    # Botones para guardar o cancelar
    ttk.Button(
        button_frame,
        text="Guardar Waypoints",
        command=guardar_waypoints,
        style="Accent.TButton"
    ).pack(side=tk.RIGHT, padx=5)

    ttk.Button(
        button_frame,
        text="Cancelar",
        command=ventana_waypoints.destroy
    ).pack(side=tk.RIGHT, padx=5)

    # Configurar un acceso rápido para agregar waypoints con Enter
    entry_waypoint.bind("<Return>", lambda event: agregar_waypoint())

    # Dar foco a la entrada de waypoint
    entry_waypoint.focus()


# Nueva función para editar waypoints de un plan existente
def editar_waypoints_window(ruta_id, origen, destino):
    """
    Abre una ventana para editar los waypoints de una ruta existente.

    Parámetros:
    ruta_id (int): ID de la ruta en la base de datos
    origen (str): Punto de origen de la ruta
    destino (str): Punto de destino de la ruta
    """
    # Crear la ventana para editar waypoints
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title(f"Editar Plan de Vuelo #{ruta_id}: {origen} → {destino}")
    ventana_edicion.geometry("700x500")

    # Marco principal
    frame = ttk.Frame(ventana_edicion, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Etiqueta de título
    ttk.Label(
        frame,
        text=f"Editar waypoints del plan de vuelo #{ruta_id}",
        font=("Arial", 14, "bold")
    ).pack(pady=(0, 20))

    # Información de la ruta
    info_frame = ttk.LabelFrame(frame, text="Detalles del Plan", padding="10")
    info_frame.pack(fill=tk.X, pady=10)

    ttk.Label(info_frame, text=f"Origen: {origen}", font=("Arial", 11)).pack(anchor=tk.W, pady=2)
    ttk.Label(info_frame, text=f"Destino: {destino}", font=("Arial", 11)).pack(anchor=tk.W, pady=2)

    # Marco para la lista de waypoints
    list_frame = ttk.LabelFrame(frame, text="Waypoints", padding="10")
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # Crear un Listbox para los waypoints
    waypoints_listbox = tk.Listbox(list_frame, font=("Arial", 11), height=10)
    waypoints_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de desplazamiento para el Listbox
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=waypoints_listbox.yview)
    waypoints_listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Lista para almacenar los waypoints
    waypoints = []

    # Cargar los waypoints existentes
    try:
        conn = sqlite3.connect('rutas.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, waypoint FROM waypoints WHERE ruta_id = ? ORDER BY id", (ruta_id,))
        waypoints_db = cursor.fetchall()

        conn.close()

        # Llenar la lista y el Listbox
        for wp_id, wp in waypoints_db:
            waypoints.append((wp_id, wp))
            waypoints_listbox.insert(tk.END, wp)

    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"No se pudieron cargar los waypoints: {e}")

    # Marco para los controles
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill=tk.X, pady=10)

    # Entrada para el nuevo waypoint
    ttk.Label(control_frame, text="Nuevo waypoint:").pack(side=tk.LEFT)
    entry_waypoint = ttk.Entry(control_frame, width=40)
    entry_waypoint.pack(side=tk.LEFT, padx=5)

    # Función para añadir un waypoint a la lista
    def agregar_waypoint():
        waypoint = entry_waypoint.get().strip()

        if not waypoint:
            messagebox.showwarning("Advertencia", "Por favor, introduzca un waypoint")
            return

        try:
            # Guardar inmediatamente en la base de datos
            conn = sqlite3.connect('rutas.db')
            cursor = conn.cursor()

            cursor.execute("INSERT INTO waypoints (ruta_id, waypoint) VALUES (?, ?)",
                           (ruta_id, waypoint))

            # Obtener el ID generado
            wp_id = cursor.lastrowid

            conn.commit()
            conn.close()

            # Añadir a la lista y al Listbox
            waypoints.append((wp_id, waypoint))
            waypoints_listbox.insert(tk.END, waypoint)

            entry_waypoint.delete(0, tk.END)
            entry_waypoint.focus()

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo guardar el waypoint: {e}")

    # Función para eliminar un waypoint seleccionado
    def eliminar_waypoint():
        seleccionado = waypoints_listbox.curselection()

        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un waypoint para eliminar")
            return

        # Obtener el índice seleccionado
        indice = seleccionado[0]

        # Obtener el ID del waypoint
        wp_id, _ = waypoints[indice]

        try:
            # Eliminar de la base de datos
            conn = sqlite3.connect('rutas.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM waypoints WHERE id = ?", (wp_id,))

            conn.commit()
            conn.close()

            # Eliminar de la lista y del Listbox
            waypoints.pop(indice)
            waypoints_listbox.delete(indice)

        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar el waypoint: {e}")

    # Función para editar un waypoint seleccionado
    def editar_waypoint():
        seleccionado = waypoints_listbox.curselection()

        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un waypoint para editar")
            return

        # Obtener el índice seleccionado
        indice = seleccionado[0]

        # Obtener el ID y el waypoint actual
        wp_id, wp_actual = waypoints[indice]

        # Pedir el nuevo valor
        nuevo_wp = simpledialog.askstring("Editar Waypoint", "Nuevo valor del waypoint:", initialvalue=wp_actual)

        if nuevo_wp and nuevo_wp.strip():
            try:
                # Actualizar en la base de datos
                conn = sqlite3.connect('rutas.db')
                cursor = conn.cursor()

                cursor.execute("UPDATE waypoints SET waypoint = ? WHERE id = ?", (nuevo_wp, wp_id))

                conn.commit()
                conn.close()

                # Actualizar en la lista y en el Listbox
                waypoints[indice] = (wp_id, nuevo_wp)
                waypoints_listbox.delete(indice)
                waypoints_listbox.insert(indice, nuevo_wp)

            except sqlite3.Error as e:
                messagebox.showerror("Error de base de datos", f"No se pudo actualizar el waypoint: {e}")

    # Botones para agregar, eliminar y editar waypoints
    ttk.Button(control_frame, text="Añadir", command=agregar_waypoint).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="Eliminar", command=eliminar_waypoint).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="Editar", command=editar_waypoint).pack(side=tk.LEFT, padx=5)

    # Marco para los botones de acción
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20, fill=tk.X)

    # Botón para visualizar el plan completo
    ttk.Button(
        button_frame,
        text="Visualizar Plan Completo",
        command=lambda: visualizar_plan_desde_edicion(ruta_id, origen, destino, ventana_edicion)
    ).pack(side=tk.LEFT)

    # Botón para cerrar
    ttk.Button(
        button_frame,
        text="Cerrar",
        command=ventana_edicion.destroy,
        style="Accent.TButton"
    ).pack(side=tk.RIGHT)

    # Configurar un acceso rápido para agregar waypoints con Enter
    entry_waypoint.bind("<Return>", lambda event: agregar_waypoint())

    # Dar foco a la entrada de waypoint
    entry_waypoint.focus()


# Función auxiliar para visualizar el plan desde la ventana de edición
def visualizar_plan_desde_edicion(ruta_id, origen, destino, ventana_edicion):
    """
    Visualiza el plan de vuelo completo desde la ventana de edición.

    Parámetros:
    ruta_id (int): ID de la ruta en la base de datos
    origen (str): Punto de origen de la ruta
    destino (str): Punto de destino de la ruta
    ventana_edicion (tk.Toplevel): Ventana de edición a cerrar
    """
    try:
        # Obtener los waypoints actualizados
        conn = sqlite3.connect('rutas.db')
        cursor = conn.cursor()

        cursor.execute("SELECT waypoint FROM waypoints WHERE ruta_id = ? ORDER BY id", (ruta_id,))
        waypoints = [wp[0] for wp in cursor.fetchall()]

        conn.close()

        # Cerrar la ventana de edición
        ventana_edicion.destroy()

        # Visualizar el plan
        visualizar_plan_de_vuelo(ruta_id, origen, destino, waypoints)

    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"No se pudieron cargar los waypoints: {e}")


# Función para visualizar un plan de vuelo completo
def visualizar_plan_de_vuelo(ruta_id, origen, destino, waypoints):
    """
    Visualiza un plan de vuelo completo con su ruta y waypoints.

    Parámetros:
    ruta_id (int): ID de la ruta en la base de datos
    origen (str): Punto de origen de la ruta
    destino (str): Punto de destino de la ruta
    waypoints (list): Lista de waypoints de la ruta
    """
    # Crear una ventana para visualizar el plan de vuelo
    ventana_visualizacion = tk.Toplevel()
    ventana_visualizacion.title(f"Plan de Vuelo: {origen} → {destino}")
    ventana_visualizacion.geometry("800x600")

    # Icono de avión para la ventana (si está disponible)
    try:
        ventana_visualizacion.iconbitmap("avion.ico")  # Puedes reemplazar esto con tu propio icono
    except:
        pass  # Si no encuentra el icono, simplemente lo ignora

    # Marco principal
    frame = ttk.Frame(ventana_visualizacion, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Título del plan de vuelo
    ttk.Label(
        frame,
        text=f"Plan de Vuelo #{ruta_id}: {origen} → {destino}",
        font=("Arial", 16, "bold")
    ).pack(pady=(0, 20))

    # Marco para la información detallada
    info_frame = ttk.LabelFrame(frame, text="Detalles del Plan", padding="10")
    info_frame.pack(fill=tk.X, pady=10)

    # Información básica
    ttk.Label(info_frame, text=f"Origen: {origen}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
    ttk.Label(info_frame, text=f"Destino: {destino}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
    ttk.Label(info_frame, text=f"Número de waypoints: {len(waypoints)}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)

    # Marco para la lista de waypoints
    waypoints_frame = ttk.LabelFrame(frame, text="Waypoints", padding="10")
    waypoints_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # Si hay waypoints, mostrarlos
    if waypoints:
        # Crear un Treeview para los waypoints
        waypoints_tree = ttk.Treeview(waypoints_frame, columns=("num", "waypoint"), show="headings")
        waypoints_tree.heading("num", text="#")
        waypoints_tree.heading("waypoint", text="Waypoint")

        waypoints_tree.column("num", width=50, anchor=tk.CENTER)
        waypoints_tree.column("waypoint", width=700, anchor=tk.W)

        # Añadir barra de desplazamiento
        waypoints_scrollbar = ttk.Scrollbar(waypoints_frame, orient="vertical", command=waypoints_tree.yview)
        waypoints_tree.configure(yscrollcommand=waypoints_scrollbar.set)

        # Colocar el Treeview y la barra de desplazamiento
        waypoints_tree.pack(side="left", fill=tk.BOTH, expand=True)
        waypoints_scrollbar.pack(side="right", fill="y")

        # Insertar los waypoints
        for i, wp in enumerate(waypoints, 1):
            waypoints_tree.insert("", "end", values=(i, wp))
    else:
        ttk.Label(
            waypoints_frame,
            text="No hay waypoints definidos para este plan de vuelo",
            font=("Arial", 12, "italic")
        ).pack(pady=20)

    # Botones de acción
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20, fill=tk.X)

    # Botón para editar el plan
    ttk.Button(
        button_frame,
        text="Editar Plan",
        command=lambda: [ventana_visualizacion.destroy(), editar_waypoints_window(ruta_id, origen, destino)]
    ).pack(side=tk.LEFT)

    # Botón para cerrar
    ttk.Button(
        button_frame,
        text="Cerrar",
        command=ventana_visualizacion.destroy
    ).pack(side=tk.RIGHT)


# Esta función inicializa la base de datos si no existe
def create_database():
    """
    Crea las tablas necesarias en la base de datos si no existen.
    """
    try:
        conn = sqlite3.connect('rutas.db')
        cursor = conn.cursor()

        # Crear tabla de rutas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rutas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origen TEXT NOT NULL,
                destino TEXT NOT NULL
            )
        ''')

        # Crear tabla de waypoints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS waypoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ruta_id INTEGER NOT NULL,
                waypoint TEXT NOT NULL,
                FOREIGN KEY (ruta_id) REFERENCES rutas (id)
            )
        ''')

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")


# Ejemplo de cómo usar estas funciones
if __name__ == "__main__":
    # Inicializar la base de datos
    create_database()

    # Crear la ventana principal de la aplicación
    root = tk.Tk()
    root.title("Planificador de Vuelos")
    root.geometry("800x600")

    # Marco principal
    main_frame = ttk.Frame(root, padding="40")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Título de la aplicación
    ttk.Label(
        main_frame,
        text="Sistema de Planificación de Vuelos",
        font=("Arial", 18, "bold")
    ).pack(pady=(0, 30))

    # Marco para los botones
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(pady=20)

    # Estilo para botones grandes
    style = ttk.Style()
    style.configure("Large.TButton", font=("Arial", 14), padding=10)

    # Botón para crear nuevo plan de vuelo
    ttk.Button(
        buttons_frame,
        text="Crear Nuevo Plan de Vuelo",
        command=crear_plan_de_vuelo_ventana,
        style="Large.TButton"
    ).pack(pady=10, padx=20, fill=tk.X)

    # Botón para cargar planes de vuelo
    ttk.Button(
        buttons_frame,
        text="Cargar Planes de Vuelo",
        command=cargar_planes_de_vuelo_ventana,
        style="Large.TButton"
    ).pack(pady=10, padx=20, fill=tk.X)

    # Iniciar el bucle principal
    root.mainloop()