from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR, CHAR, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:root@localhost/simple_address_book")
session = sessionmaker(bind=engine)()

base = declarative_base()

class people_master(base):

    __tablename__ = 'people_master'

    person_id = Column(Integer, primary_key=True)
    person_first_name = Column(VARCHAR(14))
    person_last_name = Column(VARCHAR(16))
    person_DOB = Column(DATE)
    active_phone_number = Column(VARCHAR(22))

    def _init_(self, person_id, person_first_name, person_last_name, person_DOB, active_phone_number):
        self.person_id = person_id
        self.person_first_name = person_first_name
        self.person_last_name = person_last_name
        self.person_DOB = person_DOB
        self.active_phone_number = active_phone_number


class addresses(base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True)
    street_address = Column(VARCHAR(25))
    city = Column(VARCHAR(25))
    state = Column(VARCHAR(25))
    zip_code = Column(CHAR(5))

    def _init_(self, address_id, street_address, city, state, zipcode):
        self.address_id = address_id
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zipcode


class people_address(base):
    __tablename__ = "people_address"

    person_id = Column(Integer, primary_key=True)
    address_id = Column(Integer)
    start_date = Column(DATE)
    end_date = Column(DATE)

    def _init_(self, person_id, address_id, start_date, end_date):
        self.person_id = person_id
        self.address_id = address_id
        self.start_date = start_date
        self.end_date = end_date


if __name__ == '__main__':

    # prints out main menu
    # 1. Search by last name
    # 2. Search by prefix
    # 3. Create new Contact
    # 4. Search by age range
    # 5. Exit
    print(
        "Main menu:\n1- Search by last name\n2- Search by prefix\n3- Create new Contact\n4- Search by age range\n5- Exit\n\tenter command: ",
        end='')
    command = int(input(""))

    while command != 5:
        if command == 1:
            last_name = input("enter last name: ")
            for p, a in session.query(people_master, addresses).filter(people_master.person_id == addresses.address_id).filter(people_master.person_last_name == last_name):
                print("ID: {} | Name: {} {} | Active Address: {} | Active # Number: {} |".format(p.person_id, p.person_first_name, p.person_last_name, a.street_address, p.active_phone_number))
        elif command == 2:
            prefix = input("enter prefix: ")
            for p, a in session.query(people_master, addresses).filter(people_master.person_id == addresses.address_id).filter(people_master.person_first_name.like('{}%'.format(prefix))):
                print("ID: {} | Name: {} {} | DOB: {} | Active # Number: {} | Street Address: {} | City: {} | State: {} | Zipcode: {} |".format(p.person_id,
                                                                                               p.person_first_name,
                                                                                               p.person_last_name,
                                                                                               p.person_DOB,
                                                                                               p.active_phone_number,
                                                                                               a.street_address,
                                                                                               a.city,
                                                                                               a.state,
                                                                                               a.zip_code))


        elif command == 3:
            pID = input("Choose an ID: ")
            fnC = input("First name: ")
            lnC = input("Last Name: ")
            dob = input("Date of Birth (xxxx-yy-zz): ")
            pn = input("Active Phone Number (xxx-xxx-xxxx): ")
            a = input("Street Address: ")
            c = input("City: ")
            s = input("State: ")
            z = input("Zip Code: ")
            new_person = people_master(person_id=pID, person_first_name=fnC, person_last_name=lnC, person_DOB=dob, active_phone_number=pn)
            new_address = addresses(address_id=pID, street_address=a, city=c, state=s, zip_code=z)
            session.add(new_person)
            session.commit()
            session.add(new_address)
            session.commit()
            print("New person added!")
            for p, a in session.query(people_master, addresses).filter(people_master.person_id == addresses.address_id).filter(people_master.person_last_name == lnC):
                print(
                    "ID: {} | Name: {} {} | DOB: {} | Active # Number: {} | Street Address: {} | City: {} | State: {} | Zipcode: {} |".format(
                        p.person_id,
                        p.person_first_name,
                        p.person_last_name,
                        p.person_DOB,
                        p.active_phone_number,
                        a.street_address,
                        a.city,
                        a.state,
                        a.zip_code))
        elif command == 4:
            age1 = input("Select start age range (xxxx-xx-xx): ")
            age2 = input("Select end age range (xxxx-xx-xx: ")
            for p, a in session.query(people_master, addresses).filter(people_master.person_id == addresses.address_id).filter(people_master.person_DOB.between("{}".format(age1), "{}".format(age2))).all():
                print(
                    "ID: {} | Name: {} {} | DOB: {} | Active # Number: {} | Street Address: {} | City: {} | State: {} | Zipcode: {} |".format(
                        p.person_id,
                        p.person_first_name,
                        p.person_last_name,
                        p.person_DOB,
                        p.active_phone_number,
                        a.street_address,
                        a.city,
                        a.state,
                        a.zip_code))

        print(
            "Main menu:\n1- Search by last name\n2- Search by prefix\n3- Create new Contact\n4- Search by age range\n5- Exit\n\tenter command: ",
            end='')
        command = int(input())
