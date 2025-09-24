from review.products import ListProduct
from review.product import Product

lp = ListProduct()
lp.add_product(Product(100, "Product 1", 200,10))
lp.add_product(Product(120, "Product 2", 210,9))
lp.add_product(Product(130, "Product 3", 200,20))
lp.add_product(Product(140, "Product 4", 220,21))
lp.add_product(Product(150, "Product 5", 100,120))
lp.add_product(Product(160, "Product 6", 140,120))

lp.desc_sort_product2()
print("List products sorted by price")
print(lp.print_products())
