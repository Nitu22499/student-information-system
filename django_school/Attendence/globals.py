from datetime import datetime

# made them global so as to access them in models.py as well as views.py
global date_from
global date_to

date_from = datetime(2019, 1, 1)
date_to = datetime.now()

