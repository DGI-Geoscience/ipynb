import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import numpy as np


def get_data(authtkt, from_time, to_time, file_out):
    urlDR1 = 'http://drillersdashboard.net/reports/DR01/'
    urlDR2 = "http://drillersdashboard.net/reports/DR02/"
    urlS01 = "http://drillersdashboard.net/reports/S01/"
    USERNAME = 'pat'
    PASSWORD = '2RPWmX5U'
    FROM_TIME = from_time
    TO_TIME = to_time
    UNITS = "english"

    cookies = {
        "authtkt": authtkt
    }

    rundata = {
        "time": [],
        "cum_distance": [],
        "delta_distance": [],
        "feed_rate": [],
        "wob": [],
        "rpm": [],
        "pressure": [],
        "flow_rate": [],
        "run_id": []
    }
    session = requests.Session()

    payload_s01 = {
        "from_time": FROM_TIME,
        "to_time": TO_TIME,
        "unit_system": UNITS
    }

    s01_page = session.post(urlS01, auth=(USERNAME, PASSWORD),
                            data=payload_s01,
                            cookies=cookies,
                            allow_redirects=True)
    print(s01_page.content)
    s01_soup = BeautifulSoup(s01_page.content, "lxml")

    job_table = s01_soup.find("div", attrs={"class": "report_body clear"}).find("table")
    for job_row in job_table.find_all("tr"):
        job_col = job_row.find_all("td")
        if len(job_col) == 17:
            num_runs = int(job_col[4].find("a").text)
            if num_runs > 0:
                job_url = job_col[4].find("a").get("href")
                u = urllib.parse.urlparse(job_url)
                q = urllib.parse.parse_qsl(u.query)
                job_id = int(q[2][1])
                drill_id = int(q[4][1])

                payload_dr1 = {
                    "from_time": FROM_TIME,
                    "to_time": TO_TIME,
                    "unit_system": UNITS,
                    "job_id": job_id,
                    "drill_id": drill_id
                }

                page_dr1 = session.post(urlDR1, auth=(USERNAME, PASSWORD),
                                        params=payload_dr1,
                                        cookies=cookies,
                                        allow_redirects=True)

                print(page_dr1.status_code)
                soup_dr1 = BeautifulSoup(page_dr1.content, "lxml")
                table = soup_dr1.find("div", attrs={"class": "report_body"}).find("table")
                previous_distance = 0.0
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) == 9:
                        run_url = cols[1].find("a").get("href")
                        u = urllib.parse.urlparse(run_url)
                        q = urllib.parse.parse_qsl(u.query)
                        run_id = int(q[3][1])
                        run_payload = {
                            "from_time": FROM_TIME,
                            "to_time": TO_TIME,
                            "unit_system": UNITS,
                            "run_id": run_id
                        }
                        run_page = session.post(urlDR2, auth=(USERNAME, PASSWORD),
                                                params=run_payload,
                                                cookies=cookies)
                        num_rows = 0

                        run_soup = BeautifulSoup(run_page.content, "lxml")
                        table = run_soup.find("div", attrs={"class": "report_body"}).find("table")
                        for run_row in table.find_all("tr"):
                            cols = run_row.find_all("td")
                            if len(cols) == 7:
                                try:
                                    t = pd.Timestamp(cols[0].string)
                                    c_dist = np.NaN
                                    delta_dist = np.NaN
                                    feed_rate = np.NaN
                                    wob = np.NaN
                                    rpm = np.NaN
                                    pressure = np.NaN
                                    flow_rate = np.NaN
                                    if t != pd.NaT:
                                        c_dist = float(cols[1].string)
                                        delta_dist = c_dist - previous_distance
                                        previous_distance = c_dist
                                        feed_rate = float(cols[2].string)
                                        wob = float(cols[3].string)
                                        rpm = float(cols[4].string)
                                        pressure = float(cols[5].string)
                                        flow_rate = float(cols[6].string)
                                        num_rows += 1
                                except ValueError:
                                    pass
                                except TypeError:
                                    pass
                                else:
                                    rundata["time"].append(t)
                                    rundata["cum_distance"].append(c_dist)
                                    rundata["delta_distance"].append(delta_dist)
                                    rundata["feed_rate"].append(feed_rate)
                                    rundata["wob"].append(wob)
                                    rundata["rpm"].append(rpm)
                                    rundata["pressure"].append(pressure)
                                    rundata["flow_rate"].append(flow_rate)
                                    rundata["run_id"].append(run_id)

    print("Length of time array: ", len(rundata["time"]))
    print("Length of cum distance:", len(rundata["cum_distance"]))
    print("Length of delta distance: ", len(rundata["delta_distance"]))
    df = pd.DataFrame(data=rundata)
    df.to_csv(file_out)
    return df
