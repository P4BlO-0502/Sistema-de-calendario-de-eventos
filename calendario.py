import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

class CalendarioEventos:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendario de Eventos")
        
        self.eventos = self.cargar_eventos()
        
        self.label = tk.Label(root, text="Eventos:", font=("Helvetica", 14))
        self.label.pack(pady=10)
        
        self.lista_eventos = tk.Listbox(root, width=50, height=10)
        self.lista_eventos.pack(pady=10)

        self.boton_estilo = {
            'width': 20,
            'height': 2,
            'bg': 'white',
            'fg': 'black',
            'font': ('Helvetica', 12),
            'activebackground': '#f0f0f0',
            'activeforeground': 'black',
            'borderwidth': 2,
            'relief': 'solid',
        }

        self.boton_agregar = tk.Button(root, text="Agregar Evento", command=self.agregar_evento, **self.boton_estilo)
        self.boton_agregar.pack(pady=5)

        self.boton_editar = tk.Button(root, text="Editar Evento", command=self.editar_evento, **self.boton_estilo)
        self.boton_editar.pack(pady=5)

        self.boton_eliminar = tk.Button(root, text="Eliminar Evento", command=self.eliminar_evento, **self.boton_estilo)
        self.boton_eliminar.pack(pady=5)

        self.boton_mostrar = tk.Button(root, text="Mostrar Eventos", command=self.mostrar_eventos, **self.boton_estilo)
        self.boton_mostrar.pack(pady=5)

        self.boton_filtrar = tk.Button(root, text="Filtrar por Fecha", command=self.filtrar_eventos, **self.boton_estilo)
        self.boton_filtrar.pack(pady=5)

        self.actualizar_lista()

    def cargar_eventos(self):
        try:
            with open("eventos.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def guardar_eventos(self):
        with open("eventos.json", "w") as f:
            json.dump(self.eventos, f)

    def agregar_evento(self):
        evento = simpledialog.askstring("Agregar Evento", "Introduce el nombre del evento:")
        fecha = simpledialog.askstring("Agregar Fecha", "Introduce la fecha del evento (YYYY-MM-DD):")
        
        if evento and fecha:
            try:
                fecha_datetime = datetime.strptime(fecha, "%Y-%m-%d")
                self.eventos.append({"nombre": evento, "fecha": fecha_datetime.strftime("%Y-%m-%d")})
                self.guardar_eventos()
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Evento agregado correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha no válido. Usa YYYY-MM-DD.")

    def editar_evento(self):
        seleccion = self.lista_eventos.curselection()
        if seleccion:
            index = seleccion[0]
            evento_actual = self.eventos[index]
            nuevo_nombre = simpledialog.askstring("Editar Evento", "Nuevo nombre del evento:", initialvalue=evento_actual["nombre"])
            nueva_fecha = simpledialog.askstring("Editar Fecha", "Nueva fecha del evento (YYYY-MM-DD):", initialvalue=evento_actual["fecha"])
            
            if nuevo_nombre and nueva_fecha:
                try:
                    fecha_datetime = datetime.strptime(nueva_fecha, "%Y-%m-%d")
                    self.eventos[index] = {"nombre": nuevo_nombre, "fecha": fecha_datetime.strftime("%Y-%m-%d")}
                    self.guardar_eventos()
                    self.actualizar_lista()
                    messagebox.showinfo("Éxito", "Evento editado correctamente.")
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha no válido. Usa YYYY-MM-DD.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona un evento para editar.")

    def eliminar_evento(self):
        seleccion = self.lista_eventos.curselection()
        if seleccion:
            index = seleccion[0]
            del self.eventos[index]
            self.guardar_eventos()
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Evento eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona un evento para eliminar.")

    def mostrar_eventos(self):
        if not self.eventos:
            messagebox.showinfo("Eventos", "No hay eventos programados.")
        else:
            eventos_str = "\n".join([f"{evento['nombre']} - {evento['fecha']}" for evento in self.eventos])
            messagebox.showinfo("Eventos Programados", eventos_str)

    def filtrar_eventos(self):
        fecha_str = simpledialog.askstring("Filtrar Eventos", "Introduce la fecha (YYYY-MM-DD):")
        if fecha_str:
            try:
                fecha_datetime = datetime.strptime(fecha_str, "%Y-%m-%d")
                fecha_filtrada = fecha_datetime.strftime("%Y-%m-%d")
                eventos_filtrados = [evento for evento in self.eventos if evento["fecha"] == fecha_filtrada]

                if eventos_filtrados:
                    eventos_str = "\n".join([f"{evento['nombre']} - {evento['fecha']}" for evento in eventos_filtrados])
                    messagebox.showinfo("Eventos Filtrados", eventos_str)
                else:
                    messagebox.showinfo("Eventos Filtrados", "No hay eventos para esta fecha.")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha no válido. Usa YYYY-MM-DD.")

    def actualizar_lista(self):
        self.lista_eventos.delete(0, tk.END)
        for evento in self.eventos:
            self.lista_eventos.insert(tk.END, f"{evento['nombre']} - {evento['fecha']}")

if __name__ == "__main__":
    root = tk.Tk()
    calendario = CalendarioEventos(root)
    root.mainloop()
