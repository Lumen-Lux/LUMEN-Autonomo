from supabase import create_client, Client
import os
import requests
import time
import sys
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("LUMEN Core")

def main():
    logger.info("🚀 Iniciando LUMEN Core...")
    
    # Verificar variables de entorno
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("❌ Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")
        return
    
    logger.info("✅ Variables de entorno verificadas")
    
    # Crear cliente de Supabase
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Conexión a Supabase establecida")
    except Exception as e:
        logger.error(f"❌ Error al conectar con Supabase: {str(e)}")
        return
    
    # Datos de prueba para inserción
    test_data = {
        "nombre": "Evento de prueba",
        "fecha": "2023-12-31T23:59:59",
        "descripcion": "Este es un evento de prueba para validar la conexión"
    }
    
    # Intentar inserción en la base de datos
    logger.info("⏳ Intentando inserción de prueba en la tabla 'eventos'...")
    
    try:
        response = supabase.table("eventos").insert(test_data).execute()
        
        # Manejar diferentes formatos de respuesta de Supabase
        if hasattr(response, 'data') and response.data:
            logger.info(f"✅ Inserción exitosa! ID del evento: {response.data[0]['id']}")
            return
            
        if hasattr(response, 'error') and response.error:
            logger.error(f"❌ Error en Supabase: {response.error.message}")
            return
            
        logger.error("❌ Respuesta inesperada de Supabase")
        logger.debug(f"Respuesta completa: {response}")
        
    except Exception as e:
        logger.error(f"❌ Error durante la inserción: {str(e)}")

if __name__ == "__main__":
    main()
    logger.info("🏁 Ejecución completada")
