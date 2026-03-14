class Person():
    def __init__(self, name, age, place_of_birth):
        self.name = name
        self.age = age
        self.place_of_birth = place_of_birth

    def introduce_yourself(self):
        print(f"Hello, my name is {self.name}. I am {self.age} years old and I was born in {self.place_of_birth}.")

    def age_person(self):
        self.age += 1


class Student(Person):
    def __init__(self, name, age, place_of_birth, school, graduation_year, gpa):
        super().__init__(name, age, place_of_birth)
        self.school = school
        self.graduation_year = graduation_year
        self.gpa = gpa

    def student_info(self):
        print(f"{self.name} attends {self.school}, graduating in {self.graduation_year} with a GPA of {self.gpa:.1f}.")
