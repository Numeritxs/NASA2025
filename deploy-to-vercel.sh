#!/bin/bash

echo "🚀 Preparando deployment para Vercel..."

# Verificar que estamos en el directorio correcto
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: No se encontró vercel.json. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

# Verificar que el frontend existe
if [ ! -d "Frontend" ]; then
    echo "❌ Error: No se encontró el directorio Frontend."
    exit 1
fi

# Verificar que las funciones API existen
if [ ! -d "api" ]; then
    echo "❌ Error: No se encontró el directorio api."
    exit 1
fi

echo "✅ Estructura del proyecto verificada"

# Instalar dependencias del frontend
echo "📦 Instalando dependencias del frontend..."
cd Frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias del frontend"
    exit 1
fi
cd ..

echo "✅ Dependencias instaladas"

# Verificar que los modelos están presentes
echo "🤖 Verificando modelos de ML..."
if [ ! -f "api/modelos/clf_exoplanet_type.joblib" ]; then
    echo "❌ Error: Modelo clf_exoplanet_type.joblib no encontrado"
    exit 1
fi

if [ ! -f "api/modelos/metadata.joblib" ]; then
    echo "❌ Error: Modelo metadata.joblib no encontrado"
    exit 1
fi

echo "✅ Modelos de ML verificados"

# Crear archivo de configuración para Vercel
echo "⚙️ Configurando Vercel..."

# Verificar si Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "📥 Instalando Vercel CLI..."
    npm install -g vercel
fi

echo "🎯 Configuración completada. Ahora puedes:"
echo ""
echo "1. Subir tu código a GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for Vercel deployment'"
echo "   git push origin main"
echo ""
echo "2. O usar Vercel CLI:"
echo "   vercel"
echo ""
echo "3. O conectar manualmente en vercel.com:"
echo "   - Framework Preset: Next.js"
echo "   - Root Directory: Frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: .next"
echo ""
echo "✅ ¡Todo listo para deployment!"
