class Car():
    def __init__(self, make, model, year, num_doors=4, owner="Unknown"):
        self.make = make
        self.model = model
        self.year = year
        self.num_doors = num_doors
        self.owner = owner
        self.mileage = 0

    def describe_car(self):
        print(f"{self.year} {self.make} {self.model} | {self.num_doors} doors | "
              f"Owner: {self.owner} | Mileage: {self.mileage} mi")

    def add_mileage(self, miles):
        self.mileage += miles
