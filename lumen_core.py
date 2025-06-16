from supabase import create_client
import os
import time

def main():
    
    print("🔍 Verificando variables de entorno...")
    print("SUPABASE_URL:", bool(os.environ.get('SUPABASE_URL')))
    print("SUPABASE_KEY:", bool(os.environ.get('SUPABASE_KEY')))
    
    # Conectar a Supabase
    supabase = create_client(
        os.environ['SUPABASE_URL'],
        os.environ['SUPABASE_KEY']
    )
    
    # Registrar evento de inicio
    evento = {
        "tipo": "inicio",
        "detalle": f"LUMEN activado - {time.ctime()}"
    }
    supabase.table("eventos").insert(evento).execute()
    print("✅ Núcleo ético operativo")

if __name__ == "__main__":
    main()
