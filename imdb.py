#imprtacion de librerias
#requests y beatiful soup
import requests
import bs4

# declaracion de listas para guardar los datos leidos

recaudaciones = []
nombres = []
annos = []
califs = []
censuras=[]
runtimes=[]
generos=[]
resumenes=[]

#uso de la funcion get() de la libreria requests
#asigno la pagina que vamos a leer a una variable llmamada pagina_web
#usando get() le solicito al servidor el contenido de la pagina y lo guardo en una variable llamada respuesta


from requests import get
pagina_web = 'https://www.imdb.com/search/title/?release_date=,&sort=boxoffice_gross_us,desc'


respuesta = get(pagina_web)


#aqui hago uso de BeautifulSoup
#creo un objeto tipo Soup con la respuesta que me dio el servidor
#en el objeto soup tengo ya toda la pagina web parseada para ser consumida 
#no especifique el parser a usar para que python seleccione el que mejor encuentre

from bs4 import BeautifulSoup
soup = BeautifulSoup(respuesta.text)
type(soup)
bs4.BeautifulSoup

## esta funcion la cree para limpiar el texto del año
##devuelve los ultimos valores del string

def right(string, n):
        return string[-n:]

#segun la inspeccion al source code html de la pagina web para obtener la lista de peliculas
#necesito Buscar los divs llamados lister-item mode-advanced
#utilizo find_all() para encontrar los divs antes mencionados que contiene la lista de peliculas 


contenedor_peliculas = soup.find_all('div', class_ = 'lister-item mode-advanced')
#print(soup)


#find_all() me devuelve un objeto que contiene los 50 divs de las  50 peliculas (la primera pagina, 50 peliculas por pagina)




# extraer la data de las peliculas del contenedor
for pelicula in contenedor_peliculas:

# titulo de la pelicula
        nombre = pelicula.h3.a.text
        nombres.append(nombre)

# total recaudado
    #este campo presento un problema
    #hay dos etiquetas con el mismo nombre (cantidad de votos y recaudacion $$$)
    #lo soluciones utilizando in find all  de esto mo traigo los 2 elementos y se que el primero es el num votos y el segundo  la recaudacion
    # me intersa la recaudacion por eso utilizo el segundo elemento [1]
        recaudacion = pelicula.find_all('span', attrs = {'name':'nv'})
        #print(recaudacion[1])
        recaudint =recaudacion[1]['data-value']
        # el valor viene separado por commas entonces elimino sus comas para poder guardarlo como entero
        recuadaint = int(recaudint.replace(',' , ''))
        recaudaciones.append(recuadaint)
 
      
        

# el año en que salio la pelicula
        anno = pelicula.h3.find('span', class_ = 'lister-item-year').text
        ##llamo a la funcion para que recorte el string
        anno = right(anno,5)
        #limpio el ')' del inicio del string
        anno= anno.replace(')', '')
        
        annos.append(anno)
# la calificacion asignada por la pagina IMDB
        calif = float(pelicula.strong.text)
        califs.append(calif)
# censura de la pelicula
# este campo no es leido en algunos registros, debi incluir un if para salucionar esto
        
        if (pelicula.find('span', class_ = 'certificate') is None):
                censuras.append('')
                
        else:
                
                censura = pelicula.find('span', class_ = 'certificate').text
                censuras.append(censura)
              
        #censura = pelicula.find('span', class_ = 'certificate').text
        #censuras.append(censura)
        
        
               
# duracion de la pelicula.

        runtime = pelicula.find('span', class_ = 'runtime').text
        runtimes.append(runtime)
# generos de la pelicula
        genero = pelicula.find('span', class_ = 'genre').text
        #limpieza del \n
        genero = genero.replace('\n', '')
        generos.append(genero)
# resumen
        resumen = pelicula.find_all('p', class_ = 'text-muted')
        resumen1 = resumen[1].text
        resumen1 = resumen1.replace('\n', '')
        resumenes.append(resumen1)


 



#utilizo pandas para guardarlo en una estrucura dataframe
import pandas as pd
df = pd.DataFrame({'Nombre': nombres,
'Recaudacion': recaudaciones,
'Fecha': annos,
'Calificacion imdb': califs,
'Censura': censuras,
'Duracion': runtimes,
'Genero': generos,
'resumen': resumenes
})
#print(df)


##exportacion a csv

import tkinter as tk
from tkinter import filedialog

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

def exportCSV ():
    global df
    
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv (export_file_path, index = None, header=True)

saveAsButton_CSV = tk.Button(text='Exportar a CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)

root.mainloop()
