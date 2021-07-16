import pandas as pd
import matplotlib.pyplot as plt

# Nombre de observatorio
codigo_observatorio = input("Ingrese el Codigo: ")     #solicitamos el nombre del codigo observatorio
nombre_archivo = "homog_mo_" +  codigo_observatorio + ".txt" # concatenamos el nombre del codigo con homog-mo y txt para que rastree nuestro archivo
# Leemos el archivo solicitado (region y altitud siempre en lineas 6 y 7)
f = open(nombre_archivo,"r")                           #lectura del archivo con open
lines = f.readlines()                                  #lectura de las lineas del archivo
region = (lines[5]).split(":")[1].strip()              #captura de las variables en las lineas 5 y 6 #para luego proyectar en su correspondiente gráfica
altitud = (lines[6]).split(":")[1].strip()             #usamos el split para eliminar ":" y el strip para eliminar todos los espacios en blancos inciales y finales de una cadena
   

#Calculamos el numero de indice para luego eliminar la lectura la cabecera
index_info = []                           #lista que guarda nuestra linea base- sirve para establecer las variables 
for indice, line in enumerate(lines):     #bucle for para iterar por cada linea del archivo hasta encontrar la palabra "YEAR" (conjunto de caracteres pasados como argumentos)
    if line.startswith('Year'):           #se establece una condición y se usa el "startswith" el cual indica si la cadena comienza o termina con el conjunto de caracteres.
       index_info.append(indice)          #captura el numero de linea y le agregamos a la lista index_info
#print(index_info)                        #index_info que servirá para establecer donde inician las variables necesarias.

#Creamos un data frame con el nombre de las columnas "Year", "Month, "Temperature", "Precipitation"
df = pd.read_fwf(nombre_archivo ,skiprows=index_info[0]) # lectura del archivo con pandas y uso del skiprows para omitir filas mientras lee el archivo.
#print(df.head())                                        #se estable en index_info[0] para tomar el valor inicial de la lista.

#NOTA:(Si existe un error es conveniente establecer en la linea 22----index_info[0]-1,header=1  "unicamente sino lee la cabecera)

#Valores para las fechas                              
desde= str(df.iloc[0,0])           #uso del iloc para la indexacion(seleccion basada en una ubicacion del data frame creado)
hasta = str(df.iloc[-1,0])         #variable desde leerá el primer año de la fila cero, columna YEAR 
#print(desde,hasta)                #variable hasta leerá el ultimo año de la ultima fila, columna YEAR

# Creamos la columna "Fecha" que es la combinacion de mes, dia (1) y año" + df["Year"].astype(str))
df["Fecha"] =  (df["Month"].astype(str) + "/01/"+ df["Year"].astype(str))
df['Fecha']= pd.to_datetime(df['Fecha'])  #convertimos la columna del dt['Fecha'] en to_datatime 
df = df.set_index("Fecha")                #esto servirá para la proyección de las fechas en la gráfica
#print(df)
#print(df.columns)

#Series de tiempo si hay temperatura

if 'Temperature' in df.columns and 'Precipitation' not in df.columns:
    plt.figure()                         #creamos el objeto figura
    ax = df.loc[desde:hasta, 'Temperature'].plot(linestyle='-',color='red',label='Temperature');  #df.loc especificamos que tendra ax =(fechas,columna de temperatura)
    ax.legend(loc='upper right')                       #se establece la leyenda(parte superior derecha)
    media = df["Temperature"].mean()                   #se establece la media de la temperatura
    ax.axhline(y=media, color='red', linestyle='-.')   #dibuja una linea h predeterminada en y=media
    ax.set_xlim([desde,hasta])                         #límites del eje x(fechas)     
    ax.set_ylabel('Temperatura (C°)');                 #título del eje y
    ax.set_title("Temperatura | " + codigo_observatorio + " | " + altitud + " | " + region,fontsize= 15,fontweight="bold")  #se proyectará el título principal con fontsize(tamaño de fuente=15 y fondo=negrita)
 
#Series de tiempo si hay precipitación
if 'Precipitation' in df.columns and 'Temperature' not in df.columns:
    plt.figure() # creamos el objeto figura, en este caso para graficar la precipitación
    ax = df.loc[desde:hasta, 'Precipitation'].plot(linestyle='-',color='blue',label='Precipitación'); #ax recibirá los argumentos de: las fechas y la precipitación, con la ayuda del método "loc[]" 
    ax.legend(loc='upper right')                     #se agrega leyenda (de la precipitación) en la parte superior derecha
    media = df["Precipitation"].mean()               #se obtiene la media (de la precipitación)
    ax.axhline(y=media,color='blue', linestyle='-.') #se establece una linea h predeterminada para y=media
    ax.set_xlim([desde,hasta])                       #se establecen los límites que tendrá la gráfica en el eje x(fechas)
    ax.set_ylabel('Precipitación (mm)');             #se establece el título que tendrá la gráfica en el eje y("precipitación)
    ax.set_title("Precipitación | " + codigo_observatorio + " | " + altitud + " | " + region,fontsize= 15,fontweight="bold") #se crea el encabezado de la gráfica(tamaño de fuente=15 y letra de forma "negrita")

#Series de tiempo hay las dos variables (Precipitación y Temperatura)
if 'Precipitation' in df.columns and 'Temperature' in df.columns:
    fig,ax1 = plt.subplots()                         #"subplots()" crea una Figura con un solo Eje.
    ax1.set_xlabel('Fecha')                          #se establece el nombre del eje "x" (eje que va a ser compartido)
    
    ax1.set_ylabel('Temperatura (C°)', color='red')  #se establece el nombre del eje "y" para ax1
    ax1.plot(df.loc[desde:hasta, 'Temperature'], color='red',label='Temperature') #ax recibirá los argumentos de: las fechas y la temperatura, con la ayuda del método "loc[]" 
    ax1.tick_params(axis='y', labelcolor='red')      #indicamos que la temperatura estará en le eje “y” con color rojo
    media = df["Temperature"].mean()                 #se obtiene la media (de la temperatura)
    ax1.axhline(y=media,color='red', linestyle='-.') #se establece una linea h predeterminada para y=media
    
    ax2 = ax1.twinx()  #se establece un segundo eje que comparte el mismo eje x
    ax2.set_ylabel('Precipitación (mm)', color='blue')  #ahora se establece el nombre del eje "y" para ax2
    ax2.plot(df.loc[desde:hasta, 'Precipitation'], color='blue',label='Precipitación') #ax recibirá los argumentos de: las fechas y la precipitación, con la ayuda del método "loc[]" 
    ax2.tick_params(axis='y', labelcolor='blue')     #indicamos que la temperatura estará en le eje “y” con color azul
    media = df["Precipitation"].mean()               #se obtiene la media (de la temperatura)
    ax2.axhline(y=media,color='blue', linestyle='-.')#se establece una linea h predeterminada para y=media
    ax2.set_title("Temperatura y Precipitación | " + codigo_observatorio + " | " + altitud + " | " + region,fontsize= 15,fontweight="bold") #se crea el encabezado de la gráfica(tamaño de fuente=15 y letra de forma "negrita")
    
    fig.tight_layout() #este método nos ayuda a que los parámetros de la figura se ajusten al área de la figura
    fig.legend(loc='lower right',bbox_to_anchor=(0.88, 0.75))#se crea la leyenda de la figura, especificando su posicion y coordenadas para un mejor resultado
    plt.show() #se muestran las figuras
    
