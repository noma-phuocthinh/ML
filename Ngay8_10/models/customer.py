class Customer:
    def __init__(self, ID=None, Name = None, Phone=None, Email=None,Password = None, IsDeleted=None):
        self.ID= ID
        self.Name = Name
        self.Phone = Phone
        self.Email = Email
        self.Password = Password
        self.IsDeleted = IsDeleted

    def __str__(self):
        print("ID:", self.ID)
        print("Name=", self.Name)
        print("Phone=", self.Phone)
        print("Password=", self.Password)
        print("Email=", self.Email)
        print("IsDeleted", self.IsDeleted)