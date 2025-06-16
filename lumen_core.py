from supabase import create_client
import os
import requests
import time
import sys

def send_telegram(message):
    try:
        token = os.environ['TELEGRAM_TOKEN']
        chat_id = os.environ['TELEGRAM_CHAT_ID']
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Error Telegram: {str(e)}", file=sys.stderr)
        return False

def main():
    try:
        print("🚀 Iniciando LUMEN Core...")
        
        # Verificar variables
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            error_msg = f"❌ Variables faltantes: {', '.join(missing)}"
            print(error_msg, file=sys.stderr)
            send_telegram(error_msg)
            return sys.exit(1)
            
        # Conectar a Supabase
        supabase = create_client(os.environ['SUPABASE_URL'], 
                                os.environ['SUPABASE_KEY'])
        print("✅ Conexión a Supabase establecida")
        
        # Insertar evento con manejo de errores
        try:
            evento = {
                "tipo": "inicio",
                "detalle": f"LUMEN activado - {time.ctime()}"
            }
            response = supabase.table("eventos").insert(evento).execute()
            
            if response.error:
                raise Exception(f"Supabase error: {response.error.message}")
                
            print("✅ Evento registrado en base de datos")
            
        except Exception as db_error:
            error_msg = f"❌ Error en base de datos: {str(db_error)}"
            print(error_msg, file=sys.stderr)
            send_telegram(error_msg)
            return sys.exit(1)
        
        # Notificar por Telegram
        telegram_msg = f"🚀 LUMEN Activado\n\n✅ Núcleo operativo\n📅 {time.ctime()}"
        if send_telegram(telegram_msg):
            print("✅ Notificación enviada por Telegram")
        
        print("🏁 Ejecución completada exitosamente")
        return sys.exit(0)
        
    except Exception as e:
        error_msg = f"🔥 ERROR CRÍTICO: {str(e)}"
        print(error_msg, file=sys.stderr)
        send_telegram(f"⚠️ FALLO EN LUMEN CORE:\n{str(e)}")
        return sys.exit(1)

if __name__ == "__main__":
    main()
