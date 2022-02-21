from bs4 import BeautifulSoup
import requests


def find_flats(place, rent, living_space, number_of_rooms):
    url = f"https://www.immowelt.de/liste/{place}/wohnungen/mieten?ami={living_space}&d=true&pma={rent}&rmi={number_of_rooms}&sd=DESC&sf=TIMESTAMP&sp=1"
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    flat_cards = soup.find_all(class_="EstateItem-1c115")
    flats = []
    for flat_card in flat_cards:
        title = flat_card.find("h2").string
        location = flat_card.find(["i"], text="location").next_sibling.string
        description = flat_card.find(["i"], text="check").next_sibling.string
        rent_of_flat, living_space_of_flat, number_of_rooms_of_flat = [i.string for i in list(
            flat_card.find(class_="KeyFacts-efbce").children)]
        link_to_the_flat = flat_card.a["href"]
        flats.append({
            "title": title,
            "location": location,
            "description": description,
            "rent_of_flat": rent_of_flat,
            "living_space_of_flat": living_space_of_flat,
            "number_of_rooms_of_flat": number_of_rooms_of_flat,
            "link_to_flat": link_to_the_flat
        })
    print(flats)
    save_flats_to_text_file(flats)


def save_flats_to_text_file(flats):
    flats_string = ""
    for flat in flats:
        flats_string += f"{flat['title']}\n{flat['location']}\n{flat['description']}\n{flat['rent_of_flat']}\n{flat['living_space_of_flat']}\n{flat['number_of_rooms_of_flat']}\n{flat['link_to_flat']}\n\n"
    with open(f"{place}_flats.txt", "w") as f:
        f.write(flats_string)


if __name__ == '__main__':
        print(
            "Bitte geben sie bei Orten mit ü,ö oder ä den entsprechenden Umlaut an und bei den folgen Fragen einfache Zahlen!")
        place = input("Wo wollen Sie Ihre Wohnung mieten? \n").lower()
        rent = float(input("Was wollen Sie maximal zahlen?\n"))
        living_space = float(input("Wie groß soll die Wohnung mindestens seien?\n"))
        number_of_rooms = float(input("Wie viele Zimmer soll die Wohnung mindestens haben?\n"))
        find_flats(place, rent, living_space, number_of_rooms)

