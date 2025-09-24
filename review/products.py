class ListProduct:
    def __init__(self):
        self.products = []
    def add_product(self, p):
        self.products.append(p)
    def print_products(self):
        for p in self.products:
            print(p)
    def desc_sort_product(self):
        for i in range(0, len(self.products)):
            for j in range(i+1, len(self.products)):
                pi=self.products[i]
                pj=self.products[j]
                if pi.price < pj.price:
                    self.products[j] = pi
                    self.products[i] = pj

    def desc_sort_product2(self):
        products_copy = self.products[:]
        sorted_list = []
        while products_copy: 
            max_item = max(products_copy, key=lambda p: p.price)
            sorted_list.append(max_item)
            products_copy.remove(max_item)
        self.products = sorted_list
