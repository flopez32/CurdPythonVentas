import tkinter as tk
from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
from Ventas import *
from Conexon import *

class Ventas:

    global base
    base = None

    global textBoxId
    textBoxId = None

    global textBoxNombre
    textBoxNombre = None

    global textBoxProducto
    textBoxProducto = None

    global textBoxPrecio
    textBoxPrecio = None

    global textBoxDomicilio
    textBoxDomicilio = None

    global groupBox
    groupBox = None

    global tree
    tree = None

    global combo
    combo = None
    
    
    def Formulario():

        global textBoxId
        global textBoxNombre
        global textBoxProducto   
        global textBoxPrecio
        global textBoxDomicilio
        global groupBox
        global tree
        global combo
        global base

        try:
            base = tk.Tk()
            base.geometry("1200x300")
            base.title("Ventas")
            base.configure(bg="#0de8f8")

            #  LabelFrame 
            groupBox = ttk.LabelFrame(base, text="Formulario de Ventas")
            groupBox.grid(column=0, row=0, padx=10, pady=10)

            #  Label 
            labelId = Label(groupBox, text="ID", width=20, font=("Arial", 12))
            labelId.grid(column=0, row=0)

            #  Entry separado de grid
            textBoxId = Entry(groupBox, width=20)
            textBoxId.grid(column=1, row=0)

            #  Label Nombre
            labelNombre = Label(groupBox, text="Nombre", width=20, font=("Arial", 12))
            labelNombre.grid(column=0, row=2)

            #  Entry Nombre
            textBoxNombre = Entry(groupBox, width=20)
            textBoxNombre.grid(column=1, row=2)

            #  Label Producto
            labelProducto = Label(groupBox, text="Producto", width=20, font=("Arial", 12))
            labelProducto.grid(column=0, row=1)

            #  Entry Producto
            textBoxProducto = Entry(groupBox, width=20)
            textBoxProducto.grid(column=1, row=1)
   
            #  Label Precio
            labelPrecio = Label(groupBox, text="Precio", width=20, font=("Arial", 12))
            labelPrecio.grid(column=0, row=3)

            #  Entry Precio
            textBoxPrecio = Entry(groupBox, width=20)
            textBoxPrecio.grid(column=1, row=3)

            #  Labe Domicilio
            labelDomicilio = Label(groupBox, text="Domicilio", width=20, font=("Arial", 12))
            labelDomicilio.grid(column=0, row=4)

            seleccionDom = tk.StringVar()
            combo = ttk.Combobox(groupBox, width=17, textvariable=seleccionDom)
            combo['values'] = ("si", "no")
            combo.grid(column=1, row=4)
            seleccionDom.set("no")

            Button(groupBox, text="Registrar Venta",width=15,command=GuardarVenta).grid(column=0, row=5)
            Button(groupBox, text="Modificar vaenta",width=15,command=ModificarVentaFormulario).grid(column=1, row=5)
            Button(groupBox, text="Elimina Venta",width=15,command=EliminarVentaFormulario).grid(column=2, row=5)
            Button(groupBox, text="LimpiarDatos",width=15,command=LimpiarCampos).grid(column=2, row=4)
            Button(groupBox, text="Buscar",width=15,command=BuscarPorId).grid(column=2, row=1)

            groupBox = ttk.LabelFrame(base, text="lista de Ventas")
            groupBox.grid(column=1, row=0, padx=10, pady=10)

            #Crear un treeeview
            #Configurar las columnas
            tree = ttk.Treeview(groupBox, columns=("Id","Nombre","Producto","Precio","Domicilio"), show="headings" ,height=5)

            tree.bind("<<TreeviewSelect>>", SelecionarVenta)

            tree.column("#1", anchor="center", width=50)
            tree.heading("#1", text="Id")

            tree.column("#2", anchor="center" , width=150)
            tree.heading("#2", text="Nombre")

            tree.column("#3", anchor="center", width=230)
            tree.heading("#3", text="Producto")

            tree.column("#4", anchor="center", width=150)
            tree.heading("#4", text="Precio")

            tree.column("#5", anchor="center", width=150)
            tree.heading("#5", text="Domicilio")

            #Agregar los datois a la tabla
            #Mostar la tabla

            for row in CVentas.MostrarVenta():
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

            tree.pack(fill="both", expand=True) 
            base.mainloop()

        except ValueError as error:
            print("Error al mostrar la interfaz, error: {}".format(error))

def GuardarVenta():
                
                global textBoxProducto, textBoxNombre, textBoxPrecio, combo, groupBox

                try:
                    if textBoxNombre is None or textBoxProducto is None or textBoxPrecio is None:
                       print("los witgets no estan inicialisados")
                       return
                    
                    Nombre = textBoxNombre.get()
                    Producto = textBoxProducto.get()
                    Precio = textBoxPrecio.get()
                    Domicilio = combo.get()

                    CVentas.IngresarVentas(Nombre, Producto, Precio, Domicilio)
                    messagebox.showinfo("Éxito", "Venta registrada correctamente")

                    RefrescarTree()

                    #limpiamos los campos
                    textBoxNombre.delete(0, END)
                    textBoxProducto.delete(0, END)  
                    textBoxPrecio.delete(0, END)
                    combo.set("no")

                except ValueError as e:
                    print("Error al guardar la venta, error: {}".format(e))
                    messagebox.showerror("Error", "Error al guardar la venta")

def EliminarVentaFormulario():
    global textBoxId

    try:
        id = textBoxId.get()

        if id == "":
            messagebox.showwarning("Error", "Ingrese un ID")
            return

        resultado = CVentas.EliminarVenta(id)

        if resultado:
            messagebox.showinfo("Éxito", "Venta eliminada correctamente")
            RefrescarTree()



            #limpiamos los campos
            textBoxId.delete(0, END)
            textBoxNombre.delete(0, END)
            textBoxProducto.delete(0, END)  
            textBoxPrecio.delete(0, END)
            combo.set("no")

            textBoxId.delete(0, END)
        else:
            messagebox.showerror("Error", "No se pudo eliminar")

    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", str(e))

def ModificarVentaFormulario():
    global textBoxId, textBoxNombre, textBoxProducto, textBoxPrecio, combo

    try:
        Id = textBoxId.get()
        Nombre = textBoxNombre.get()
        Producto = textBoxProducto.get()
        Precio = textBoxPrecio.get()
        Domicilio = combo.get()

        if Id == "":
            messagebox.showwarning("Error", "Debe ingresar ID")
            return

        resultado = CVentas.ModificarVenta(Id, Nombre, Producto, Precio, Domicilio)

        if resultado:
            messagebox.showinfo("Éxito", "Venta modificada correctamente")
            RefrescarTree()

            #limpiamos los campos
            textBoxNombre.delete(0, END)
            textBoxProducto.delete(0, END)  
            textBoxPrecio.delete(0, END)
            combo.set("no")
        else:
            messagebox.showerror("Error", "No se pudo modificar")

    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", str(e))  

def RefrescarTree():
    global tree

    # limpiar tabla
    for item in tree.get_children():
        tree.delete(item)

    # cargar datos desde la BD
    for row in CVentas.MostrarVenta():
        tree.insert("", "end", values=(
            row[0], row[1], row[2], row[3], row[4]
        ))

def SelecionarVenta(event):
    global tree, textBoxId, textBoxNombre, textBoxProducto, textBoxPrecio, combo

    try:
        item = tree.selection()[0]
        values = tree.item(item, "values")

        textBoxId.delete(0, END)
        textBoxId.insert(0, values[0])

        textBoxNombre.delete(0, END)
        textBoxNombre.insert(0, values[1])

        textBoxProducto.delete(0, END)
        textBoxProducto.insert(0, values[2])

        textBoxPrecio.delete(0, END)
        textBoxPrecio.insert(0, values[3])

        combo.set(values[4])

    except IndexError:
        print("No se seleccionó ningún elemento")  

def LimpiarCampos():
        global textBoxId, textBoxNombre, textBoxProducto, textBoxPrecio, combo
        try:
            textBoxId.delete(0, END)
            textBoxNombre.delete(0, END)
            textBoxProducto.delete(0, END)  
            textBoxPrecio.delete(0, END)
            combo.set("no")
        except Exception as e:
            print("Error al limpiar campos:", e)

def BuscarPorId():
    global textBoxId, textBoxNombre, textBoxProducto, textBoxPrecio, combo

    try:
        Id = textBoxId.get()

        if Id == "":
            messagebox.showwarning("Error", "Ingrese un ID")
            return

        # Buscar en la BD
        datos = CVentas.BuscarVenta(Id)

        if datos:
            # Llenar formulario
            textBoxNombre.delete(0, END)
            textBoxNombre.insert(0, datos[1])

            textBoxProducto.delete(0, END)
            textBoxProducto.insert(0, datos[2])

            textBoxPrecio.delete(0, END)
            textBoxPrecio.insert(0, datos[3])

            combo.set(datos[4])

        else:
            messagebox.showwarning("Error", "No se encontró el registro")

    except Exception as e:
        print("Error al buscar:", e)            
      
          
Ventas.Formulario()


       
   