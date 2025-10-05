#!/usr/bin/env python3
"""
Script para verificar que el proyecto esté listo para deployment en Vercel
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica que un archivo exista"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NO ENCONTRADO")
        return False

def check_directory_exists(dirpath, description):
    """Verifica que un directorio exista"""
    if os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} - NO ENCONTRADO")
        return False

def main():
    print("🔍 Verificando preparación para deployment en Vercel...\n")
    
    all_good = True
    
    # Verificar archivos de configuración principales
    print("📋 Archivos de configuración:")
    config_files = [
        ("vercel.json", "Configuración de Vercel"),
        ("requirements.txt", "Dependencias de Python"),
        (".vercelignore", "Archivos a ignorar en Vercel"),
        ("package.json", "Configuración de Node.js"),
    ]
    
    for filepath, description in config_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print("\n📁 Estructura de directorios:")
    directories = [
        ("Frontend/", "Directorio del frontend Next.js"),
        ("api/", "Directorio de funciones serverless"),
        ("api/modelos/", "Directorio de modelos de ML"),
    ]
    
    for dirpath, description in directories:
        if not check_directory_exists(dirpath, description):
            all_good = False
    
    print("\n🤖 Modelos de Machine Learning:")
    model_files = [
        ("api/modelos/clf_exoplanet_type.joblib", "Modelo clasificador de tipos"),
        ("api/modelos/metadata.joblib", "Metadatos del modelo"),
        ("api/modelos/clf_is_exoplanet.joblib", "Modelo clasificador binario"),
    ]
    
    for filepath, description in model_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print("\n🔧 Funciones serverless:")
    api_files = [
        ("api/__init__.py", "Inicializador del paquete API"),
        ("api/health.py", "Endpoint de salud"),
        ("api/predict.py", "Endpoint de predicción"),
        ("api/classify-exoplanet.py", "Endpoint de clasificación"),
    ]
    
    for filepath, description in api_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print("\n🌐 Frontend:")
    frontend_files = [
        ("Frontend/package.json", "Configuración del frontend"),
        ("Frontend/next.config.ts", "Configuración de Next.js"),
        ("Frontend/src/app/page.tsx", "Página principal"),
    ]
    
    for filepath, description in frontend_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Verificar tamaño de los modelos
    print("\n📊 Verificación de tamaños:")
    modelos_dir = Path("api/modelos")
    if modelos_dir.exists():
        total_size = sum(f.stat().st_size for f in modelos_dir.glob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        print(f"Tamaño total de modelos: {size_mb:.2f} MB")
        
        if size_mb > 50:
            print("⚠️  ADVERTENCIA: Los modelos exceden 50MB (límite de Vercel)")
            print("   Considera usar modelos más pequeños o un servicio externo")
        else:
            print("✅ Tamaño de modelos dentro del límite de Vercel")
    
    print("\n" + "="*50)
    
    if all_good:
        print("🎉 ¡Todo listo para deployment en Vercel!")
        print("\n📝 Próximos pasos:")
        print("1. Sube tu código a GitHub")
        print("2. Conecta el repositorio con Vercel")
        print("3. Configura las variables de entorno si es necesario")
        print("4. ¡Despliega!")
    else:
        print("❌ Hay problemas que deben resolverse antes del deployment")
        print("Revisa los archivos marcados como faltantes")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
