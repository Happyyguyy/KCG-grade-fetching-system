import requests
from bs4 import BeautifulSoup
from json import dumps
import sqlite3
from pprint import pprint

# Constants
db = sqlite3.connect("db.db")
cur = db.cursor()

# Assembly constant
assembly = 71

main_html = "https://leg.colorado.gov"
leg_page = main_html + "/legislators"

page_request = requests.get(leg_page)
soup = BeautifulSoup(page_request.text, "html.parser")
online_table = soup.table


def printer(func):
    """Prints self.__doc__ on call, """
    def wrapper(*args, **kwargs):
        print(func.__doc__)
        returned = func(*args, **kwargs)
        print("\tDone!")
        return returned
    return wrapper


def timer(func):
    import time

    def wrapper(*args, **kwargs):
        t0 = time.clock()
        aa = func(*args, **kwargs)
        t1 = time.clock()
        t_delta = t0 - t1
        print(t_delta)
        return aa
    return wrapper


@printer
def get_leg_headers():
    """Getting headers..."""
    online_leg_headings = online_table.thead.descendants
    leg_headings = [item for item in online_leg_headings if item !=
                    "\n" and isinstance(item, str)]
    leg_headings.append("leg_page")
    return tuple(leg_headings)


@printer
def get_leg_data():
    "Getting legislator data..."
    leg_table = []
    online_leg_table = online_table.tbody.select("tr")
    for row in online_leg_table:
        extract = [item.strip("\n ")
                   for item in row.descendants if isinstance(item, str) and item != "\n"]
        extract.append(row.a['href'])
        leg_table.append(extract)
    return leg_table


@printer
def zip_dict(key_itr, values_itr):
    """Organizing data..."""
    ld = []

    for values in values_itr:
        ld.append(dict(zip(key_itr, values)))

    return ld


@printer
def dump_json(json_file, data):
    """Writing JSON file..."""
    json = dumps(data, indent=4)
    with open(json_file, "w") as file:
        file.write(json)


def split_name(data):
    """Splitting names..."""
    for row in data:
        full_name = row["Name"]
        row['last'], row['first'] = full_name.split(", ")
    return data


def get_potrait_link(href):
    leg_page = requests.get(main_html + href)
    leg_soup = BeautifulSoup(leg_page.text, "html.parser")
    return leg_soup.find_all("img")[1]["src"]


@printer
def append_portait_link(data):
    """Getting portrait links..."""
    for each in data:
        print(f"\tGetting link for: {each['Name']}")
        each["img_link"] = get_potrait_link(each["leg_page"])


@printer
def create_ids(data):
    """Creating IDs..."""
    for each in data:
        each["id"] = (str(assembly) + each["Title"].lower()[:3] +
                      each["last"].lower() + each["District"])

    return data


def create_data_file():

    data = get_leg_data()
    headers = get_leg_headers()

    data = zip_dict(headers, data)

    split_name(data)
    data = data[:5]
    append_portait_link(data)
    create_ids(data)
    pprint(data)

    for each in data:
        ID = each["id"]
        title = each["Title"]
        name = each["Name"]
        district = each["District"]
        party = each["Party"]
        phone_num = each["Capitol Phone #"]
        email = each["Email"]
        leg_page = each["leg_page"]
        last = each["last"]
        first = each["first"]
        img_link = each["img_link"]
        try:
            cur.execute(f"INSERT INTO legislators (ID,assembly,title,name,district,party,phone_num,email,leg_page,last,first,img_link) VALUES {(ID,assembly,title,name,district,party,phone_num,email,leg_page,last,first,img_link)}")
        except Exception as e:
            print(e)
            print("failed: ", ID)
        finally:
            pass

    # dump_json(json_file, data)
    db.commit()


if __name__ == '__main__':
    create_data_file()
