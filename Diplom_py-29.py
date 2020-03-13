import requests
import json
import time

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
app_id = '171691064'
version = 5.103


class User:
    def __init__(self, vk_id):
        if str(vk_id).isdigit():
            self.vk_id = vk_id
        else:
            params = {
                'user_ids': vk_id,
                'access_token': TOKEN,
                'v': '5.103',
            }
            response = requests.get('https://api.vk.com/method/users.get', params)
            user_profile = response.json()
            self.vk_id = user_profile['response'][0]['id']

    def friends(self):
        params = {
            'user_id': self.vk_id,
            'access_token': TOKEN,
            'v': '5.103',
            'fields': 'domain'
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friends_info = response.json()
        friends_set = set()
        for friend in friends_info['response']['items']:
            friends_set.add(friend['id'])
        return friends_set

    def groups(self):
        params = {
            'user_id': self.vk_id,
            'extended': '1',
            'access_token': TOKEN,
            'v': '5.103',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)
        groups_info = response.json()
        groups_set = set()
        for group in groups_info['response']['items']:
            groups_set.add(group['id'])
        return groups_set


class Group:
    def __init__(self, group_id):
        self.group_id = group_id

    def group_profile(self):
        params = {
            'group_id': self.group_id,
            'access_token': TOKEN,
            'v': '5.103',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        group_info = response.json()
        return group_info


def selection_groups():
    user = User(USER_ID)
    user_friends = user.friends()
    user_groups = user.groups()

    complete_set = set()
    for friend in user_friends:
        try:
            i_user = User(str(friend))
            complete_set = complete_set.union(i_user.groups())
            print('-', end='')
            time.sleep(0.3)
        except KeyError:
            print('-', end='')
            time.sleep(0.3)

        selection_groups = user_groups.difference(complete_set)
    return selection_groups


def write_result(id_group_list, file):
    group_list = []
    for group in id_group_list:
        top_group = Group(str(group))
        group_info = top_group.group_profile()
        iter_dict = dict()

        try:
            for item in group_info['response']:
                iter_dict['name'] = item['name']
                iter_dict['gid'] = item['id']
                iter_dict['members_count'] = item['members_count']
        except KeyError:
            print('-', end='')

        group_list.append(iter_dict)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    USER_ID = input('Введите id или имя пользователя: ')
    write_result(selection_groups(), 'groups.json')