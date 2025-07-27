import json

def check_email_format(email):
    if email is None:
        return None
    
    at_index = email.find("@")
    dot_index = email.rfind(".")

    if at_index == -1:
        raise ValueError("Invalid email: Missing '@' (at) character.")
    if dot_index == -1 or dot_index < at_index:
        raise ValueError("Invalid email: Missing or misplaced '.' (dot) after '@'.")

    return email

def check_valid_phone_number(phone):
    if len(phone) <= 0:
        raise ValueError("Phone number cannot be empyty.")
    if not phone.isdigit():
            raise TypeError("Phone number must be a series of numbers.")
    if len(phone.strip()) != 10: 
        # Phone number length depends on different countries
        raise ValueError("Phone number length must be 10 digits.")
    return phone

def check_valid_contact_id(contact_id):
    if not isinstance(contact_id,int):
        raise TypeError("Contact_Id must be an integer.")
    if contact_id <= 0:
        raise ValueError("Contact_Id must greater than zero.")
    return contact_id

class Contact:
    def __init__(self,name,phone,contact_id,email=None):
        if len(name.strip()) <= 0:
            raise ValueError("Name cannot be empty.")
        
        
        valid_phone_number = check_valid_phone_number(phone)
        valid_contact_id = check_valid_contact_id(contact_id)
        valid_email = check_email_format( email)

        self.name = name
        self.phone = valid_phone_number
        self.contact_id = valid_contact_id
        self.email = valid_email

    def update(self,name=None,phone=None,email=None):
        if name is not None:
            if len(name.strip()) <= 0:
                raise ValueError("Name cannot be empty.")
            self.name = name
        if phone is not None:
            self.phone = check_valid_phone_number(phone)
        if email is not None:
            self.email = check_email_format(email)

    def to_dict(self):
        return {"contact_id":self.contact_id,"name":self.name,"phone":self.phone,"email":self.email}
    
    def __str__(self):
        return f"ID: {self.contact_id} | Name: {self.name} | Phone Number: {self.phone} | Email: {"Not yet provided" if self.email is None else self.email} "
    
class ContactBook:
    def __init__(self, file_name='contacts.json'):
        self.contacts = []
        self.file_name = file_name
        self.next_id = 1
        self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.file_name,'r',encoding='utf-8') as f:
                data_contacts = json.load(f)
        except FileNotFoundError:
           with open(self.file_name,'x') as f:
               json.dump([],f,indent=5,ensure_ascii=False)
               data_contacts = []
        except json.decoder.JSONDecodeError:
            data_contacts = []

        if data_contacts:
            for data in data_contacts:
                contact_loading = Contact(data["name"],data["phone"],data["contact_id"],data["email"])
                self.contacts.append(contact_loading)
                self.next_id += 1

    def save_contacts(self):
        try:
            self.reassign_id()
            data_to_save = [contact.to_dict() for contact in self.contacts]
            with open(self.file_name,'w',encoding='utf-8') as f:
                json.dump(data_to_save,f,indent=5,ensure_ascii=False)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def check_duplicate_phone_number(self,check_phone):
        if check_phone is None:
            return None
        for contact in self.contacts:
            if contact.phone == check_phone:
                raise TypeError(f"Phone number: {check_phone} already exists.")
        return check_phone
    
    def reassign_id(self,):
        if self.contacts:
            current_id = 1
            for contact in self.contacts:
                contact.contact_id = current_id
                current_id += 1 
            
            self.next_id = current_id
        else:
            self.next_id = 1
    
    def add_contact(self,name,phone,email=None):
        try:
            phone = self.check_duplicate_phone_number(phone)
            new_contact = Contact(name,phone,self.next_id,email)
        except (ValueError,TypeError) as e:
            print(e)
        else:
            self.contacts.append(new_contact)
            self.next_id += 1
            print(f"New contact: {name} added successfully.")

    def get_contact_by_id(self,contact_id):
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                return contact
        return None
    
    def get_contact_by_name(self,name):
        found_contacts = []
        for contact in self.contacts:
            if name.strip().lower() == contact.name.lower():
               found_contacts.append(contact)

        return found_contacts if found_contacts else None
    
    def update_contact_by_id(self,contact_id,name=None,phone=None,email=None):
        contact = self.get_contact_by_id(contact_id)
        if contact is None:
            raise ValueError(f"Contact with ID {contact_id} not found.")
        else:
            try:
                phone = self.check_duplicate_phone_number(phone)
                contact.update(name,phone,email)
            except (ValueError,TypeError) as e:
                print(e)
            else:
                info_output = ""
                if name is not None:
                    info_output += "name "
                if phone is not None:
                    info_output += "phone "
                if email is not None:
                    info_output += "email"
                print(f"Contact with ID {contact_id} has updated {info_output}.")
                print(contact)

    def update_contact_by_name(self,name,phone=None,email=None):
        contact = self.get_contact_by_name(name)
        if contact is None:
            raise ValueError(f"Contact with Name {name} not found.")
        else:
            if len(contact) == 1:
                phone = self.check_duplicate_phone_number(phone)
                contact[0].update(phone,email)
                if phone is not None and name is not None:
                    info_output = "phone number and email"
                elif phone is not None:
                    info_output = "phone"
                elif email is not None:
                    info_output = "email"
                else:
                    info_output = "nothing"
                print(f"{contact[0].name} has updated {info_output}.")
                print(contact[0])
            else:
                print("Please check the information again and select by ID")
                print(f"{len(contact)} contacts with the same Name {name}:")
                for duplicate_contact in contact:
                    print(duplicate_contact)

    def delete_contact_by_id(self,contact_id):
        contact = self.get_contact_by_id(contact_id)
        if contact is None:
            raise ValueError(f"Contact with ID {contact_id} not found.")
        else:
            self.contacts.remove(contact)
            self.reassign_id()
            print(f"Contact with ID {contact_id} has been removed.")

    def delete_contact_by_name(self,name):
        contact = self.get_contact_by_name(name)
        if contact is None:
            raise ValueError(f"Contact with Name {name} not found")
        else:
            if len(contact) == 1:
                self.contacts.remove(contact[0])
                self.reassign_id()
                print(f"Contact with Name {contact[0].name} has been removed")
            else:
                print("Please check the information again and select by ID")
                print(f"{len(contact)} contacts with the same Name {name}:")
                for duplicate_contact in contact:
                    print(duplicate_contact)

    def display_contacts(self):
        if len(self.contacts) > 0:
            for contact in self.contacts:
                print(contact)
        else:
            print("Your contact book is empty. Add a few contacts first!")

    def contactss(self,query,is_name=False,is_phone=False):
        if True not in [is_name,is_phone]:
            raise TypeError("Please specify if you are searching by a name, phone number, or email.")
        if is_phone and not query.isdigit():
            raise TypeError("Phone number must be a series of numbers.")
        
        match_query = []


        for contact in self.contacts:
            if (is_name and query in contact.name.lower()) or (is_phone and query in contact.phone):
                match_query.append(contact)
                
        if len(match_query) <= 0:
            if is_name:
                raise ValueError(f"Not found any name match with {query}.")
            elif is_phone:
                raise ValueError(f"Not found any phone number match with {query}.")

        return match_query

def check_action_input(action):
    action_list = ["view","add","search","delete","exit"]
    if not action.isalpha() or action not in action_list:
        raise ValueError("Invalid action. Please choose from (View/Add/Search/Delete/Exit).")
    return action       

def main():
    contactbook = ContactBook()
    while True:
        print("How can I help you with your contact book?")
        daft_action = input("(View/Add/Search/Delete/Exit): ").strip().lower()
        try:
            action = check_action_input(daft_action)
        except ValueError as v:
            print(f"{v}\nPlease try again.")
            continue

        if action == "exit":
            contactbook.save_contacts()
            print("Thanks for using the Contact Book App!")
            break

        if action == "view":
            contactbook.display_contacts()

        elif action == "add":
            while True:
                name = input("Please enter the new contact's name: ").strip()
                if len(name) <= 0:
                    print("The contact's name cannot be empty.")
                    continue
                break

            while True:
                phone_number = input("Please enter the new contact's phone number: ").strip()
                try:
                    valid_phone_number = check_valid_phone_number(phone_number)
                except (ValueError,TypeError) as e:
                    print(f"{e}\nPlease try again.")
                    continue
                break 
            
            while True:
                has_email = input("Do you have the new contact's email? (Y/N): ").strip().lower()
                if len(has_email) <= 0:
                     print("Please answer the question.")
                     continue
                break
            
            if has_email == "y":
                while True:
                    email = input("Please enther the new contact's email: ").strip()
                    try:
                        valid_email = check_email_format(email)
                    except ValueError as v:
                        print(f"{v}\nPlease try again.")
                        continue
                    break

                contactbook.add_contact(name,valid_phone_number,valid_email)
            else:
                contactbook.add_contact(name,valid_phone_number)

        elif action == "search":
            while True:
                search_type = input("Search by name or phone number? (N/P): ").strip().lower()
                if not (search_type == "n" or search_type == "p"):
                    print("Please enter (N/P) to search by name or phone number")
                    continue
                break
            while True:
                query = input("Please enter the information you remember to search for: ").strip().lower()
                if len(query) <= 0:
                    print("The infomation cannot be empty.")
                    continue
                break

            if search_type == "n":
                try:
                    found_contact = contactbook.contactss(query,is_name=True)
                    if len(found_contact) == 1:
                        print(found_contact[0])
                    else:
                        print(f"Had found {len(found_contact)} contacts with query Name {query}")
                        for contact in found_contact:
                            print(contact)
                except (ValueError,TypeError) as e:
                    print(e)
            else:
                try:
                    found_contact = contactbook.contactss(query,is_phone=True)
                    if len(found_contact) == 1:
                        print(found_contact[0])
                    else:
                        print(f"Had found {len(found_contact)} contacts with query Name {query}")
                        for contact in found_contact:
                            print(contact)
                except (ValueError,TypeError) as e:
                    print(e)
        
        elif action == "delete":
            while True:
                delete_type = input("Delete by name or id? (N/I): ").strip().lower()
                if not (delete_type == 'n' or delete_type == 'i'):
                    print("Please enter (N/I) to delete by name or id")
                    continue
                break

            if delete_type == 'n':
                while True:
                    name = input("Please enter a valid contact name: ")
                    if len(name) <= 0:
                        print("The name of the contact cannot be empty.")
                        continue
                    break

                try:
                    contactbook.delete_contact_by_name(name)
                except ValueError as v:
                    print(v)
            else:
                while True:
                    try:
                        contact_id = int(input("Please enter a valid id: "))
                    except ValueError:
                        print("Please try again, id must be an integer.")
                        continue
                    break

                while True:
                    try:
                        valid_contact_id = check_valid_contact_id(contact_id)
                    except (ValueError,TypeError) as e:
                        print(f"{e}\nPlease try again.")
                        continue
                    break

                try:
                    contactbook.delete_contact_by_id(valid_contact_id)
                except ValueError as v:
                    print(v)

main()