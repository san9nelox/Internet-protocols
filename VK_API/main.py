import requests
from prettytable import PrettyTable

with open('token.txt') as file:
    TOKEN = file.readline()


def get_gifts(user_id):
    gifts_req = requests.get("https://api.vk.com/method/gifts.get?",
                               params={
                                   'access_token': TOKEN,
                                   'user_id': user_id,
                                   'v': 5.131
                               }).json()['response']

    print_table(gifts_req)


def print_table(req_info):
    table = PrettyTable()
    table.field_names = ["Link", "Message"]
    for item in req_info["items"]:
        gift = item['gift']
        table.add_row([gift['thumb_256'], item['message']])
    print(table)


def main():
    user_id = input("Enter user id: ")
    get_gifts(user_id)


if __name__ == '__main__':
    main()
