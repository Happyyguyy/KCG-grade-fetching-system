from PIL import Image, ImageDraw, ImageFont
import json
import sqlite3
import requests
import time
import textwrap


# init sqlite3 connection
db = sqlite3.connect("db.db")
cur = db.cursor()

# Dates
date = "Updated: " + time.strftime("%B %d, %Y")
shortDate = time.strftime("_%m_%d_%Y")

# Assembly constant
assembly = 71

def download_img(URL=None):
    # Get img from webpage
    r = requests.get(URL)

    with open("temp.jpg", "wb") as img:
        img.write(r.content)
    thing = Image.open("temp.jpg")
    return thing


def create_card(id, voting, rhetoric, donation):

    # Get Template Configuration
    with open("template.config", "rb") as config_file:
        config = json.load(config_file)

    # Get legislator details
    cur.execute(f"SELECT name, district, title, img_link FROM legislators WHERE id= '{id}';")
    name, district, title, img_link = cur.fetchone()

    # Create canvas from template with image
    template = Image.open("kcggrading_blank.png")
    canvas = Image.new("RGBA", template.size, (255,255,255,255))
    portrait = download_img(img_link)


    # calculate aspect ratio height
    new_dimensions = config["portrait_scale"]
    scale_multiplier = new_dimensions[0] / portrait.size[0]
    scaled_height = int(portrait.size[1] * scale_multiplier)

    # scale the portrait with correct aspect ratio
    scaled_portrait = portrait.resize((config["portrait_scale"][0],scaled_height), Image.ANTIALIAS)

    # Create canvas to post grades onto
    canvas.paste(scaled_portrait, (58, 62))
    canvas.paste(template, (0,0), template)


    txt = Image.new("RGBA", template.size, (255,255,255,0))
    d = ImageDraw.Draw(txt)

    name_fnt = ImageFont.truetype(config["font"]["name"], config["font_size"]["m"])
    district_fnt = ImageFont.truetype(config["font"]["district"], config["font_size"]["s"])
    updated_fnt = ImageFont.truetype(config["font"]["district"], config["font_size"]["xs"])
    grade_fnt = ImageFont.truetype(config["font"]["bold"], config["font_size"]["l"])

    # Draw grades
    d.text(config["location"]["voting"], voting, font=grade_fnt, fill=tuple(config["color"]["font_1"]))
    d.text(config["location"]["rhetoric"], rhetoric, font=grade_fnt, fill=tuple(config["color"]["font_1"]))
    d.text(config["location"]["donation"], donation, font=grade_fnt, fill=tuple(config["color"]["font_1"]))

    # Draw district
    if title == "Senator":
        district_str = "Senate District " + str(district)
    if title == "Representative":
        district_str = "House District " + str(district)
    d.text(config["location"]["district"], district_str, font=district_fnt, fill=tuple(config["color"]["font_1"]))

    # Draw names
    if len(name) <= 30:
        wrapped_name = textwrap.wrap(name, width=16)

        # Draw one line name
        if len(wrapped_name) == 1:
            line_1 = wrapped_name[0]
            d.text((553, 112), line_1, font=name_fnt, fill=tuple(config["color"]["font_1"]))

        # Draw Two lines
        elif len(wrapped_name) == 2:
                line_1, line_2 = wrapped_name
                d.text((553, 89), line_1, font=name_fnt, fill=tuple(config["color"]["font_1"]))
                d.text((553, 135), line_2, font=name_fnt, fill=tuple(config["color"]["font_1"]))
    elif len(name) > 30:
        raise ValueError("Name is too long. Shorten the name or ask project manager to patch program")

    # Draw updated tag
    updated_location = config["location"]["updated"]
    updated_location[0] -= d.textsize(date, font=updated_fnt)[0]
    d.text(updated_location, date, font=updated_fnt, fill=(tuple(config["color"]['font_2'])))

    # Output composite image
    output = Image.alpha_composite(canvas, txt)
    # output.show()

    return output


def save_card(card, directory):
    card.save(directory)


def batch_create(destination):
    cur.execute(f"SELECT id, voting, rhetoric, donations FROM grades WHERE assembly LIKE '{assembly}%'")
    for row in cur.fetchall():
        cur2 = db.cursor()
        cur2.execute(f"SELECT last, first, house, district FROM legislators WHERE id='{row[0]}'")
        file_name = cur2.fetchone().join("_") + shortDate + ".jpg"
        save_location = destination + file_name
        report_card = create_card(*row)
        save_card(report_card, save_location)


if __name__ == '__main__':
    cur.execute("SELECT id, voting, rhetoric, donations FROM grades WHERE id ='71repmichaelson jenet30' OR id = '71repwinkler34'")
    for row in cur.fetchall():
        thing = create_card(*row)
        thing.show()
