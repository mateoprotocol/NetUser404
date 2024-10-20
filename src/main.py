from metrics import get_transferred_and_time


if __name__ == "__main__":

    url= "https://calculos-energeticos.netlify.app/fotovoltaico"

    metrics = get_transferred_and_time(url)

    print(metrics)
