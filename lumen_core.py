import os
import time
import json
import http.client
import ssl

def main():
    print("🚀 Iniciando LUMEN Core...")
    
    # Verificar variables de entorno
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")
        return
    
    print("✅ Variables de entorno verificadas")
    
    # Extraer host y path de la URL de Supabase
    supabase_host = SUPABASE_URL.split('//')[1].split('/')[0]
    supabase_path = '/' + '/'.join(SUPABASE_URL.split('//')[1].split('/')[1:]) + "/rest/v1/eventos"
    
    # Configurar conexión HTTPS
    conn = http.client.HTTPSConnection(supabase_host, context=ssl._create_unverified_context())
    
    # Encabezados para Supabase
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    # Datos de prueba para inserción
    test_data = {
        "nombre": "Evento de prueba",
        "fecha": "2023-12-31T23:59:59",
        "descripcion": "Este es un evento de prueba para validar la conexión"
    }
    
    print("⏳ Intentando inserción de prueba en la tabla 'eventos'...")
    
    try:
        # Realizar la solicitud POST
        conn.request("POST", supabase_path, body=json.dumps(test_data), headers)
        response = conn.getresponse()
        
        # Leer y decodificar la respuesta
        response_data = response.read().decode()
        
        # Verificar el código de estado
        if response.status in [200, 201]:
            print(f"✅ Inserción exitosa! Respuesta: {response_data}")
        else:
            print(f"❌ Error en Supabase (Código {response.status}): {response_data}")
    
    except Exception as e:
        print(f"❌ Error durante la conexión: {str(e)}")
    
    finally:
        # Cerrar la conexión
        conn.close()

if __name__ == "__main__":
    main()
    print("🏁 Ejecución completada")
