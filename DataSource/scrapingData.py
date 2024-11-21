#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Chemin du dossier de téléchargement
download_folder = "/Users/pro/Desktop/DataSource"

# Créer le dossier s'il n'existe pas
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Options de Chrome
chrome_options = Options()
prefs = {"download.default_directory" : download_folder}
chrome_options.add_experimental_option("prefs", prefs)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://statistics.btselem.org/en/all-fatalities/by-date-of-incident?section=overall&tab=overview")

try:
    # Attendre que le bouton soit chargé et visible
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#overall > div > div > div > div:nth-child(1) > div > div.v-card__actions.mt-auto.d-flex.justify-space-between > div:nth-child(2) > button"))
    )

    download_button.click()
    print("Bouton cliqué")

    # Attendre que le fichier téléchargé apparaisse dans le dossier de téléchargement
    timeout = 30  # Délai d'attente en secondes
    start_time = time.time()
    previous_file_count = len([filename for filename in os.listdir(download_folder) if filename.endswith('.xlsx')])

    while True:
        current_file_count = len([filename for filename in os.listdir(download_folder) if filename.endswith('.xlsx')])

        if current_file_count > previous_file_count:
            print("Nouveau fichier téléchargé.")
            break

        if time.time() - start_time > timeout:
            print("Timeout atteint. Aucun fichier téléchargé.")
            break

        time.sleep(1)  # Attendre une seconde

    # Identifier le fichier le plus récent dans le dossier de téléchargement
    latest_file = max([os.path.join(download_folder, f) for f in os.listdir(download_folder)], key=os.path.getctime)

    # Définir le nouveau nom pour le fichier téléchargé
    new_file_name = os.path.join(download_folder, "PKForces.xlsx")

    # Remplacer le fichier s'il existe déjà
    if os.path.exists(new_file_name):
        os.remove(new_file_name)

    # Renommer le fichier téléchargé
    os.rename(latest_file, new_file_name)

    print("Fichier renommé et enregistré sous:", new_file_name)

finally:
    # Fermer le navigateur
    driver.quit()


# In[ ]:




