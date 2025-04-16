
import scrapy
from bs4 import BeautifulSoup
from tabulate import tabulate

class LiveScorecardSpider(scrapy.Spider):
    name = "live_scorecard"
    start_urls = [
        "https://www.cricbuzz.com/live-cricket-scorecard/115156/pbks-vs-kkr-31st-match-indian-premier-league-2025"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        innings_sections = soup.find_all("div", class_="cb-col cb-col-100 cb-ltst-wgt-hdr")

        innings_data = []

        i = 0
        while i < len(innings_sections):
            section = innings_sections[i]
            header = section.find("span")
            if header and "Innings" in header.text:
                team_name = header.text.strip().replace(" Innings", "")
                # Extract batting
                batting_rows = section.find_all("div", class_="cb-col cb-col-100 cb-scrd-itms")
                batting_data = []
                for row in batting_rows:
                    cols = row.find_all("div", class_="cb-col")
                    if len(cols) >= 7:
                        name = cols[0].text.strip()
                        dismissal = cols[1].text.strip()
                        r = cols[2].text.strip()
                        b = cols[3].text.strip()
                        _4s = cols[4].text.strip()
                        _6s = cols[5].text.strip()
                        sr = cols[6].text.strip()
                        batting_data.append([name, r, b, _4s, _6s, sr, dismissal])

                # Now go to the next section which is the bowling data
                bowling_data = []
                if i + 1 < len(innings_sections):
                    next_section = innings_sections[i + 1]
                    bowling_rows = next_section.find_all("div", class_="cb-col cb-col-100 cb-scrd-itms")
                    for row in bowling_rows:
                        cols = row.find_all("div", class_="cb-col")
                        if len(cols) >= 8:
                            name = cols[0].text.strip()
                            o = cols[1].text.strip()
                            m = cols[2].text.strip()
                            r = cols[3].text.strip()
                            w = cols[4].text.strip()
                            nb = cols[5].text.strip()
                            wd = cols[6].text.strip()
                            eco = cols[7].text.strip()
                            bowling_data.append([name, o, m, r, w, nb, wd, eco])

                innings_data.append({
                    "team": team_name,
                    "batting": batting_data,
                    "bowling": bowling_data
                })
                i += 2  # Move to next innings pair
            else:
                i += 1

        # Display all innings
        for inning in innings_data:
            print(f"\n🏏 {inning['team']} Batting\n{'=' * 80}")
            print(tabulate(inning['batting'], headers=["Batter", "R", "B", "4s", "6s", "SR", "Dismissal"]))
            print(f"\n🎯 {inning['team']} Bowling\n{'=' * 80}")
            if inning["bowling"]:
                print(tabulate(inning["bowling"], headers=["Bowler", "O", "M", "R", "W", "NB", "WD", "ECO"]))
            else:
                print("No bowling data found.")

