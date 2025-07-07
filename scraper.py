from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import os
import time
import re
from datetime import datetime
import random

# Configurar Chrome (con tiempos más lentos)
s = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=s)
wait = WebDriverWait(driver, 30)  # Tiempo de espera más largo

# Ir a la web con mayor tiempo de espera inicial
driver.get('https://sentencias.scba.gov.ar/')
time.sleep(5)  # Espera inicial más larga

# Configuración para scraping lento
TIEMPO_ESPERA_MIN = 2    # Tiempo mínimo entre acciones
TIEMPO_ESPERA_MAX = 5    # Tiempo máximo entre acciones
TIEMPO_ENTRE_DOCS = 5    # Tiempo entre documentos
TIEMPO_ENTRE_PAGS = 7    # Tiempo entre páginas

def pausa_aleatoria(min_t=TIEMPO_ESPERA_MIN, max_t=TIEMPO_ESPERA_MAX):
    """Pausa aleatoria entre min_t y max_t segundos"""
    tiempo = random.uniform(min_t, max_t)
    time.sleep(tiempo)

# Crear carpeta base si no existe
carpeta_base = "resoluciones"
os.makedirs(carpeta_base, exist_ok=True)

def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

# Solicitar parámetros de búsqueda al usuario
print("\n📅 Ingrese los parámetros de búsqueda:")
while True:
    fecha_desde = input("Fecha desde (formato DD/MM/AAAA): ")
    if validar_fecha(fecha_desde):
        break
    print("Formato de fecha incorrecto. Use DD/MM/AAAA")

while True:
    fecha_hasta = input("Fecha hasta (formato DD/MM/AAAA): ")
    if validar_fecha(fecha_hasta):
        break
    print("Formato de fecha incorrecto. Use DD/MM/AAAA")

texto_busqueda = input("Texto a buscar: ")

def seleccionar_registro():
    # Hacer clic en el contenedor de registros
    wait.until(EC.element_to_be_clickable((By.ID, 'select2-Registros-container'))).click()
    pausa_aleatoria()
    
    # Esperar a que se carguen las opciones
    registros_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'select2-results__option')]")))
    
    # Filtrar las opciones disponibles
    registros = [el.text for el in registros_elements if el.text.strip() != ""]
    
    # Mostrar las opciones disponibles (segundo y tercer elemento)
    print("\n📜 Registros disponibles:")
    if len(registros) >= 3:
        print(f"2. {registros[1]} (Resoluciones)")
        print(f"3. {registros[2]} (Sentencias)")
    else:
        print("No hay suficientes registros disponibles.")
        return None
    
    seleccion = None
    while seleccion not in ['2', '3']:
        seleccion = input("\nSeleccione 2 o 3 para elegir el registro (0 para terminar): ")
        if seleccion == '0':
            return None
        elif seleccion not in ['2', '3']:
            print("Opción no válida. Intente de nuevo.")
    
    # Hacer clic en el registro seleccionado
    index = int(seleccion) - 1  # Convertir a índice (0 o 1)
    wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[contains(@class, 'select2-results__option')])[{index + 1}]"))).click()
    pausa_aleatoria()
    
    # Crear carpeta específica según la opción seleccionada
    tipo_registro = "resoluciones" if seleccion == '2' else "sentencias"
    carpeta_registro = os.path.join(carpeta_base, tipo_registro)
    os.makedirs(carpeta_registro, exist_ok=True)
    
    return tipo_registro  # Retornar el tipo de registro seleccionado

def seleccionar_organismos():
    # Hacer clic en el contenedor de organismos
    wait.until(EC.element_to_be_clickable((By.ID, 'select2-Organismos-container'))).click()
    pausa_aleatoria()
    organismos_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'select2-results__option')]")
    organismos = [el.text for el in organismos_elements[1:] if el.text.strip() != ""]
    driver.find_element(By.ID, 'select2-Organismos-container').click()
    pausa_aleatoria()
    
    print("\n📌 Organismos disponibles:")
    for i, org in enumerate(organismos, 1):
        print(f"{i}. {org}")
    
    seleccionados = []
    while True:
        try:
            opcion = input("\nSeleccione un número de organismo (0 para terminar): ")
            if opcion == '0':
                break
            idx = int(opcion) - 1
            if 0 <= idx < len(organismos):
                seleccionados.append(organismos[idx])
                print(f"✔ Añadido: {organismos[idx]}")
            else:
                print("Número fuera de rango")
        except ValueError:
            print("Ingrese un número válido")
    
    return seleccionados

def buscar_y_guardar(organismo, carpeta_registro):
    try:
        nombre_carpeta_organismo = re.sub(r'[<>:"/\\|?*]', '', organismo).strip()
        carpeta_organismo = os.path.join(carpeta_registro, nombre_carpeta_organismo)
        os.makedirs(carpeta_organismo, exist_ok=True)
        
        print(f"\n🔍 Procesando organismo: {organismo}")
        pausa_aleatoria()
        
        # Seleccionar organismo
        wait.until(EC.element_to_be_clickable((By.ID, 'select2-Organismos-container'))).click()
        pausa_aleatoria()
        organismo_xpath = f"//li[contains(@class, 'select2-results__option') and normalize-space(text())='{organismo}']"
        wait.until(EC.element_to_be_clickable((By.XPATH, organismo_xpath))).click()
        pausa_aleatoria()
        
        # Ingresar fechas
        input_fecha = wait.until(EC.element_to_be_clickable((By.ID, 'idFeDesde')))
        input_fecha.clear()
        for char in fecha_desde:
            input_fecha.send_keys(char)
            time.sleep(0.3)  # Más lento al escribir
        pausa_aleatoria()
        
        input_fecha_hasta = wait.until(EC.element_to_be_clickable((By.ID, 'idFeHasta')))
        input_fecha_hasta.clear()
        for char in fecha_hasta:
            input_fecha_hasta.send_keys(char)
            time.sleep(0.3)
        pausa_aleatoria()
        
        # Ingresar texto
        input_texto = wait.until(EC.element_to_be_clickable((By.ID, 'idTexto')))
        input_texto.clear()
        input_texto.send_keys(texto_busqueda)
        pausa_aleatoria()
        
        # Buscar
        wait.until(EC.element_to_be_clickable((By.ID, 'btnBuscar'))).click()
        wait.until(EC.presence_of_element_located((By.ID, 'grid-ListadoRegistros')))
        time.sleep(5)  # Espera larga después de buscar
        
        pagina = 1
        documentos_guardados = 0
        
        while True:
            print(f"  🔄 Procesando página {pagina}...")
            
            botones_documento = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Documento')]")))
            if not botones_documento:
                print("    ❌ No hay documentos en esta página.")
                break
            
            for i in range(len(botones_documento)):
                try:
                    # Re-localizar los botones
                    botones = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Documento')]")))
                    if i >= len(botones):
                        break
                    
                    botones[i].click()
                    time.sleep(TIEMPO_ENTRE_DOCS * 0.6)  # Espera antes de procesar
                    
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-body")))
                    time.sleep(2)  # Espera adicional
                    card_bodies = driver.find_elements(By.CLASS_NAME, "card-body")
                    texto_completo = "\n".join([el.text for el in card_bodies if el.text.strip() != ""])
                    
                    parrafos = texto_completo.strip().split("\n")
                    nombre_archivo = re.sub(r'[<>:"/\\|?*]', '', parrafos[1]) if len(parrafos) > 1 else f"documento_p{pagina}_{i+1}"
                    nombre_archivo = nombre_archivo[:100]
                    ruta = os.path.join(carpeta_organismo, f"{nombre_archivo}.txt")
                    
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(texto_completo)
                    documentos_guardados += 1
                    print(f"    ✅ Guardado: {ruta}")
                    
                    # Cerrar modal con más tiempo
                    wait.until(EC.element_to_be_clickable((By.ID, "btnCerrarModal"))).click()
                    time.sleep(TIEMPO_ENTRE_DOCS)
                    
                except Exception as e:
                    print(f"    ⚠️ Error procesando documento {i+1} en página {pagina}: {str(e)[:100]}...")
                    continue
            
            # Pasar de página
            try:
                siguiente_btn = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#grid-ListadoRegistros_next a.page-link")))
                
                if 'disabled' in siguiente_btn.find_element(By.XPATH, "./..").get_attribute("class"):
                    print("    🏁 No hay más páginas disponibles.")
                    break
                
                driver.execute_script("arguments[0].scrollIntoView();", siguiente_btn)
                time.sleep(3)  # Espera antes de hacer clic
                siguiente_btn.click()
                
                wait.until(EC.staleness_of(botones_documento[0]))
                wait.until(EC.presence_of_element_located((By.ID, 'grid-ListadoRegistros')))
                time.sleep(TIEMPO_ENTRE_PAGS)  # Espera larga entre páginas
                pagina += 1
                
            except Exception as e:
                print(f"    ⚠️ Error al intentar pasar página: {str(e)[:100]}...")
                break
        
        print(f"  ✔️ Organismo completado. Documentos guardados: {documentos_guardados}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error procesando organismo {organismo}: {str(e)[:100]}...")
        return False

# Procesamiento principal
try:
    tipo_registro = seleccionar_registro()  # Llamar a la función para seleccionar el registro
    organismos_a_procesar = seleccionar_organismos()

    if not organismos_a_procesar:
        print("\n⚠️ No se seleccionaron organismos para procesar")
    else:
        print(f"\n🔄 Comenzando procesamiento de {len(organismos_a_procesar)} organismo(s) seleccionado(s)")
        for organismo in organismos_a_procesar:
            if not buscar_y_guardar(organismo, os.path.join(carpeta_base, tipo_registro)):
                print(f"⚠️ Continuando con el siguiente organismo después de error en {organismo}")
            time.sleep(5)  # Espera larga entre organismos

    print("\n🏁 Proceso completado.")
finally:
    # Asegurar que el driver se cierre
    driver.quit()
