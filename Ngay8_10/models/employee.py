class Employee:
    def __init__(self, ID=None,EmployeeCode= None, Name = None, Phone=None, Email=None, IsDeleted=None):
        self.ID= ID
        self.EmployeeCode = EmployeeCode
        self.Name = Name
        self.Phone = Phone
        self.Email = Email
        self.IsDeleted = IsDeleted

    def __str__(self):
        print("ID:", self.ID)
        print("Name=", self.Name)
        print("Phone=", self.Phone)
        print("Email=", self.Email)