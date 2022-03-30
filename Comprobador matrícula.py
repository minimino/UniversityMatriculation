# Importamos los paquetes necesarios
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def inicio_sesion(driver):
    # Credenciales
    usuario = ""
    contr = ""
    
    sleep(2)
    driver.find_element_by_id("username").send_keys(usuario);
    form_contr = driver.find_element_by_id("password")
    form_contr.send_keys(contr);
    form_contr.send_keys(Keys.RETURN)
    # Necesariamente hemos iniciado sesión (si las credenciales son correctas)

# Valida la matrícula
def val_matricula():
    driver.execute_script("navegar('validacion')");
    sleep(2)
    driver.find_element_by_id("botonValidar").click()

# Busca plazas en la asignatura 'cod_asig' y grupo 'grupo'
def buscar_plaza(cod_asig, grupo):
    # Código del elemento que caracteriza el grupo y asignatura
    id_elem = "id_grupo_" + cod_asig + "_" + grupo
    # Cogemos el elemento
    elem = driver.find_element_by_id(id_elem)
    
    # Comprobamos si hay plazas disponibles en el grupo
    if elem.is_enabled():
        if not driver.find_element_by_id("collapse" + cod_asig).is_displayed():
            driver.find_element_by_id("cabeceraActividades" + cod_asig).click()
        
        sleep(1)
        elem.find_element_by_xpath('..').click()
        
        return True
    else:
        return False
        
def inicio(driver, asignaturas):
    # Esperamos a que se cargue
    # Seleccionamos la carrera de Física a tiempo completo (hay que seleccionar el padre del elemento
    sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/main/section/div/form/div[1]/div/div[2]/label').click()
    sleep(5)
    # cod_carrera = "0808"
    # driver.execute_script("document.getElementById('radioPlan1').setAttribute('value', '" + cod_carrera + "')");
    # driver.execute_script("navegar('datospersonales')");
    # driver.find_element_by_id("radioPlan1").find_element_by_xpath('..').click()

    # Avanzamos a la siguiente página hasta llegar a finalizar matrícula...
    # driver.execute_script("javascript:navegar('datospersonales')")
    while "Finalizar Automatrícula" not in driver.title:
        driver.find_element_by_id("btnsiguiente").click()
        
    # Volvemos a selección de grupos...
    driver.get("university matriculation page groups")

    # Recorremos cada asignatura y buscamos plaza...
    encontrada = False
    encontradas = []
    while not encontrada:
        # Indicamos estado
        print("Reiniciando bucle...")
        # Esperamos 30 segundos
        sleep(30)
        # Recargamos la página
        driver.refresh()
        # Por cada asignatura, buscamos plaza
        print("Buscando...")
        
        sleep(1)
        for asignatura in asignaturas.keys():
            existe_plaza = buscar_plaza(asignatura, asignaturas[asignatura])
            if existe_plaza:
                encontradas.append(asignatura)
                encontrada = existe_plaza
                
        for asignatura in encontradas:
            del asignaturas[asignatura]
    
    # Imprimimos las asignaturas de als que hemos encontrado plaza
    print("Asignaturas encontradas: ", encontradas)
        
    # Validamos la matrícula
    val_matricula()
    
    # Cargamos la página inicial
    driver.get("university matriculation page")
    # Volvemos a empezar
    inicio(driver, asignaturas)
        
# Seleccionamos el driver del navegador
driver = webdriver.Chrome()
# Cargamos la página
driver.get("university matriculation page")
# Iniciamos sesión
inicio_sesion(driver)
# Códigos de las asignaturas de las que buscamos plaza. Formato: Código : Grupo deseado
asignaturas = {"800533" : "200248"}
# Iniciamos el programa
inicio(driver, asignaturas)
