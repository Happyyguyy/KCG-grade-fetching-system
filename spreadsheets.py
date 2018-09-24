import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import sqlite3
import time

# Init sqlite3
db = sqlite3.connect("db.db")
cur = db.cursor()

# auth for gspread
scopes = ["https://spreadsheets.google.com/feeds",
          "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "KCG Legislator Report Card-fbc798c310a9.json", scopes)

gc = gspread.authorize(creds)

# Config for spreadsheet
sheet_name = "Copy of Co Leg Grades"
file = gc.open(sheet_name)
sen_sheet = file.worksheet("Senators")
rep_sheet = file.worksheet("Representatives")

# Assembly config
assembly = 71

# Data Validation: list of columns for headings. If any don't exist will throw error
try:
    sen_cols = {
        "id": sen_sheet.find("id").col,
        "assembly": sen_sheet.find("Assembly").col,
        "title": sen_sheet.find("title").col,
        "first": sen_sheet.find("first").col,
        "last": sen_sheet.find("last").col,
        "district": sen_sheet.find("District").col,
        "voting": sen_sheet.find("Voting").col,
        "donation": sen_sheet.find("Donation").col,
        "rhetoric": sen_sheet.find("Rhetoric").col,
        "updated": sen_sheet.find("last_updated").col
        }

    rep_cols = {
        "id": rep_sheet.find("id").col,
        "assembly": rep_sheet.find("Assembly").col,
        "title": rep_sheet.find("title").col,
        "first": rep_sheet.find("first").col,
        "last": rep_sheet.find("last").col,
        "district": rep_sheet.find("District").col,
        "voting": rep_sheet.find("Voting").col,
        "donation": rep_sheet.find("Donation").col,
        "rhetoric": rep_sheet.find("Rhetoric").col,
        "updated": rep_sheet.find("last_updated").col
        }
except gspread.exceptions.CellNotFound:
    raise IndexError("Fix headings\nThe spreadsheet isn't formatted correctly\nMake sure both sheets include headings: id, Assembly, title, first, last, District, Voting, Rhetoric, Donation, and last_updated\nCASE MATTERS && SPACES MATTER\nDONT LEAVE TRAILING SPACES")


def format_data(data):
    '''Format imported data '''
    
    formatted = []
    for each in data:
        # print(each)
        item_dict = {}
        item_dict["id"] = str(each["Assembly"]) + each["title"][:3].lower() + each["last"].lower() + str(each["District"])
        item_dict["Donation"] = each["Donation"]
        item_dict["Rhetoric"] = each["Rhetoric"]
        item_dict["Voting"] = each["Voting"]
        item_dict["last_updated"] = each["last_updated"]
        formatted.append(item_dict)
    return formatted


def save_grades(data):
    for row in data:
        try:
            cur.execute(f'INSERT INTO grades (id, voting, rhetoric, donations, last_updated) VALUES {(row["id"],row["Voting"],row["Rhetoric"],row["Donation"],row["last_updated"])}')
        except sqlite3.IntegrityError:
            cur.execute(f"UPDATE grades SET voting = '{row['Voting']}', rhetoric = '{row['Rhetoric']}', donations = '{row['Donation']}', last_updated = '{row['last_updated']}' WHERE id = '{row['id']}';")
    db.commit()
    return data


def update_data(id, voting, rhetoric, donation):
    '''pushes data to gspread'''

    # Get some data from local database
    cur.execute(f"SELECT title, first, last, district FROM legislators WHERE id = '{id}'")
    title, first, last, district = cur.fetchone()

    # Selects proper sheet
    if title == "Representative":
        worksheet = rep_sheet
        col_set = rep_cols
    elif title == "Senator":
        worksheet = sen_sheet
        col_set = sen_cols

    cell = worksheet.find(id)
    row = cell.row
    date = time.strftime("%m/%d/%Y").replace("0", "")

    # Update cell of row id with new data IF CHANGED
    updated = False
    if worksheet.cell(row, col_set["voting"]).value != voting:
        worksheet.update_cell(row, col_set["voting"], voting)
        updated = True
    if worksheet.cell(row, col_set["rhetoric"]).value != rhetoric:
        worksheet.update_cell(row, col_set["rhetoric"], rhetoric)
        updated = True
    if worksheet.cell(row, col_set["donation"]).value != donation:
        worksheet.update_cell(row, col_set["donation"], donation)
        updated = True
    if worksheet.cell(row, col_set["updated"]).value != date and updated:
        worksheet.update_cell(row, col_set["updated"], date)


def import_data():
    '''Imports grade data from gspread'''

    Sens = sen_sheet.get_all_records()
    Reps = rep_sheet.get_all_records()

    Sens.extend(Reps)
    Both = Sens
    data = save_grades(format_data(Both))
    return data


def reformat_gspread(reset_key):
    '''Clears the sheet and resets it with information from database with the given assembly number
       Takes a long time because of quota limits by google'''

    # Must give reset_key because it will clear all data
    if reset_key == "danshaircut":
        # Clears sheet
        sen_sheet.clear()
        rep_sheet.clear()

        # Insert new heading
        sen_sheet.insert_row(("id", "Assembly", "title", "first", "last", "District", "Voting", "Rhetoric", "Donation", "last_updated"))
        rep_sheet.insert_row(("id", "Assembly", "title", "first", "last", "District", "Voting", "Rhetoric", "Donation", "last_updated"))

        # Insert Senator data
        cur.execute(f"SELECT id,assembly,title,first,last,district FROM legislators WHERE assembly = {assembly} AND title = 'Senator' ORDER BY last DESC")
        for row in cur.fetchall():
            sen_sheet.insert_row(row, index=2)
            print(row)
            time.sleep(1)

        # Insert Representative data
        cur.execute(f"SELECT id,assembly,title,first,last,district FROM legislators WHERE assembly = {assembly} AND title = 'Representative' ORDER BY last DESC")
        for row in cur.fetchall():
            rep_sheet.insert_row(row, index=2)
            print(row)
            time.sleep(1)


if __name__ == "__main__":
    # get_data()
    # update_data("71reparndt53", "A", "A", "A")
    reformat_gspread("danshaircut")
