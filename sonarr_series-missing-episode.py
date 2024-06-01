#!/usr/bin/python

import json
import requests
import os


class MissingEpisodes:

    sonarr_api_key = os.environ.get("SONARR_KEY")
    sonar_endpoint = "127.0.0.1:8989"
    jackett_api_key = os.environ.get("JACKETT_KEY")
    all_series = None

    def __init__(self):
        pass

    def search_missing(self, show, season):
        print(show["title"] + " - " + str(season["seasonNumber"]))
        print(json.dumps(season, indent=1))
        # curl -k -i --verbose -H "Accept: application/json" -H "Content-Type:application/json" "http://192.168.0.30:9117/api/v2.0/indexers/all/results/torznab?t=tvsearch&q=blacklist&season=6&apikey=qfrjm4sva4iriur4labcjdthcq2x0ge1"

    def find_missing(self):
        series_json_endpoint = (
            "http://"
            + self.sonar_endpoint
            + "/api/series?apikey="
            + self.sonarr_api_key
        )
        result = requests.get(series_json_endpoint)
        # self.all_series = json.loads(result.text)
        print(result.content)

        for show in self.all_series:
            for season in show["seasons"]:
                if season["seasonNumber"] != 0:
                    if season["statistics"]["percentOfEpisodes"] != 100.0:
                        self.search_missing(show, season)


if __name__ == "__main__":
    x = MissingEpisodes()
    x.find_missing()
