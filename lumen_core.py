import os
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
    
    # Parsear la URL de Supabase
    try:
        # Eliminar posibles espacios y caracteres inválidos
        clean_url = SUPABASE_URL.strip()
        if clean_url.endswith('/'):
            clean_url = clean_url[:-1]
            
        # Extraer componentes de la URL
        protocol = "https://"
        base_url = clean_url.replace(protocol, "")
        host = base_url.split('/')[0]
        project_path = '/' + '/'.join(base_url.split('/')[1:]) if '/' in base_url else ''
        
        # Construir el endpoint completo
        endpoint = f"{project_path}/rest/v1/eventos"
        
        print(f"ℹ️ Supabase Host: {host}")
        print(f"ℹ️ Endpoint: {endpoint}")
    
    except Exception as e:
        print(f"❌ Error al parsear SUPABASE_URL: {str(e)}")
        return
    
    # Configurar conexión HTTPS
    try:
        conn = http.client.HTTPSConnection(host, context=ssl._create_unverified_context())
    except Exception as e:
        print(f"❌ Error al establecer conexión HTTPS: {str(e)}")
        return
    
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
        # CORRECCIÓN CLAVE: Usar argumentos de palabra clave correctamente
        conn.request(
            method="POST",
            url=endpoint,
            body=json.dumps(test_data),
            headers=headers  # Argumento de palabra clave
        )
        
        response = conn.getresponse()
        status = response.status
        response_data = response.read().decode()
        
        # Verificar el código de estado
        if status in [200, 201, 204]:
            print(f"✅ Inserción exitosa! Código: {status}")
            if response_data:
                print(f"📄 Respuesta: {response_data}")
        else:
            print(f"❌ Error en Supabase (Código {status}): {response_data}")
    
    except Exception as e:
        print(f"❌ Error durante la conexión: {str(e)}")
    
    finally:
        # Cerrar la conexión
        conn.close()
        print("🔒 Conexión cerrada")

if __name__ == "__main__":
    main()
    print("🏁 Ejecución completada")
