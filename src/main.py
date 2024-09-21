from scrapper import get_all_urls
from metrics import get_metrics


if __name__ == "__main__":

    #url= "https://calculos-energeticos.netlify.app/fotovoltaico"
    url = "https://www.eltiempo.com"
    resource_links= get_all_urls(url)
    metrics = get_metrics(*resource_links)

    print(metrics)
