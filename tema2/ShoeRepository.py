from Shoe import Shoe
import json


class ShoeRepository:
    def __init__(self):
        self.list_of_shoes = list(json.load(open("database_wannabe.json", "r")))

    def save_state(self):
        json.dump(self.list_of_shoes, open("database_wannabe.json", "w"))

    def get_all_shoes(self):
        return json.dumps(self.list_of_shoes)

    def get_shoe_by_id(self, _id):
        for x in self.list_of_shoes:
            if x['id'] == _id:
                return json.dumps(x)

        return None

    def add_shoe_to_list(self, _shoe):
        self.list_of_shoes.append(_shoe.__dict__)
        self.save_state()
        return json.dumps(_shoe.__dict__)

    def update_shoe_by_id(self, _id, **kwargs):

        for a_shoe in self.list_of_shoes:
            if a_shoe['id'] == _id:
                a_shoe['brand'] = kwargs['brand']
                a_shoe['model'] = kwargs['model']
                a_shoe['size'] = kwargs['size']
                self.save_state()
                return json.dumps(a_shoe)

    def delete_all_shoes(self):
        self.list_of_shoes = list()
        self.save_state()

    def delete_shoe_by_id(self,_id):
        for a_shoe in self.list_of_shoes:
            if a_shoe['id'] == _id:
                self.list_of_shoes.remove(a_shoe)
                self.save_state()
                return True

        return None
