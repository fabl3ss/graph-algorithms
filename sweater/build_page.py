from bs4 import BeautifulSoup
import json


def build_page():
    paths = json.load(open('options/properties.json', ))['html_paths'][0]
    main_soup = BeautifulSoup(open(paths['head_html'], 'r').read(), 'lxml')
    network_soup = BeautifulSoup(open(paths['network_html'], 'r').read(), 'lxml')

    main_soup.body.append(network_soup.find_all('script')[1])

    with open("sweater/templates/output.html", "w") as file:
        file.write(str(main_soup))
