from review.product import Product

p1 = Product(100, "Thuoc lao",4, 20)
#Xuat ket qua
print(p1)
p2 = Product(200, "Thuoc tri hoi nach", 5, 35)
p1 = p2
print("Thong tin p1",p1)
p1.name = "Thuoc tu trong"
print("Thong tin p2", p2)
