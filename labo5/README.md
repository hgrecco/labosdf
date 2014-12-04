#labo5_df_uba
  
Programas utilizados en las prácticas del Laboratorio 5, DF, UBA
  
##Descripción de los archivos  
  
__instrumentos.py__  
Archivo con las clases de cada instrumental. En particular implementamos un osciloscopio para la práctca de conteo y un amplificador Lockin para la práctica de Fotoeléctrico 

__conteo.py__  
Programa para la práctica de conteo de fotones. Este programa consiste en tomar varias ventana de tiempo del osciloscopio, que está midiendo la señal de salida del PMT, y obtener un histograma de cuentas por ventana. El programa está particionado en funciones, para el uso en una interfaz interactiva como ser IPython.  
  
__fotoelectrico.py__  
Programa de adquisición de datos, análisis de estos y simulación para la práctica de fotoeléctrico.  El programa está particionado con funciones. La variable config es global al script, cada función recibe la varible de configuración, por lo que cada función usa una copia de la variable. adqFotocorriente() obtiene una fotocorriente y simFotocorriente() presenta una simulación dado un espectro de origen.

##TODO  
  
Nos queda pendiente efectuar la interface con el espectofotómetro manejado con el Arduino, pero en paticular también nos queda pendiente seguir avanzando en el hardware de esa práctica

