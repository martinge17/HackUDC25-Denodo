from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import time
import shutil

class TestUntitled:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # Opcional: Agregar opciones para debugging
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 25)
        self.driver.implicitly_wait(3)
      
    def teardown_method(self, method):
        self.driver.quit()
        # Limpiar perfil temporal
        shutil.rmtree("./temp_chrome_profile", ignore_errors=True)

    def test_untitled(self):
        try:
            # Paso 1: Cargar la URL y hacer login una sola vez
            self.driver.get("http://localhost:9090/denodo-design-studio/#/")
            print("Título de la página:", self.driver.title)
            
            # Paso 2: Login
            username = self.wait.until(EC.visibility_of_element_located((By.NAME, "user")))
            username.send_keys("admin")
            
            password = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
            password.send_keys("admin" + Keys.ENTER)
            
            # Definir carpeta de archivos VQL y filtrar solo los .vql
            carpeta = os.path.abspath("./vql_output")
            archivos = [f for f in os.listdir(carpeta) if f.endswith('.vql')]
            
            if not archivos:
                print("No se encontraron archivos .vql en la carpeta especificada.")
                return
            
            # Iterar sobre cada archivo
            for idx, archivo in enumerate(archivos):
                ruta_archivo = os.path.join(carpeta, archivo)
                print(f"Subiendo el archivo: {ruta_archivo}")
                
                # Paso 3: Menú FILE
                file_menu = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '.menu\\.file\\$Menu > .rc-menu-submenu-title')
                ))
                file_menu.click()
                
                # Paso 4: Menú IMPORT
                import_option = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '.rc-menu-item.Navbar_menuItem_______47.menu\\.file\\.import\\$Menu')
                ))
                import_option.click()
                time.sleep(1)
                
                # Paso 7: Selección de base de datos
                db_dropdown = self.wait.until(EC.element_to_be_clickable((By.NAME, "databaseName")))
                db_dropdown.click()
                time.sleep(1)
                option = self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//option[. = 'jjoo']")
                ))
                option.click()
                time.sleep(1)
                
                # Paso 8: Botón inicial de importación
                primary_button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".Button___primary_______76")
                ))
                primary_button.click()
                time.sleep(1)
                
                # Esperar a que aparezca el input de archivo
                file_input = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[type='file']")
                ))
                time.sleep(1)
                
                # Enviar la ruta del archivo VQL
                file_input.send_keys(ruta_archivo)
                time.sleep(1)
                
                # Seleccionar el botón de confirmación según corresponda:
                confirm_button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".Button_______60.Popup_button_______194.Button___primary_______76")
                ))
                time.sleep(1)
                confirm_button.click()

                confirm_button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".Button_text_______61.Text_______201.Text___actionSecondary_______229")
                ))
                time.sleep(1)
                confirm_button.click()
                
        except Exception as e:
            self.driver.save_screenshot(f"error_{int(time.time())}.png")
            raise e
        
if __name__ == "__main__":
    test_app = TestUntitled()
    test_app.setup_method(None)  # Inicializa el navegador
    try:
        test_app.test_untitled()  # Ejecuta los pasos de la prueba
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
    finally:
        test_app.teardown_method(None)  # Cierra el navegador y limpia
