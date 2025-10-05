# NASA 2025 Exoplanet Application - Vercel Deployment

## Descripción del Proyecto

Esta es una aplicación de exoplanetas que combina inteligencia artificial y simulación 3D para hacer comprensible y atractivo el descubrimiento de exoplanetas. Los usuarios pueden modificar parámetros físicos como masa, temperatura y densidad atmosférica para generar planetas potenciales. Un modelo de IA evalúa estas entradas para determinar si el resultado califica como exoplaneta e identifica su tipo.

## Estructura para Vercel

Este proyecto ha sido adaptado para funcionar en Vercel con las siguientes modificaciones:

### Frontend (Next.js)
- Ubicado en `Frontend/`
- Configurado para usar rutas API serverless
- Optimizado para deployment en Vercel

### Backend (Serverless Functions)
- Convertido de FastAPI a funciones serverless de Python
- Ubicado en `api/`
- Incluye los modelos de ML en `api/modelos/`

## Archivos de Configuración

- `vercel.json`: Configuración principal de Vercel
- `requirements.txt`: Dependencias de Python para las funciones serverless
- `.vercelignore`: Archivos a excluir del deployment

## Cómo Desplegar en Vercel

### Opción 1: Desde GitHub (Recomendado)

1. **Sube tu código a GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Conecta con Vercel:**
   - Ve a [vercel.com](https://vercel.com)
   - Inicia sesión con tu cuenta de GitHub
   - Haz clic en "New Project"
   - Selecciona tu repositorio
   - Vercel detectará automáticamente la configuración

3. **Configura las variables de entorno:**
   - En el dashboard de Vercel, ve a Settings > Environment Variables
   - Asegúrate de que `NEXT_PUBLIC_API_URL` esté configurado como `/api`

### Opción 2: CLI de Vercel

1. **Instala Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Despliega:**
   ```bash
   vercel
   ```

3. **Sigue las instrucciones en pantalla**

## Estructura de Archivos

```
NASA2025/
├── Frontend/                 # Aplicación Next.js
│   ├── src/
│   ├── package.json
│   └── next.config.ts
├── api/                      # Funciones serverless
│   ├── health.py
│   ├── predict.py
│   ├── classify-exoplanet.py
│   └── modelos/             # Modelos de ML
├── vercel.json              # Configuración de Vercel
├── requirements.txt         # Dependencias Python
└── package.json            # Scripts de build
```

## Endpoints API

- `GET /api/health` - Verificar estado de la API
- `POST /api/predict` - Predicción de tipo de exoplaneta
- `POST /api/classify-exoplanet` - Clasificación alternativa

## Características

- ✅ Frontend Next.js con visualización 3D
- ✅ Modelos de ML funcionando en serverless
- ✅ Soporte multiidioma (ES, EN, CA, GL)
- ✅ Juego interactivo de clasificación
- ✅ Generación de códigos QR
- ✅ Optimizado para Vercel

## Solución de Problemas

### Error de Modelos No Encontrados
- Verifica que los archivos en `api/modelos/` estén presentes
- Los archivos requeridos son:
  - `clf_exoplanet_type.joblib`
  - `metadata.joblib`
  - `clf_is_exoplanet.joblib` (opcional)

### Error de CORS
- Las funciones serverless incluyen headers CORS apropiados
- Si persisten problemas, verifica la configuración en `vercel.json`

### Error de Build
- Verifica que todas las dependencias estén en `requirements.txt`
- Asegúrate de que el tamaño de los modelos no exceda los límites de Vercel

## Límites de Vercel

- **Tamaño de función**: Máximo 50MB
- **Tiempo de ejecución**: Máximo 10 segundos (Hobby), 60 segundos (Pro)
- **Memoria**: Máximo 1024MB

Si los modelos de ML son muy grandes, considera:
- Usar modelos más pequeños
- Implementar lazy loading
- Usar un servicio externo para los modelos

## Desarrollo Local

Para desarrollo local con las funciones serverless:

```bash
# Instalar Vercel CLI
npm i -g vercel

# Ejecutar localmente
vercel dev
```

Esto simulará el entorno de Vercel localmente.
