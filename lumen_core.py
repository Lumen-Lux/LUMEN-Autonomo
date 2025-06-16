from supabase import create_client
import os
import time

def main():
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
