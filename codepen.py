from csv import DictReader, DictWriter

csv = []


with open("leglist.csv") as file:
    dict_reader = DictReader(file)
    with open("leglist_new.csv", "w") as write_file:
        fieldnames = ["title", "name", "district", "party", "phone_num", "email", "leg_page", "last", "first", "img_link", "id"]
        writer = DictWriter(write_file, fieldnames=fieldnames, delimiter=",", lineterminator="\n")
        writer.writeheader()

        for row in dict_reader:
            id = row["title"][:3].lower() + row["last"].lower() + row["district"]
            writer.writerow({"title":row['title'], "name": row["first"] + " " + row["last"], "district": row["district"], "party": row["party"], "phone_num": row["phone_num"], "email": row["email"], "leg_page": row["link"], "last": row["last"], "first": row["first"], "img_link": row["img_link"], "id": id})
# print(csv)
