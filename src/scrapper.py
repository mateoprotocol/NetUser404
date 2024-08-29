import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


#-------------------------------------------- extracción urls
def get_url_base(url):
    parsed_url= urlparse(url)
    base_url= f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    return base_url

def scrape_webpage(url):
    response= requests.get(url)
    soup= BeautifulSoup(response.content, "html.parser") # extrae el contenido de la pagina web
    
    return soup

# Imágenes
def get_img_links(soup,resource_links):
    for img in soup.find_all("img"):
        resource_links.append(img.get("src"))

# Hojas de estilo (CSS)
def get_css_links(soup,resource_links):
    for link in soup.find_all("link", rel="stylesheet"):
        resource_links.append(link.get("href"))

# Scripts
def get_script_links(soup,resource_links):
    for script in soup.find_all("script"):
        if script.get("src"):
            resource_links.append(script.get("src"))

def format_resource_links(base_url, resource_links):
    resource_links= [f"{base_url}/{link}" for link in resource_links] 
    resource_links.insert(0,url) 
    resource_links= tuple(resource_links)

    return resource_links
#--------------------------------------------




if __name__ == "__main__":

    url= "https://calculos-energeticos.netlify.app/fotovoltaico"
    resource_links= []

    soup= scrape_webpage(url)

    img_links= get_img_links(soup,resource_links)
    css_links= get_css_links(soup,resource_links)
    script_links= get_script_links(soup,resource_links)

    base_url= get_url_base(url)

    resource_links= format_resource_links(base_url, resource_links)

