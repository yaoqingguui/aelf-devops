
import datetime
import os

import config


print((datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M"))

dirs = "/opt/swap-oracle-client-1/Logs"

if os.path.exists(dirs):
    print("123")



