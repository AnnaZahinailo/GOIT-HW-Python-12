import re
from pathlib import Path

from classes import AddressBook, Record, Name, Phone, Birthday

users = AddressBook()

def input_error(func):
    def inner(*args):
        try: 
            return func(*args)
        except KeyError:
            return f"Enter user name."
        except ValueError:
            return "Give me name and phone or birthday corretly please."
        except IndexError:
            return "Give me name and phone or birthday corretly please."
        except TypeError:
            return "Give me name and phone or birthday corretly please."
        except FileNotFoundError:
            return "File not found."
    return inner


def cmd_hello_func(*_): 
    return "How can I help you?"


@input_error
def cmd_add_phone_func(name, *phones):
    if name and not re.match(r"^\w+$", name):
        raise ValueError
    if name in users and not phones:
            return f"The name {name} is already registred in the Address Book."
    user = Record(Name(name))
    if name in users:
        user.phone_list = users[name][0]
        if user.birthday:
            user.birthday.value = users[name][1]
    else:
        user.phone_list = []
    new_phones_list = []
    p = ""
    rp = ""
    if phones:
        for phone in phones:      
            if phone in user.phone_list and len(phones) == 1:
                return f"The phone number {phone} is already registred in the Address Book."    
            elif phone in user.phone_list and len(phones) > 1:
                rp += f"\nThe phone number {phone} is already registred in the Address Book." 
            else:
                user.add_phone(Phone(phone))
                new_phones_list.append(phone)
    users.add_record(user)
    p = ", ".join(new_phones_list)
    return f"{name} {p} has been added to the Address Book.{rp}"


@input_error
def cmd_change_phone_func(name, phone, new_phone):
    if name and not re.match(r"^\w+$", name):
        raise ValueError
    if new_phone and not re.match(r"^\+[\d]{12}$", phone):
        raise ValueError
    if name not in users:
        return f"User {name} is not in the Address Book."
    else:
        user = Record(Name(name))
        user.phone_list = users[name][0]
        if name in users and new_phone in user.phone_list:
            return f"The phone number {phone} is already registred in the Address Book."    
        if phone not in user.phone_list:
            return(f"The phone number {phone} is not in the list")   
        user.change_phone(Phone(phone), Phone(new_phone)) 
        return f"The phone number {phone} for {name} has been changed for {new_phone}."


@input_error
def cmd_delete_phone_func(name, phone):
    if name and not re.match(r"^\w+$", name):
        raise ValueError
    if phone and not re.match(r"^\+[\d]{12}$", phone):
        raise ValueError
    if not name in users:
        return f"No user {name} in the Address Book."
    user = Record(Name(name))
    user.phone_list = users[name][0]
    if phone not in user.phone_list:
        return f"The phone number {phone} is not in the Address Book."
    if phone not in user.phone_list:
        return(f"The phone number {phone} is not in the list")
    user.delete_phone(Phone(phone))
    return f"The phone number {phone} for {name} has been deleted."


@input_error
def cmd_phone_func(*args):
    name = args[0]
    if name and not re.match(r"^\w+$", name):
        raise ValueError
    if not name in users:
        return f"No user {name} in the Address Book."
    phone_list = users[name][0]    
    if phone_list == []:
        return f"No phones for {name} in the Address Book."
    else:
        return f"{name}: " + ", ".join(phone_list)


@input_error
def cmd_show_all_func(num=None): 
    all = ""
    l = len(users)
    n = int(num) if num else l
    if l == 0:
        return "No items in the Address Book"
    else:
        page = users.iterator(n)
        for page_dict in page:
            for name, data in page_dict.items():
                phones = data[0]
                bd = data[1]       
                bd_info = f" Birthday: {bd} " if bd else ""
                all += name + ": " + ", ".join(phones) + bd_info + "\n"
            all += "\n"
    return all + "All contacts are displayed"


@input_error
def cmd_add_birthday_func(name, birthday):
    if name and not re.match(r"^\w+$", name):
        raise ValueError
    user = Record(Name(name))
    if name in users and not birthday:
            return f"The name {name} is already registred in the Address Book."
    if name in users:
        user.phone_list = users[name][0]
        user.birthday = users[name][1]
    else:
        user.phone_list = []
    user.add_birthday(Birthday(birthday))
    users.add_record(user)
    return f"{name} {birthday} has been added to the Address Book."


@input_error
def cmd_birthday_func(*args):
    name = args[0]
    if name and not re.match(r"^\w+$", name):
        raise ValueError
    if not name in users:
        return f"No user {name} in the Address Book."
    birthday = users[name][1]
    if not birthday:
        return f"No birthday for {name} in the Address Book."
    else:
        return f"{name}: {birthday}"


@input_error
def cmd_days_to_birthday_func(name):
    if name and not re.match(r"^\w+$", name):
        raise ValueError
    if not name in users:
        return f"No user {name} in the Address Book."
    birthday = users[name][1]
    if not birthday:
        return f"No birthday for {name} in the Address Book."
    else:
        user = Record(Name(name))
        days = str(user.days_to_birthday(birthday))
        return f"{days} days to {name}'s Birthday."


@input_error
def cmd_open_func(file_name=None):
    if file_name and not re.match(r"^\w+(.bin)?$", file_name):
        raise ValueError
    file_name = file_name if file_name else "addressbook.bin"
    if not file_name.endswith(".bin"):
        file_name += ".bin"
    p = Path(file_name)
    if not p.is_file():
        return f"File '{file_name}' not found."
    users.upload_dict(file_name)
    return f"Address Book has been opened from '{file_name}'."


@input_error
def cmd_save_func(file_name=None):
    if file_name and not re.match(r"^\w+(.bin)?$", file_name):
        raise ValueError
    file_name = file_name if file_name else "addressbook.bin"
    if not file_name.endswith(".bin"):
        file_name += ".bin"
    users.save_dict(file_name)
    return f"Address Book has been saved to '{file_name}'."


@input_error
def cmd_find_func(sample, case_mode=None):
    sample = str(sample)
    if sample and not re.match(r"^(\+\d*)|\w+$", sample):
        raise ValueError
    found_dict = users.find_txt(sample, case_mode)
    if len(found_dict) == 0:
        return f"No result for '{sample}'."
    found = f"Contacts containing in name or phone '{sample}':\n"
    for name, data in found_dict.items():
        phones = data[0]
        bd = data[1]       
        bd_info = f" Birthday: {bd} " if bd else ""
        found += name + ": " + ", ".join(phones) + bd_info + "\n"
    return found

def help_info(): 
     return """You can manage your Address Book with the commands:
           hello
           open ['File'][.bin] (default: addressbook.bin)
           save ['File'][.bin] (default: addressbook.bin)
           find 'sample' ['s'] (s: case-sensitive, default: case-insensitive)
           add phone 'Name' ['+380000000000'] ['+380000000001'] ...
           change phone 'Name' '+380000000000' '+380000000001'
           delete phone 'Name' '+380000000000'
           phone 'Name'
           add birthday 'Name' ['dd.mm.yyyy']
           birthday 'Name'
           days to birthday 'Name'
           show all ['N'] (N=number of contacts per page, default=All)
           good bye
           close
           exit"""


def cmd_exit_func(*_):
     return "Good bye!\n"


COMMANDS = {
    'hello': cmd_hello_func,
    'open': cmd_open_func,
    'save': cmd_save_func,
    'find': cmd_find_func,
    'add phone': cmd_add_phone_func,
    'change phone': cmd_change_phone_func,
    'delete phone': cmd_delete_phone_func,
    'phone': cmd_phone_func,
    'add birthday': cmd_add_birthday_func,
    'birthday': cmd_birthday_func,
    'days to birthday': cmd_days_to_birthday_func,
    'show all': cmd_show_all_func,
    'good bye': cmd_exit_func,
    'close': cmd_exit_func,
    'exit': cmd_exit_func,
}


def cmd_parser(command_line: str):          
    for cmd in COMMANDS:
        command_line = command_line.strip()
        space_case = ' ' if cmd in ('add phone', 'change phone', 'delete phone', 'phone', 'add birthday', 'birthday', 'find') or cmd == 'open' and command_line.endswith('open\n') or cmd == 'save' and command_line.endswith('save\n') else '' #to avoid an incorrect commandline that didn't interrupt the program in received version
        if command_line.lower().startswith(cmd + space_case):
            command_line = command_line.replace(command_line[0:len(cmd)], cmd)   #command shoudl be case-insensitive
            return COMMANDS[cmd], command_line.replace(cmd, '').strip().split()
    return None, []


def main():
    command_line = ""
    print("\nHello!")
    print(help_info())

    while True:
        command_line = input("\nEnter command: ")
        command, data = cmd_parser(command_line)

        if not command:
            print("No command. Try again!")
        else:
            print(command(*data))

            if command == cmd_exit_func:
                break


if __name__ == "__main__":
    main()