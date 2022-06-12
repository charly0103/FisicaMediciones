from cgitb import text
from cmath import sqrt
from decimal import getcontext
from inspect import getcoroutinelocals
from operator import itemgetter
from struct import iter_unpack
from tkinter import *
from tkinter import ttk
from turtle import position, width
from tkinter import messagebox
import numpy as np

class Medicion:
    contadorFilas = 0
    idEdicion = 0
    idEliminado = 0
    def __init__(self,ventana):
        
        self.ventana = ventana
        self.ventana.title("Operador de")
        
        marco = LabelFrame(self.ventana,text="Medicione de Fisica").grid(row=0,column=0)
        #Titulo
        titulo = Label(marco,text="Complete los campos").grid(row=0,columnspan=3,sticky="")
        
        #Error instrumento
        Label(marco,text="∆ Instrumento").grid(row=1,column=0)
        self.eIns = Entry(marco)
        self.eIns.grid(row=1,column=1)
        self.eIns.bind('<Return>',self.realizaCalculos)
        
        #decimales
        Label(marco,text="Cantidad de decimales").grid(row=2,column=0)
        self.decimales = Entry(marco)
        self.decimales.grid(row=2,column=1)
        self.decimales.bind('<Return>',self.realizaCalculos)
        #FALSO para hacer espacio
        Label(marco,text="").grid(row=3,column=0)
        
        #Medicion
        Label(marco,text="Ingrese medición (presione enter para que registre):").grid(row=4,column=0)
        self.medicion = Entry(marco)
        self.medicion.grid(row=4,column=1)
        self.medicion.bind('<Return>',self.crearEntrada)

        #Tabla
        self.tabla = ttk.Treeview(self.ventana)
        self.tabla["columns"] = ("0","1","2","3","4","5","6","7","8")
        self.tabla['show'] = 'headings'
        self.tabla.grid(row=5,column=0,columnspan=9)
        self.tabla.column("0",width=80)
        self.tabla.column("1",width=80)
        self.tabla.column("2",width=80)
        self.tabla.column("3",width=80)
        self.tabla.column("4",width=80)
        self.tabla.column("5",width=80)
        self.tabla.column("6",width=80)
        self.tabla.column("7",width=80)
        self.tabla.column("8",width=80)

        self.tabla.heading("0",text="Nº")
        self.tabla.heading("1",text="Xi")
        self.tabla.heading("2",text="Ẍ")
        self.tabla.heading("3",text="|Xn - Ẍ|")
        self.tabla.heading("4",text="∆instrumento")
        self.tabla.heading("5",text="∆Medicion")
        self.tabla.heading("6",text="|Xn - Ẍ|^2")
        self.tabla.heading("7",text="E.C.M")
        self.tabla.heading("8",text="ex%")

        self.tabla.bind('<ButtonRelease-1>',self.selectItem)
        
        #Cantidadmediciones
        self.cantMed = Label(marco,text="Cantidad de mediciones: 0")
        self.cantMed.grid(row=7,column=0)
        #Edicion
        Label(marco,text="Presione una línea para editar o borrar").grid(row=8,column=0)
        self.editar = Entry(marco)
        self.editar.grid(row=8,column=1)
        #Boton
        ttk.Button(marco,text="Guardar cambios",command=self.guardarEdicion).grid(row=8,column=2)
        ttk.Button(marco,text="Eliminar",command=self.eliminarFila).grid(row=8,column=3)

        #Resultado
        self.resultado = Label(marco,text="",fg="green")
        self.resultado.grid(row=9,column=0)
        

    def crearEntrada(self,x):
        if (len(self.medicion.get()) > 0 & len(self.eIns.get()) > 0 & len(self.decimales.get()) > 0 ):
            messagebox.showinfo(message="Deben estar completos el error del instrumento, cantidad de decimales y medida.", title="ERROR")
        else:
            dato = int(self.medicion.get())
            self.contadorFilas=self.contadorFilas+1
            self.tabla.insert('',"end",iid=self.contadorFilas,values=(self.contadorFilas,dato))
            self.medicion.delete(0,"end")
            self.medicion.focus()
            self.cantMed["text"]="Cantidad de mediciones: " + str(self.contadorFilas)
            self.realizaCalculos(self)

    def selectItem(self,a):
        item = self.tabla.focus()
        if (item != ''):
            self.editar.focus()
            valor = self.tabla.item(item,"values")            
            self.idEdicion = valor[0]
            self.editar.delete(0,"end")
            self.editar.insert(0,valor[1])

    def guardarEdicion(self):
        item = self.tabla.focus()
        if (item != ''):
            dato = int(self.editar.get())
            self.tabla.item(item,text="",values=(self.idEdicion,dato))
            self.editar.delete(0,"end")
            self.medicion.focus()
            self.realizaCalculos(self)
            
    def eliminarFila(self):
        item = self.tabla.focus()
        if (item != ''):
            self.idEliminado = self.tabla.item(item,"values")[0]
            self.tabla.delete(item)
            self.contadorFilas=self.contadorFilas-1
            self.editar.delete(0,"end")
            self.recargarTabla(self)
            self.realizaCalculos(self)
            self.medicion.focus()

    def realizaCalculos(self,a):
        if(self.contadorFilas > 1):
            grillaCalculos=[]
            for x in range(self.contadorFilas):
                item = ["","","","","","","","",""]
                tupla = self.tabla.item(str(x+1),"values")
                item[0] = tupla[0]
                item[1] = tupla[1]
                grillaCalculos.append(item)

            if(len(grillaCalculos) > 0):
                sumaErrores = 0
                for item in grillaCalculos:
                    sumaErrores = float(item[1])+sumaErrores
                promedioErrores = round(sumaErrores / len(grillaCalculos),int(self.decimales.get()))

            for item in grillaCalculos:
                item[2]=promedioErrores
                item[3]=abs(round(float(item[1])-promedioErrores,int(self.decimales.get())))
                item[4]=float(self.eIns.get())

            sumaPromedioErrores=0
            for item in grillaCalculos:
                    sumaPromedioErrores = float(item[3])+sumaPromedioErrores
            promedioDifError = round(sumaPromedioErrores/len(grillaCalculos),int(self.decimales.get()))

            for item in grillaCalculos:
                item[5]=promedioDifError
                item[6]=item[3]**2

            sumaErroresCuadrados=0
            for item in grillaCalculos:
                    sumaErroresCuadrados = float(item[6]) + sumaErroresCuadrados
            ECM= sqrt(sumaErroresCuadrados/(len(grillaCalculos) * (len(grillaCalculos)-1)) )
            ECM = round(ECM.real,int(self.decimales.get()))
            ValorRepresenativo = round(promedioErrores,int(self.decimales.get()))
            VariacionError = round(max(float(self.eIns.get()),promedioDifError,ECM),int(self.decimales.get()))
            for item in grillaCalculos:
                item[7]=ECM
                item[8]=(VariacionError / promedioErrores)*100

            registros = self.tabla.get_children()
            for registro in registros:
                self.tabla.delete(registro)
            for item in grillaCalculos:
                self.tabla.insert('',"end",iid=item[0],values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]))

            self.resultado["text"]="El resultado es: " + str(ValorRepresenativo) + "±" + str(VariacionError)

    def recargarTabla(self,a):
        arrayTemporal=[]
        registros = self.tabla.get_children()
        for registro in registros:
            item =  np.asarray(self.tabla.item(registro,"values"))
            if(int(item[0])>int(self.idEliminado)):
                item[0]=int(item[0])-1
            arrayTemporal.append(item)
            self.tabla.delete(registro)

        for item in arrayTemporal:
                self.tabla.insert('',"end",iid=item[0],values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]))


#Pantalla principal
if __name__== "__main__":
    ventana=Tk()
    ventana.geometry("750x500")
    aplicacion = Medicion(ventana)
    aplicacion.eIns.focus()
    ventana.mainloop()
