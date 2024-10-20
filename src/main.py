from metrics import get_transferred_and_time


if __name__ == "__main__":

    url= "https://es.wikipedia.org/wiki/Urano_(planeta)"

    metrics = get_transferred_and_time(url)

    print(metrics)
