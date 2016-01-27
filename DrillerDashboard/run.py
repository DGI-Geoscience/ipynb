import web_scrapper
import pandas as pd

authtkt = '649ea5fc6285fff8c9777ee358c1783556a25382pat!'
FROM_TIME = "2015-10-01 07:00:00"
TO_TIME = "2016-01-12 07:00:00"


df1 = web_scrapper.get_data(authtkt=authtkt, from_time=FROM_TIME, to_time=TO_TIME,
                            file_out="kma-1_drillers_dashboard_data.csv")



