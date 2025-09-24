from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime, timedelta
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Archivo donde se guardarán los mensajes
#ARCHIVO_MENSAJES = 'mensajes.csv'
ARCHIVO_MENSAJES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mensajes.csv')

def leer_mensajes():
    """Lee todos los mensajes del archivo CSV"""
    mensajes = []
    if os.path.exists(ARCHIVO_MENSAJES):
        with open(ARCHIVO_MENSAJES, 'r', newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                mensajes.append(fila)
    return mensajes

def guardar_mensaje(nombre, mensaje):
    """Guarda un nuevo mensaje en el archivo CSV"""
    archivo_existe = os.path.isfile(ARCHIVO_MENSAJES)
    
    with open(ARCHIVO_MENSAJES, 'a', newline='', encoding='utf-8') as archivo:
        campos = ['nombre', 'mensaje', 'fecha']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        
        if not archivo_existe:
            escritor.writeheader()
            
        # Agregar 2 horas a la hora actual
        fecha_actualizada = datetime.now() + timedelta(hours=2)
        
        escritor.writerow({
            'nombre': nombre,
            'mensaje': mensaje,
            'fecha': fecha_actualizada.strftime('%d/%m/%Y - %H:%M:%S')
        })

@app.route('/')
def index():
    """Sirve la página principal con los mensajes existentes"""
    mensajes = leer_mensajes()
    # Invertir el orden para mostrar los más recientes primero
    mensajes.reverse()
    return render_template('index.html', mensajes=mensajes)

@app.route('/agregar-mensaje', methods=['POST'])
def agregar_mensaje():
    """Recibe y guarda un nuevo mensaje del formulario"""
    nombre = request.form.get('nombre')
    mensaje_texto = request.form.get('mensaje')
    
    if nombre and mensaje_texto:
        guardar_mensaje(nombre, mensaje_texto)
    
    return redirect('/')

@app.route('/borrar-mensaje', methods=['POST']) 
def borrar_mensaje():
    """Borra un mensaje específico basándose en el nombre del autor"""
    try:
        nombre_a_borrar = request.form.get('nombre') 
        if not nombre_a_borrar:
            return redirect('/')
            
        mensajes = leer_mensajes()

        # Filtrar los mensajes manteniendo solo los que NO coinciden
        mensajes_actualizados = [m for m in mensajes if m['nombre'] != nombre_a_borrar]

        # Solo reescribir si hubo cambios
        if len(mensajes_actualizados) < len(mensajes):
            with open(ARCHIVO_MENSAJES, 'w', newline='', encoding='utf-8') as archivo:
                campos = ['nombre', 'mensaje', 'fecha']
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(mensajes_actualizados)

        return redirect('/')
    
    except Exception as e:
        print(f"Error al borrar mensaje: {e}")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)