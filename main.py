import json
import os
import vk_api
import requests
from auth_data import token



def get_wall_posts(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token}&v=5.81"
    req = requests.get(url)
    src = req.json()

    # проверяем существует ли директория с именем группы
    if os.path.exists(f"{group_name}"):
        print(f"Директория с именем {group_name} уже существует!")
    else:
        os.mkdir(group_name)

    # сохраняем данные в json файл, чтобы видеть структуру
    with open(f"{group_name}/{group_name}_wall.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # собираем ID новых постов в список
    fresh_posts_id = []
    posts = src["response"]["items"]

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    """Проверка, если файла не существует, значит это первый
    парсинг группы(отправляем все новые посты). Иначе начинаем
    проверку и отправляем только новые посты."""
    if not os.path.exists(f"{group_name}/exist_posts_{group_name}.txt"):
        print("Файла с ID постов не существует, создаём файл!")

        with open(f"{group_name}/exist_posts_{group_name}.txt", "w") as file:
            for item in fresh_posts_id:
                file.write(str(item) + "\n")

        # извлекаем данные из постов
        for post in posts:

            post_id = post["id"]
            print(f"Отправляем пост с ID {post_id}")

            try:
                if "attachments" in post:
                    post = post["attachments"]

                    # забираем фото
                    if post[0]["type"] == "photo":

                        photo_quality = [
                            "photo_2560",
                            "photo_1280",
                            "photo_807",
                            "photo_604",
                            "photo_130",
                            "photo_75"
                        ]

                        if len(post) == 1:

                            for pq in photo_quality:
                                if pq in post[0]["photo"]:
                                    post_photo = post[0]["photo"][pq]
                                    print(f"Фото с расширением {pq}")
                                    print(post_photo)
                                    break
                        else:
                            for post_item_photo in post:
                                if post_item_photo["type"] == "photo":
                                    for pq in photo_quality:
                                        if pq in post_item_photo["photo"]:
                                            post_photo = post_item_photo["photo"][pq]
                                            print(f"Фото с расширением {pq}")
                                            print(post_photo)
                                            break
                                else:
                                    print("Линк или аудио пост")
                                    break

            except Exception:
                print(f"Что-то пошло не так с постом ID {post_id}!")

    else:
        print("Файл с ID постов найден, начинаем выборку свежих постов!")


def get_vk_status_and_save_to_json(group_name):
    # Получаем информацию о пользователе
    url = f"https://api.vk.com/method/users.get?user_ids={group_name}&fields=status&access_token={token}&v=5.81"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        print(f"Ошибка при получении статуса: {data['error']['error_msg']}")
        return None

    # Извлекаем статус
    status = data.get("response", [{}])[0].get("status")

    # Записываем статус в JSON файл
    with open(f"{group_name}/{group_name}_status.json", 'w', encoding='utf-8') as json_file:
        json.dump({"user_id": group_name, "status": status}, json_file, ensure_ascii=False, indent=4)

    print(f"Статус пользователя {group_name} записан в файл .")



def get_user_id(screen_name):
    url = f"https://api.vk.com/method/users.get?user_ids={screen_name}&access_token={token}&v=5.131"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        print(f"Ошибка при получении user_id: {data['error']['error_msg']}")
        return None

    return data['response'][0]['id']


def get_vk_friends_and_groups(user_id_or_name, group_name):
    # Проверяем, является ли это именем пользователя или ID
    if not user_id_or_name.isdigit():
        user_id = get_user_id(user_id_or_name)
        if user_id is None:
            return
    else:
        user_id = int(user_id_or_name)

    # Получаем список друзей
    friends_url = f"https://api.vk.com/method/friends.get?user_id={user_id}&fields=nickname,city,education&access_token={token}&v=5.131"
    friends_response = requests.get(friends_url)
    friends_data = friends_response.json()

    print("Друзья:", friends_data)  # Отладочная информация

    if 'error' in friends_data:
        print(f"Ошибка при получении друзей: {friends_data['error']['error_msg']}")
        return

    # Получаем список сообществ
    groups_url = f"https://api.vk.com/method/groups.get?user_id={user_id}&fields=name&access_token={token}&v=5.131"
    groups_response = requests.get(groups_url)
    groups_data = groups_response.json()



    print("Группы:", groups_data)  # Отладочная информация

    if 'error' in groups_data:
        print(f"Ошибка при получении групп: {groups_data['error']['error_msg']}")
        return

    # Сохраняем данные в JSON файл
    data = {
        "friends": friends_data.get("response", {}).get("items", []),
        "groups": groups_data.get("response", {}).get("items", [])
    }

    with open(f"{group_name}/{group_name}_friendsgroups.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Друзья и сообщества пользователя {user_id} сохранены в файл")


def get_user_info(user_id, group_name):
    # Авторизация в ВКонтакте
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    try:
        # Получение информации о пользователе
        user_info = vk.users.get(user_ids=user_id, fields='relation, education, city')[0]

        # Извлечение необходимых данных
        family_status = user_info.get('relation', None)
        education = user_info.get('education', {}).get('university_name', None)
        city = user_info.get('city', {}).get('title', None)

        # Создание словаря с данными
        data = {
            'user_id': user_id,
            'family_status': family_status,
            'education': education,
            'city': city
        }

        # Сохранение данных в JSON файл
        with open(f"{group_name}/{group_name}_love_education_city.json", 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Данные пользователя {user_id} успешно сохранены в {user_id}_info.json")

    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    group_name = input("Введите ID: ")
    get_wall_posts(group_name)
    get_vk_status_and_save_to_json(group_name)
    get_vk_friends_and_groups(group_name, group_name)
    get_user_info(group_name, group_name)


if __name__ == '__main__':
    main()
