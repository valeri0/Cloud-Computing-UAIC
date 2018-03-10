import Utils

class Shoe:
    def __init__(self,_brand,_model,_size):
        self.id = Utils.generate_random_string()
        self.brand = _brand
        self.model = _model
        self.size = _size
