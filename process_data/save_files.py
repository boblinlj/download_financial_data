import os
from datetime import date
from tools import util

def create_staging_file(json, cik):
    file=os.path.join('staging_data',f'{cik}_factor_{date.today()}.txt')
    util.write_text_file(json, file)
    return None

