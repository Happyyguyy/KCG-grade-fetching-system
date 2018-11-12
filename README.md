# KCG-grade-fetching-system
System built on python tkinter and sqlite3 to handle kcg grade update requests


__Note:__ doesn't include signin token due to security 

__Also Note:__ heavily considering abandoning the python backend and reconfiguring for a complete cloud based solution (ie. cloud database with google sheets, or a cloud non-sql database by means of google firebase)

### Quick Rundown of modules and methods:
    spreadsheets:
        = on import: connects to sqlite3, validates data on gspread
        - format_data(data)
            - takes imported data and formats it
        - save_grades(data)
            - takes data and inserts it into db.grades
        - update_data(id, voting, rhetoric, donations)
            - takes information and updates it on gspread
        - reformat_gspread(reset_key)
            - takes reset_key as an argument. reset_key == danshaircut
            - clears the gspread workbook and inputs data from current assembly (no grades)
            - NOTE: slow because google api limits 100 calls per 100 seconds

    create_card:
        = on import: connects to sqlite3, sets constants for date
        - download_img(URL=none):
            - takes url and downloads jpg
        - create_card(id, voting, rhetoric, donation):
            - takes arguments and returns a PIL.Image object of report card
            - NOTE: does not save on local machine, only cache
        - save_card(card, directory):
            - takes PIL.Image object and directory string to save image
        - batch_create(destination)
            - takes destination directory as argument and creates report_card for all legislators
            - NOTE: (for now) destination directory MUST exist

    get_legs:
        = on import: connects to sqlite3, parses legislator table on leg.colorado.gov/legislators using bs4
        - printer(func): (depreciated)
            - wrapper function to print self.__doc__ of func
            - for easy terminal printing
            - NOTE: largely unnecessary
        - timer(func): (depreciated):
            - wrapper function to measure time
            - NOTE: largely unnecessary
        - get_leg_headers():
            - gets headers from legislator table
            - returns tuple of headers
        - get_leg_data():
            - scrapes legislator data from table
            - returns list of lists of data
        - zip_dict(key_itr, values_itr):
            - takes headings and data and zips it into a list of dictionaries
            - returns list of dictionaries of legislator data
        - split_name(data):
            - takes data as argument and splits names by first and last and appends it to data
            - returns data
        - get_portrait_link(href):
            - spider to get portrait link from each legislators bio page
            - returns None
        - append_portait_link(data):
            - takes data and for each in data appends link to portrait
            - calls get_portrait_link(href)
            - returns data
        - create_data_file():
            - main process to get data from leg.colorado.gov/legislators and save it locally in db.legislators
            - can be paired with spreadsheets.reformat_gspread() to update gspread

 
