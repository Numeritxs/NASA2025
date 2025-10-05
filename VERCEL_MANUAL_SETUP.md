# 🔧 Configuración Manual de Vercel

Si Vercel no detecta automáticamente tu proyecto, sigue estos pasos:

## 📋 Configuración Manual en Vercel Dashboard

### 1. **Crear Nuevo Proyecto**
- Ve a [vercel.com](https://vercel.com)
- Haz clic en "New Project"
- Selecciona tu repositorio de GitHub

### 2. **Configuración del Framework**
- **Framework Preset:** `Next.js`
- **Root Directory:** `Frontend` ⚠️ **IMPORTANTE**
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Install Command:** `npm install`

### 3. **Variables de Entorno**
Agrega estas variables de entorno:
- `NEXT_PUBLIC_API_URL` = `/api`

### 4. **Configuración Avanzada**
En "Advanced" → "Build & Development Settings":
- **Node.js Version:** `18.x` o superior
- **Python Version:** `3.9`

## 🚀 Alternativa: Usar Vercel CLI

Si prefieres usar la línea de comandos:

```bash
# Instalar Vercel CLI
npm install -g vercel

# En el directorio del proyecto
vercel

# Seguir las instrucciones:
# - Link to existing project? No
# - Project name: nasa-exoplanet-app
# - Directory: Frontend
# - Framework: Next.js
```

## ⚙️ Configuración Específica para tu Proyecto

### Estructura Detectada:
```
NASA2025/
├── Frontend/          ← Vercel debe apuntar aquí
│   ├── package.json
│   ├── next.config.ts
│   └── src/
├── api/               ← Funciones serverless
│   ├── *.py
│   └── modelos/
└── vercel.json        ← Configuración personalizada
```

### Configuración Recomendada:
- **Framework:** Next.js
- **Root Directory:** `Frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Install Command:** `npm install`

## 🔍 Verificación Post-Deployment

Una vez desplegado, verifica estos endpoints:

1. **Frontend:** `https://tu-app.vercel.app`
2. **API Health:** `https://tu-app.vercel.app/api/health`
3. **API Predict:** `https://tu-app.vercel.app/api/predict`

## 🛠️ Solución de Problemas

### Error: "Build failed"
- Verifica que `Frontend/package.json` existe
- Asegúrate de que el Root Directory sea `Frontend`
- Revisa que todas las dependencias estén en `package.json`

### Error: "API not found"
- Verifica que el directorio `api/` esté en la raíz
- Asegúrate de que `vercel.json` esté configurado correctamente
- Revisa que los archivos `.py` tengan la clase `handler`

### Error: "Models not found"
- Verifica que `api/modelos/` contenga los archivos `.joblib`
- Asegúrate de que los modelos no excedan 50MB

## 📞 Si Necesitas Ayuda

Si sigues teniendo problemas:

1. **Revisa los logs** en el dashboard de Vercel
2. **Verifica la configuración** paso a paso
3. **Usa el script de verificación:** `python3 verify_deployment.py`
4. **Prueba con Vercel CLI** como alternativa

## ✅ Checklist Final

- [ ] Repositorio subido a GitHub
- [ ] Proyecto creado en Vercel
- [ ] Root Directory configurado como `Frontend`
- [ ] Variables de entorno configuradas
- [ ] Build exitoso
- [ ] API endpoints funcionando
- [ ] Frontend cargando correctamente

¡Con esta configuración manual debería funcionar perfectamente! 🎉
