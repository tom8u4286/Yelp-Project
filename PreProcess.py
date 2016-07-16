import json
import os

class PreProcess:
    'This program takes menu.json to filter out the reviews of the matched restaurants.'

    def __init__(self):
        self.business_id_list = []

    def get_menu(self):
        """ return menu_json"""
        with open('all_menu.json') as f:
            menu_json = json.load(f)
        return menu_json

    def get_business_id_list(self):
        """ return business_id_list, which is a list of business_id(s) in menu.json """
        menu_json = self.get_menu()
        for dic in menu_json["menu"]:
            self.business_id_list.append(dic["business_id"])

        return self.business_id_list

    def get_review_list(self):
        """ return review_list, which is comprised of every line in all_reviews.json """
        """ update business_id and its review to review_dic """
        with open('all_reviews.json') as f:
            review_json = open('all_reviews.json')

        review_list = []
        for line in review_json:
            string = eval(line.strip()) #type dict
            review_list.append({'business_id': string["business_id"], "review": string["text"], 'stars': string['stars']})
        return review_list

    def create_folder(self):
        """ create directroy if not found """
        directory = os.path.dirname("./reviews/")
        if not os.path.exists(directory):   # if the directory does not exist
            os.makedirs(directory)          # create the directory

    def split_reviews(self):
        """ create a json file and dump the content in the review_dic that match each business_id """

        self.create_folder()
        review_list = self.get_review_list()
        business_id_list = self.get_business_id_list()

        for i in xrange(len(business_id_list)):
            f = open("./reviews/restaurant_%s.json"%(i+1), "w+")

            text_list = []
            for dic in review_list:
                """find a match of business_id: """
                if business_id_list[i] == dic["business_id"]:
                    text_list.append({'review': dic["review"], 'stars': dic['stars'] })
            proper_json = {"business_id":business_id_list[i], "reviews":text_list}

            f.write(json.dumps(proper_json, indent=4))
            f.close()

        return None

if __name__ == '__main__':
    preProcess = PreProcess()
    preProcess.split_reviews()

