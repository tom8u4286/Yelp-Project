import sys
import copy
import re
import json
import os
import operator
import uuid

class Parse:
    """ Render json files with all the dishes changed into the format of dish_rest & Render rest_list.json """

    def __init__(self):
        self.input_json = sys.argv[1]

    def get_menus(self):
        """ return data["menu"], which is a list containing all the details in every restaurants """
        with open('all_menu.json') as f:
            data = json.load(f)
        return data["menu"]

    def get_restaurant(self):
        """ return a dictionary containing the business_id and the reviews of input_json """
        with open(self.input_json) as f:
            rest_dic = json.load(f)
        return rest_dic

    def get_business_id(self):
        """ return the business_id of the input_json """
        rest_dic = self.get_restaurant()
        business_id = rest_dic["business_id"]
        return business_id

    def get_dishes(self):
        """ return dishes, which is a list of dishes of the matched restaurant """
        """ menus is a list """
        menus = self.get_menus()
        business_id = self.get_business_id()
        for i in xrange(len(menus)):
            if menus[i]["business_id"] == business_id:
                dishes = menus[i]["dishes"]
        #print dishes
        return dishes

    def get_restaurant_name(self):
        """ return the name of the restaurant of the input_json"""
        menus = self.get_menus()
        business_id = self.get_business_id()
        for i in xrange(len(menus)):
            if menus[i]["business_id"] == business_id:
                restaurant_name = menus[i]["restaurant_name"]
        return restaurant_name.lower()

    def get_dishes_regex(self):
        """ dishes_regex is the regular expression for every dish in the dish_list # about to be changed """
        dishes_regex = self.get_dishes()

        for i in xrange(len(dishes_regex)):
            dishes_regex[i] = dishes_regex[i].replace("-","\-").encode('utf-8').lower()
            dishes_regex[i] = re.sub("\&|\.|\(.*\)|[0-9]|([0-9]*-[0-9])+|oz","",dishes_regex[i])

            dishes_regex[i] = dishes_regex[i].split()
            dishes_regex[i][0]= "(" + dishes_regex[i][0] # adding '(' before the first word

            for word in xrange(len(dishes_regex[i])-1):
                dishes_regex[i][word] += "\\s*"

            for word in xrange(len(dishes_regex[i])-2):
                dishes_regex[i][word] += "|"

            dishes_regex[i][len(dishes_regex[i])-2] = dishes_regex[i][len(dishes_regex[i])-2] + ")+"
            dishes_regex[i] = "".join(dishes_regex[i])[:-1]
            dishes_regex[i] += "[a-z]+(s|es|ies)?"

#       print dishes_regex
        return dishes_regex

    def get_dishes_ar(self):
        """ dishes_ar is the dish_list with every dish 'a'ppending 'r'estaurant_name E.g. dish_restaurant """
        restaurant_name = self.get_restaurant_name()
        dishes_ar = self.get_dishes()
        for i in xrange(len(dishes_ar)):
                dishes_ar[i] = dishes_ar[i].lower()
                dishes_ar[i] = "-".join(dishes_ar[i].split(" ")) + "_" + restaurant_name
        #print dishes_ar
        return dishes_ar

    def get_stars(self):
        restaurant_name = self.get_restaurant_name()
        dishes_ar = self.get_dishes()
        for i in xrange(len(dishes_ar)):
                dishes_ar[i] = dishes_ar[i].lower()
                dishes_ar[i] = "-".join(dishes_ar[i].split(" ")) + "_" + restaurant_name
        return stars_string

    def set_marked_dishes(self):
        """ match the dishes in the reviews and mark the dish"""
        dishes = self.get_dishes()
        marked_dishes = []
        for dish in dishes:
            #dish.encode("utf-8").lower()
            marked_dishes.append("<mark>" + dish + "</mark>")
        return marked_dishes

    def parse(self):
        """ match the dishes in the reviews with dishes_regex and replace them with the dishes in dishes_ar  """
        #frontend_review_list = list(self.get_restaurant()["reviews"])
        backend_review_list = list(self.get_restaurant()["reviews"])
        marked_dishes = self.set_marked_dishes()

        dishes_regex = self.get_dishes_regex()
        dishes_ar = self.get_dishes_ar()

        """ tolower before backend parse """
        for i in xrange(len(backend_review_list)):
            #print review
            #frontend_review_list[i]['review']  = frontend_review_list[i].encode("utf-8").lower()
            backend_review_list[i]['review'] = re.sub("(\(|\)|\:|\;|\*|\&|\.|\!|\,|\?|\")", r' \1 ', backend_review_list[i]['review'])
            backend_review_list[i]['review'] = re.sub("\\n", r" ", backend_review_list[i]['review'])
            backend_review_list[i]['review']  = backend_review_list[i]['review'].encode("utf-8").lower()
        #match_count = 0

        """ parse """
        for i in xrange(len(frontend_review_list)):
            for dish in xrange(len(dishes_ar)):
                stars = '*'*backend_review_list[i]['stars']
                #frontend_review_list[i]['review'] = re.sub(dishes_regex[dish], marked_dishes[dish], frontend_review_list[i], flags = re.IGNORECASE)
                backend_review_list[i]['review'] = re.sub(dishes_regex[dish], stars , backend_review_list[i]['reviews'], flags = re.IGNORECASE)
        """ match backend_review_list with dish_ar count the frequnecy of every dish"""
        dish_count_list = []
        matched_count_for_each_review = [0]*len(backend_review_list)
        for dish in dishes_ar:
            matched_reviews = []
            count = 0
            for i in xrange(0,len(backend_review_list)):
                count += str(backend_review_list[i]['review']).count(" "+ dish +" ")
                if dish in backend_review_list[i]['review']:
                    matched_count_for_each_review[i]+=1
            dish_count_list.append(count)
#        print dish_count_list
        avg_diff_dish_count = float(sum(matched_count_for_each_review))/float(len(matched_count_for_each_review))


        """ match every dish in dishes the reviews in frontend_review_list by using every dish in dishes """
        frontend_review_dic_list = []
        for dish in self.get_dishes():
            matched_reviews = []
            for review in frontend_review_list:
                if dish in review:
                    matched_reviews.append(review)
            frontend_review_dic_list.append({"dish_name": dish,"text":matched_reviews})

        return backend_review_list, frontend_review_dic_list,  dish_count_list, avg_diff_dish_count

    def create_dirs(self):
        """ create the directory if not exist"""
        dir1 = os.path.dirname("./backend_reviews/")
        #dir2 = os.path.dirname("./frontend_reviews/")
        #dir3 = os.path.dirname("./restaurant_dic_list/")

        if not os.path.exists(dir1):
            os.makedirs(dir1)
        #if not os.path.exists(dir2):
        #    os.makedirs(dir2)
        #if not os.path.exists(dir3):
        #    os.makedirs(dir3)

    def render(self):
        """ render frontend_review & backend_reviews & restaurant_list """
        backend_review_list, frontend_review_dic_list, dish_count_list, avg_diff_dish_count = self.parse()
        self.create_dirs()
        filename = sys.argv[1][19]
        if sys.argv[1][20] != ".":
            filename = filename + sys.argv[1][20]

        """ 1. render restaurant_*.json in ./frontend_reviews """
        #frontend_json = open("./frontend_reviews/restaurant_%s.json"%(filename), "w+")
        #frontend_json.write(json.dumps(frontend_review_dic_list, indent = 4))
        #frontend_json.close()

        #print sys.argv[1], "'s frontend json is done"

        """ 2. render restaurant_*.json in ./backend_reviews """
        """ tweak backend_reviews"""
        backend_txt = open("./backend_reviews/restaurant_%s.txt"%(filename), "w+")
        for review in backend_review_list:
            backend_txt.write(reviewi['review'] + '\n')
        backend_txt.close()

        print sys.argv[1], "'s backend json is done"

        """ 3. render restaurant_dictionary, which has to be appended in restaurant_dic_list later in the next program """
        #restaurant_json = open("./restaurant_dic_list/restaurant_dic_%s.json"%(filename), "w+")

        #dish_list = []
        #for i in xrange(len(self.get_dishes())):
        #    dish_list.append({"name": self.get_dishes()[i], "vector": NoIndent([0]*200), "name_ar": self.get_dishes_ar()[i].encode("utf-8").lower(), "count": dish_count_list[i], "score":0, "x":0, "y":0})
        #dish_list = sorted(dish_list, key=lambda k: k['count'])
        #dish_list.reverse()
        #restaurant_dic = {"rest_name": self.get_restaurant_name(), "review_count": len(backend_review_list), "dishes_count": len(dish_count_list),"avg_dish_count_in_each_review":avg_diff_dish_count, "dishes": dish_list}
        #restaurant_json.write(json.dumps( restaurant_dic, indent = 4, cls=NoIndentEncoder))
        #restaurant_json.close()

        #print sys.argv[1], "'s restaurant_list json is done"

class NoIndent(object):
    def __init__(self, value):
        self.value = value

class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.iteritems():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result

if  __name__ == '__main__':
    parse = Parse()
    parse.render()

