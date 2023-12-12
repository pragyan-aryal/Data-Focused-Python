import time
from DrissionPage import ChromiumPage
from bs4 import BeautifulSoup
import pandas as pd


def fetch_description(codes, sample="All"):
    job_url = "https://www.indeed.com/viewjob?jk={}&from=vjs&viewtype=embedded"

    page = ChromiumPage()

    print('\n')

    for code in codes:
        records = pd.read_csv('Final_Data/' + sample + "/" + code + ".tsv", sep="\t")

        jobKeys = [records.loc[i, "Key"] for i in range(len(records))]

        descriptions = []

        for key in jobKeys:
            l_ = (
                    "Currently Fetched "
                    + "{:3.2f}".format((len(descriptions) / len(jobKeys)) * 100)
                    + "% job description"
            )
            l_ = (
                    l_
                    + ". Remaining "
                    + str(len(jobKeys) - len(descriptions)).ljust(4)
                    + " jobs"
            )
            l_ = l_ + ". Completed " + str(len(descriptions)).ljust(4) + " jobs."

            print(l_)

            try:
                page.get(job_url.format(key))
                page.wait.load_complete()

                err = False
                while not err:
                    try:
                        page.wait.ele_display("#jobDescriptionText", timeout=20)
                        err = True
                    except Exception:
                        time.sleep(10)

                time.sleep(0.2)

                soup = BeautifulSoup(page.html, "lxml")

                try:
                    d = soup.find("div", {"id": "jobDescriptionText"})
                    g = d.extract()
                    f = [h.text.replace("\n", "") for h in g if h.text != "\n"]

                    a = "".join(f)
                except Exception:
                    a = "NA"

                try:
                    benef = soup.find("div", {"id": "benefits"})
                    lis = benef.find_all("li")
                    benefits = [ben.text for ben in lis]
                except Exception:
                    benefits = []

                descriptions.append({"key": key, "desc": a, "benefits": benefits})

                time.sleep(0.5)
            except Exception:
                pass

        with open('Final_Data/' + sample + '/'+ code + "_desc.tsv", "a", encoding="utf-8") as outfile:
            for i in descriptions:
                outfile.write(
                    i["key"] + "\t" + i["desc"] + "\t" + str(i["benefits"]) + "\n"
                )
        outfile.close()

    page.quit()
