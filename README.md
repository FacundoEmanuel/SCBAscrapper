
# 🏛️ SCBA Scraper - Primera Instancia

Este script automatiza la descarga de resoluciones y sentencias judiciales publicadas en el sitio de la Suprema Corte de Justicia de la Provincia de Buenos Aires: [https://sentencias.scba.gov.ar](https://sentencias.scba.gov.ar)

## ⚙️ Requisitos

- Python 3.8 o superior
- Google Chrome instalado
- `chromedriver.exe` (debe coincidir con la versión de Chrome)
- Paquetes de Python:

```bash
pip install selenium
```

## 📁 Estructura de Carpetas

Al ejecutar el script, se crea una estructura de carpetas como la siguiente:

```
sentencias judiciales/
├── resoluciones/
│   └── [organismo]/
│       └── documento_x.txt
├── sentencias/
│   └── [organismo]/
│       └── documento_y.txt
```

## 🧠 ¿Qué hace el script?

1. Abre el sitio de la SCBA.
2. Solicita al usuario:
   - Fecha desde y hasta (formato DD/MM/AAAA).
   - Texto a buscar.
   - Registro (Resoluciones o Sentencias).
   - Organismos a consultar.
3. Realiza búsquedas por organismo, extrae el texto completo de cada documento, lo guarda como `.txt` y lo organiza en carpetas.
4. Simula pausas humanas entre acciones para evitar ser bloqueado.
5. Maneja errores comunes y modales que podrían interrumpir el scraping.

## 🚀 Cómo usar

1. Asegurate de tener `chromedriver.exe` en el mismo directorio que el script.
2. Ejecutá el script:

```bash
python SCBA_Scraper_Primera\ instancia.py
```

3. Ingresá los datos requeridos por consola.

## 🛑 Advertencias

- Este script accede a datos públicos, pero **respetá siempre los términos de uso del sitio**.
- Su uso intensivo puede generar bloqueos temporales si no se respetan los tiempos de espera.
- Está pensado para un uso académico, profesional o de investigación, **no para reventa o explotación comercial** de la información.

## 🧩 Funciones destacadas

- `seleccionar_registro()` → permite elegir entre resoluciones y sentencias.
- `seleccionar_organismos()` → permite seleccionar múltiples organismos judiciales.
- `buscar_y_guardar()` → realiza la búsqueda, descarga y guarda los documentos por organismo y página.
- `cerrar_modal()` → cierra modales emergentes automáticamente o con un clic alternativo.

## 📌 Autor

Facundo Emanuel Gómez  
Abogado - Automatización jurídica y análisis judicial

---

> Si querés adaptar este scraper a otros fueros, sitios o formatos, podés reutilizar su arquitectura base con mínimos cambios.
