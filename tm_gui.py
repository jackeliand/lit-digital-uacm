#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.ttk import *
from tkinter import Menu
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import random
import textwrap

global f
global logtxt
logtxt= "\n\n++++++++\n\n"+"Métodos usados:" + "\n"

def acerca():
    acercaTxt='''
    APROPIACIÓN TEXTUAL

    Versión 1.0

    Programa creado para el taller en la UACM Cuautepec:

    "Creatividad computacional: poesía y narrativa generada en inteligencia artificial"
    Prof. Daniel Martínez García
    
    Noviembre 2018

    Dudas:
    daniel.m.olivera@gmail.com
    Twitter: jackeliand
    '''
    messagebox.showinfo('Acerca de este programa', acercaTxt)

def enviar(txtN,txtX):
    txtN.delete(1.0,END)
    txtN.insert(INSERT,txtX.get("1.0",END))

def abrir():
    archivo = askopenfilename(filetypes=[("Archivos de texto","*.txt")])
    f = open(archivo, 'r').read().lower()
    txt1.insert(INSERT,f)

def guardar():
    f = asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(txtd.get("1.0",END))
    f.write(text2save)
    f.close()

def importar(txtN,comboN):
    txtN.delete(1.0,END)
    estado = comboN.get()
    if estado == "Original":
        txtN.insert(INSERT,txt1.get("1.0",END))
    elif estado == "Aleatorio":
        txtN.insert(INSERT,txt2.get("1.0",END))
    elif estado == "Cut-Up":
        txtN.insert(INSERT,txt4.get("1.0",END))
    elif estado == "S+N":
        txtN.insert(INSERT,txt6.get("1.0",END))
    elif estado == "Markov":
        txtN.insert(INSERT,txt8.get("1.0",END))
    elif estado == "Más texto":
        txtN.insert(INSERT,txtb.get("1.0",END))

def versos():
    txt2.delete(1.0,END)
    n=int(spin1.get())
    x=0
    poema1=""
    while x<n:
        myline = random.choice(txt1.get("1.0",END).splitlines())
        poema1 = poema1 + myline + "\n"
        x=x+1
    txt2.insert(INSERT,poema1)
    global logtxt
    logtxt= logtxt + "- Líneas aleatorias" + "\n"

def shuffle():
    txt4.delete(1.0,END)
    words = txt3.get("1.0",END).split()
    random.shuffle(words)
    poema2= textwrap.fill(" ".join(words), 40)
    txt4.insert(INSERT,poema2)
    global logtxt
    logtxt= logtxt + "- Método Cut-Up" + "\n"

def cambio():
    txt6.delete(1.0,END)
    palabra = palabro1.get()
    cambio = palabro2.get()
    desdetxt = txt5.get("1.0",END)
    poema3 = desdetxt.replace(palabra, cambio)
    txt6.insert(INSERT,poema3)
    global logtxt
    logtxt = logtxt + "- S+7" + "\n"

def mastxt():
    txtb.insert(INSERT,txta.get("1.0",END))

def obtenerlog():
    txte.delete(1.0,END)
    txte.insert(INSERT,logtxt)
    
#######
def add_to_model(model, n, seq):
    seq = list(seq[:]) + [None]
    for i in range(len(seq)-n):
        gram = tuple(seq[i:i+n])
        next_item = seq[i+n]
        if gram not in model:
            model[gram] = []
        model[gram].append(next_item)

def markov_model(n, seq):
    model = {}
    add_to_model(model, n, seq)
    return model

def gen_from_model(n, model, start=None, max_gen=100):
    if start is None:
        start = random.choice(list(model.keys()))
    output = list(start)
    for i in range(max_gen):
        start = tuple(output[-n:])
        next_item = random.choice(model[start])
        if next_item is None:
            break
        else:
            output.append(next_item)
    return output

def markov_model_from_sequences(n, sequences):
    model = {}
    for item in sequences:
        add_to_model(model, n, item)
    return model

def markov_generate_from_sequences(n, sequences, count, max_gen=100):
    starts = [item[:n] for item in sequences if len(item) >= n]
    model = markov_model_from_sequences(n, sequences)
    return [gen_from_model(n, model, random.choice(starts), max_gen)
           for i in range(count)]

def markov():
    txt8.delete(1.0,END)
    poema_markov =""
    lines_words = txt7.get("1.0",END).strip().split("\n")
    for item in markov_generate_from_sequences(int(spin2.get()), lines_words,int(spin3.get())):
        verso= ''.join(item)
        poema_markov = poema_markov + verso + "\n"
    txt8.insert(INSERT,poema_markov)
    global logtxt
    logtxt= logtxt + "- N-gramas por cadena de Markov" + "\n"

#######

window = Tk()
window.title("Apropiación textual - Taller de Creatividad Computacional'")
#window.geometry('800x600')

menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label='Cargar original', command=abrir)
new_item.add_separator()
new_item.add_command(label='Limpiar')
new_item.add_command(label='Acerca de...', command=acerca)
new_item.add_separator()
new_item.add_command(label='Salir', command=window.quit)
menu.add_cascade(label='Archivo', menu=new_item)
window.config(menu=menu)

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)
tab6 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Aleatoria')
tab_control.add(tab2, text='Cut-Up')
tab_control.add(tab3, text='S+N')
tab_control.add(tab4, text='Markov')
tab_control.add(tab5, text='Más texto')
tab_control.add(tab6, text='Guardar')
tab_control.pack(expand=1, fill='both')
############
txt1 = scrolledtext.ScrolledText(tab1,width=50,height=30)
txt1.grid(column=0, row=1)
txt2 = scrolledtext.ScrolledText(tab1,width=50,height=30)
txt2.grid(column=2, row=1)

lbl = Label(tab1, text="Original", font=("sans", 14))
lbl.grid(column=0, row=0)
lb2 = Label(tab1, text="Selección aleatoria", font=("sans", 14))
lb2.grid(column=2, row=0)
lb3 = Label(tab1, text="Carga un archivo de texto, copia y pega,\n o escribe en el cuadro de texto.")
lb3.grid(column=0, row=2)
lb8 = Label(tab1, text="(O usa una mezcla)")
lb8.grid(column=0, row=3,sticky = W)
combo1 = Combobox(tab1)
combo1['values']= ("Cut-Up", "Aleatorio", "S+N", "Markov")
combo1.current(1)
combo1.grid(column=0, row=4,sticky = W)
export2 = Button(tab1, text="Importar", command=lambda: importar(txt1,combo1))
export2.grid(column=0, row=4, sticky = E)

lb4 = Label(tab1, text="Número de versos:")
lb4.grid(column=2, row=2, sticky = W)
spin1 = Spinbox(tab1, from_=1, to=99, width=3)
spin1.grid(column=2, row=2, sticky = N)
btn = Button(tab1, text="Elegir versos", command=versos)
btn.grid(column=2, row=2, sticky = E)

btn2 = Button(tab1, text="<", command=lambda: enviar(txt1,txt2))
btn2.grid(column=1, row=1)
#########
txt3 = scrolledtext.ScrolledText(tab2,width=50,height=30)
txt3.grid(column=0, row=1)
btn3 = Button(tab2, text="<", command=lambda: enviar(txt3,txt4))
btn3.grid(column=1, row=1)
txt4 = scrolledtext.ScrolledText(tab2,width=50,height=30)
txt4.grid(column=2, row=1)

lb5 = Label(tab2, text="Texto", font=("sans", 14))
lb5.grid(column=0, row=0)
lb6 = Label(tab2, text="Cut-Up", font=("sans", 14))
lb6.grid(column=2, row=0)

lb7 = Label(tab2, text="Importar desde...")
lb7.grid(column=0, row=2)
combo2 = Combobox(tab2)
combo2['values']= ("Original", "Aleatorio", "S+N", "Markov")
combo2.current(1)
combo2.grid(column=0, row=3,sticky = W)
export1 = Button(tab2, text="Importar", command=lambda: importar(txt3,combo2))
export1.grid(column=0, row=3, sticky = E)

aleat = Button(tab2, text="Tristan-Tzara!", command=shuffle)
aleat.grid(column=2, row=3)
#################
txt5 = scrolledtext.ScrolledText(tab3,width=50,height=30)
txt5.grid(column=0, row=1)
btn4 = Button(tab3, text="<", command=lambda: enviar(txt5,txt6))
btn4.grid(column=1, row=1)
txt6 = scrolledtext.ScrolledText(tab3,width=50,height=30)
txt6.grid(column=2, row=1)

lb8 = Label(tab3, text="Texto", font=("sans", 14))
lb8.grid(column=0, row=0)
lb9 = Label(tab3, text="S+N", font=("sans", 14))
lb9.grid(column=2, row=0)

lb10 = Label(tab3, text="Importar desde...")
lb10.grid(column=0, row=2)
combo3 = Combobox(tab3)
combo3['values']= ("Original", "Aleatorio", "Cut-Up", "Markov")
combo3.current(1)
combo3.grid(column=0, row=3,sticky = W)
export3 = Button(tab3, text="Importar", command=lambda: importar(txt5,combo3))
export3.grid(column=0, row=3, sticky = E)

desdelb = Label(tab3, text="Cambiar la palabra:")
desdelb.grid(column=2, row=3,sticky = W)
palabro1 = Entry(tab3,width=15)
palabro1.grid(column=2, row=3,sticky = N)
hacialb = Label(tab3, text="Por la palabra:")
hacialb.grid(column=2, row=4,sticky = W)
palabro2 = Entry(tab3,width=15)
palabro2.grid(column=2, row=4, sticky = N)
aleat = Button(tab3, text="Cambiar", command=lambda: cambio())
aleat.grid(column=2, row=3,sticky = E)
#################
txt7 = scrolledtext.ScrolledText(tab4,width=50,height=30)
txt7.grid(column=0, row=1)
btn5 = Button(tab4, text="<", command=lambda: enviar(txt7,txt8))
btn5.grid(column=1, row=1)
txt8 = scrolledtext.ScrolledText(tab4,width=50,height=30)
txt8.grid(column=2, row=1)

lb11 = Label(tab4, text="Texto", font=("sans", 14))
lb11.grid(column=0, row=0)
lb12 = Label(tab4, text="Markov", font=("sans", 14))
lb12.grid(column=2, row=0)

lb13 = Label(tab4, text="Importar desde...")
lb13.grid(column=0, row=2)
combo4 = Combobox(tab4)
combo4['values']= ("Original", "Aleatorio", "Cut-Up", "S+N")
combo4.current(1)
combo4.grid(column=0, row=3,sticky = W)
export4 = Button(tab4, text="Importar", command=lambda: importar(txt7,combo4))
export4.grid(column=0, row=3, sticky = E)

lb14 = Label(tab4, text="N-grama:")
lb14.grid(column=2, row=2, sticky = W)
spin2 = Spinbox(tab4, from_=1, to=15, width=3)
spin2.grid(column=2, row=2, sticky = N)
lb15 = Label(tab4, text="Versos:")
lb15.grid(column=2, row=3, sticky = W)
spin3 = Spinbox(tab4, from_=1, to=40, width=3)
spin3.grid(column=2, row=3, sticky = N)
aleat1 = Button(tab4, text="Markov!", command=lambda: markov())
aleat1.grid(column=2, row=3,sticky = E)

#################
txta = scrolledtext.ScrolledText(tab5,width=50,height=30)
txta.grid(column=0, row=1)
btna = Button(tab5, text="<", command=lambda: enviar(txta,txtb))
btna.grid(column=1, row=1)
txtb = scrolledtext.ScrolledText(tab5,width=50,height=30)
txtb.grid(column=2, row=1)

lba = Label(tab5, text="Texto", font=("sans", 14))
lba.grid(column=0, row=0)
lbb = Label(tab5, text="Más texto", font=("sans", 14))
lbb.grid(column=2, row=0)

lbc = Label(tab5, text="Importar desde...")
lbc.grid(column=0, row=2)
comboa = Combobox(tab5)
comboa['values']= ("Original", "Aleatorio", "Cut-Up", "S+N", "Markov")
comboa.current(1)
comboa.grid(column=0, row=3,sticky = W)
exporta = Button(tab5, text="Importar", command=lambda: importar(txta,comboa))
exporta.grid(column=0, row=3, sticky = E)

aleat2 = Button(tab5, text="Pegar más texto", command=lambda: mastxt())
aleat2.grid(column=2, row=3,sticky = N)

#################
txtd = scrolledtext.ScrolledText(tab6,width=50,height=30)
txtd.grid(column=0, row=1)
txte = scrolledtext.ScrolledText(tab6,width=50,height=15)
txte.grid(column=2, row=1,sticky = N)


lbd = Label(tab6, text="Resultado", font=("sans", 14))
lbd.grid(column=0, row=0)
lbe = Label(tab6, text="Operaciones", font=("sans", 14))
lbe.grid(column=2, row=0)

lbf = Label(tab6, text="Importar desde...")
lbf.grid(column=0, row=2)
combob = Combobox(tab6)
combob['values']= ("Original", "Aleatorio", "Cut-Up", "S+N", "Markov", "Más texto")
combob.current(1)
combob.grid(column=0, row=3,sticky = W)
exportb = Button(tab6, text="Importar", command=lambda: importar(txtd,combob))
exportb.grid(column=0, row=3, sticky = E)

aleat3 = Button(tab6, text="Obtener métodos", command=lambda: obtenerlog())
aleat3.grid(column=2, row=2,sticky = N)
aleat3 = Button(tab6, text="Guardar como...", command=lambda: guardar())
aleat3.grid(column=2, row=3,sticky = N)

window.mainloop()
