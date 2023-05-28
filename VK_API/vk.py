import vk_api
from prettytable import PrettyTable


def get_user_groups(api_vk, user_id):
    table = PrettyTable()
    table.field_names = ["Name", "ID"]
    groups_list = api_vk.groups.get(user_id=user_id, extended=1)
    groups_count = groups_list['count']

    with open(r"groups_list.txt", "w") as file:
        count_output = f'Groups count: {groups_count}'
        file.write(count_output + '\n\n')
        for group in groups_list['items']:
            output = f"{group['name']} : id={group['id']}"
            table.add_row([group['name'], group['id']])
            file.write(output + '\n')
        print(table)
        print('\n' + count_output)


def main():
    with open('token.txt') as file:
        access_token = file.readline()  # access token
    target_id = int(input('Enter user id: '))

    api_vk = vk_api.VkApi(token=access_token).get_api()
    get_user_groups(api_vk, target_id)


if __name__ == '__main__':
    main()
