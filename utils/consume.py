import requests
from fastapi import Depends
import jaro
from datetime import date
from .procesar_archivo import buscar2
import random,string
import pandas as pd
from .config import get_settings
from fpdf import FPDF
import random
import string
import hashlib

dato=get_settings()

def generar_password(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(caracteres, k=longitud))
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash

def consumir(nombre_busca,coincidencia):
    coincidencia = coincidencia/100
    list_ofac = [] 
    list_onu = []
    list_fbi = []
    val_ofac = ' '
    val_onu = ' '
    val_fbi = ' '
    nombre_busca = nombre_busca.upper()
    nombre_busca = nombre_busca.replace(" ", "")

    #Ofac
    url = dato.URLOFAC
    data = requests.get(url)
    if data.status_code == 200:
        data_ofac = data.json()
    for datos in data_ofac :
        nombre = str(datos[1])
        p = jaro.jaro_metric(nombre_busca,nombre)
        if p >= coincidencia :
            val_ofac = 'X'
            dicc_onu = {'List':'Ofac','Name': datos[1] ,'tipoId':datos[2],'identificacion':datos[3],'direccion':datos[4],'pais':datos[5],'ciudad':datos[6]}
            list_ofac.append(dicc_onu)
            
            
    #Onu
    url =dato.URLONU
    data = requests.get(url)
    if data.status_code == 200:
        data_onu= data.json()
    for datos in data_onu:
        nombre=str(datos[1])
        p= jaro.jaro_metric(nombre_busca,nombre)
        if p>=coincidencia :
            val_onu='X'
            dicc_onu = {'List':'Onu','Name':datos[1],'Tipo_documento':datos[2],'Numero_documento':datos[3],'Description':datos[4],'Pais':datos[5],'Fecha_nacimiento':datos[6]}
            list_onu.append(dicc_onu)

    
    url =dato.URLFBI
    try:
        data = requests.get(url)
        if data.status_code == 200:
            data_fbi= data.json()
        for datos in data_fbi:
            nombre=str(datos[1])
            p= jaro.jaro_metric(nombre_busca,nombre)
            if p>=0.77 :
                val_fbi='X'
                dicc_fbi = {'List':'Fbi','name':datos[1],'Detalle':datos[2],'Link_info':datos[3],'Nacionalidad':datos[4],'Link_picture':datos[5],'Link_ref':datos[6]}
                list_fbi.append(dicc_fbi)
    except:
        raise Exception


    #Generador de id de consulta
    
    today = generar_password(8)
    lista_busquedad = list_onu + list_ofac + list_fbi

    lista ={'FirstName':nombre_busca,'ListOfac':val_ofac,'ListOnu':val_onu,'ListFbi':val_fbi,'FindDate':today,'Consulta':rand,'list_find':lista_busquedad}
    
    return lista

def consumir_id(id,coincidencia):
    coincidencia = coincidencia/100
    list_ofac = [] 
    list_onu = []
    list_fbi = []
    val_ofac = ' '
    val_onu = ' '
    val_fbi = ' '

    #Ofac
    url = dato.URLOFAC
    data = requests.get(url)
    if data.status_code == 200:
        data_ofac = data.json()
    for datos in data_ofac :
        nombre = str(datos[3])
        p = jaro.jaro_metric(id,nombre)
        if p >= coincidencia :
            val_ofac = 'X'
            dicc_onu = {'list':'Ofac','name': datos[1] ,'tipoId':datos[2],'identificacion':datos[3],'direccion':datos[4],'pais':datos[5],'ciudad':datos[6]}
            list_ofac.append(dicc_onu)
            
            
    #Onu
    url =dato.URLONU
    data = requests.get(url)
    if data.status_code == 200:
        data_onu= data.json()
    for datos in data_onu:
        nombre=str(datos[3])
        p= jaro.jaro_metric(id,nombre)
        if p>=coincidencia :
            val_onu='X'
            dicc_onu = {'list':'Onu','name':datos[1],'tipo_documento':datos[2],'numero_documento':datos[3],'description':datos[4],'pais':datos[5],'fecha_nacimiento':datos[6]}
            list_onu.append(dicc_onu)

    url =dato.URLFBI
    try:
        data = requests.get(url)
        if data.status_code == 200:
            data_fbi= data.json()
        for datos in data_fbi:
            nombre=str(datos[1])
            p= jaro.jaro_metric(id,nombre)
            if p>=coincidencia :
                val_fbi='X'
                dicc_fbi = {'list':'Fbi','name':datos[1],'detalle':datos[2],'link_info':datos[3],'nacionalidad':datos[4],'link_picture':datos[5],'link_ref':datos[6]}
                list_fbi.append(dicc_fbi)
    except:
        raise Exception

    #Generador de id de consulta
    rand = random.choice(string.ascii_letters)
    rand1 = random.choice(string.ascii_letters)
    rand2 = random.randint(1, 20) * 5
    rand = rand1+str(rand2)+rand
    today = str(date.today())
    lista_busquedad = list_onu + list_ofac + list_fbi

    lista ={'FirstName':id,'ListOfac':val_ofac,'ListOnu':val_onu,'ListFbi':val_fbi,'FindDate':today,'Consulta':rand,'list_find':lista_busquedad}
    
    return lista

def consumir_2(lista:list,name:str):

    lista1 = {'Nombre':[],'ListaOnu':[],'ListaOfac':[],'ListaFBI':[],'ListaCargue':[]}
    writer=pd.ExcelWriter(dato.NAME_ARCHIVO_REPORTE)
    for nombre_busca in lista:
        if nombre_busca[0] is not None:

            val_ofac=' '
            val_onu=' '
            val_fbi=' '
            nombre_busca=nombre_busca[0].upper()
            val_cargue=buscar2(nombre_busca,90)
            
            #Ofac
            url =dato.URLOFAC
            data = requests.get(url)
            if data.status_code == 200:
                data_ofac= data.json()
            for datos in data_ofac :
                datos=str(datos)
                p= jaro.jaro_metric(nombre_busca,datos)
                if p>= 0.9 :
                    val_ofac='X'
            #Onu
            url =dato.URLONU
            data = requests.get(url)
            if data.status_code == 200:
                data_onu= data.json()
            for datos in data_onu:
                datos=str(datos)
                p= jaro.jaro_metric(nombre_busca,datos)
                if p>=0.9 :
                    val_onu='X'
            
            url =dato.URLFBI
            data = requests.get(url)
            if data.status_code == 200:
                data_fbi= data.json()
            for datos in data_fbi:
                datos=str(datos)
                p= jaro.jaro_metric(nombre_busca,datos)
                if p>=0.9 :
                    val_onu='X'

            #añadir a lista
            lista1['Nombre'].append(nombre_busca)
            lista1['ListaOfac'].append(val_ofac)
            lista1['ListaOnu'].append(val_onu)
            lista1['ListaFBI'].append(val_fbi)
            lista1['ListaCargue'].append(val_cargue)
    
    df1=pd.DataFrame(lista1, columns=['Nombre','ListaOfac','ListaOnu','ListaFBI','ListaCargue'])
    
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)
    pdf.cell(0, 10, "Mi Reporte LPR", align="C")
    pdf.ln(20)
    pdf.image("7.jpg", x=80, y=30, w=50, h=50)
    pdf.ln(60)

    # Cabecera de la tabla
    pdf.cell(30)
    pdf.cell(30,10,"Nombre", border=1)
    pdf.cell(30,10,"Lista Ofac", border=1,align="center")
    pdf.cell(30,10,"Lista Onu", border=1,align="center")
    pdf.cell(30,10,"Lista FBI", border=1,align="center")
    pdf.cell(30,10,"Lista Cargue", border=1,align="center")
    pdf.ln()

    # Agregar filas
    for fila in df1.values:
        pdf.cell(30)
        for valor in fila:
            pdf.cell(30,10,str(valor), border=1, align= "center")
        pdf.ln()

    # Guardar archivo
    pdf.output("tabla.pdf")
    
    
    df1.to_excel(writer,'Reporte',index=False)
    writer.save()
    

    #Generador de id de consulta
    rand = random.choice(string.ascii_letters)
    rand1 = random.choice(string.ascii_letters)
    rand2 = random.randint(1, 20) * 5
    rand = rand1+str(rand2)+rand
    today = str(date.today())

    lista ={'FirstName':name,'ListOfac':'','ListOnu':'','ListFbi':'','FindDate':today,'Consulta':rand}
    
    return lista



