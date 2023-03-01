import json


from googleapiclient.discovery import build
my_api_key = "[Your Google Search Api key]"
my_cse_id = "[Your Custom Search Engine Project Key]"


class ParsingException(Exception):
    pass


class GoogleNoResultException(Exception):
    pass


class GoogleSearchClient:
    def __init__(self, api_key=my_api_key, cse_id=my_cse_id, log_path="./"):
        self.service = build("customsearch", "v1", developerKey=api_key)
        self.cse_id = cse_id
        self.log_path = log_path

    def search_count(self, search_term, **kwargs):

        res = self.service.cse().list(q=search_term, cx=self.cse_id, **kwargs).execute()
        if res:
            try:
                count = int(res["searchInformation"]['totalResults'])
            except Exception:
                with open(f"{self.log_path}{search_term}_problematic_response.json", "w") as f:
                    json.dump(res, f)
                raise ParsingException(f"Error in parsing number of pages google response for search term {search_term} "
                                       f"result saved in {self.log_path}{search_term}_problematic_response.json")

            return count
        else:
            raise GoogleNoResultException(f"No result found for the given search_term: {search_term}")
