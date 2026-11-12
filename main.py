import requests

# Константы
USERNAME = "CREATOR4k"
# Необязательно: GitHub Token (classic) с правом read:user.
# Оставьте пустой строкой "", чтобы запустить без токена (лимит 60 запросов/час).
TOKEN = ""

API_URL = "https://api.github.com"
WEB_URL = "https://github.com"


def get_github_users(endpoint):
    """Получает ВСЕ страницы списка пользователей (followers/following) из GitHub API.
    Возвращает множество логинов или None при ошибке."""
    url = f"{API_URL}/users/{USERNAME}/{endpoint}"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    logins = set()
    page = 1

    while True:
        params = {"per_page": 100, "page": page}  # по умолчанию API отдаёт только 30
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети при запросе к {endpoint}: {e}")
            return None

        if response.status_code != 200:
            print(f"Ошибка при запросе к {endpoint}: {response.status_code}")
            try:
                print(response.json().get("message", ""))
            except Exception:
                pass
            return None

        data = response.json()
        if not data:  # пустая страница — данные закончились
            break

        logins.update(user["login"] for user in data)
        if len(data) < 100:  # последняя страница
            break
        page += 1

    return logins


def main():
    print(f"Получение данных для аккаунта {USERNAME}...\n")

    followers = get_github_users("followers")
    following = get_github_users("following")

    if followers is None or following is None:
        print("Не удалось получить данные. Проверьте подключение, имя пользователя и токен.")
        return

    # Логика сравнения множеств
    mutual = followers & following             # Взаимные подписки
    not_following_back = following - followers  # Вы подписаны, а они на вас нет
    fans = followers - following                # Они на вас подписаны, а вы на них нет

    # Вывод результатов
    print("📊 Статистика профиля:")
    print(f"Подписчиков (Followers): {len(followers)}")
    print(f"Подписок (Following): {len(following)}")
    print(f"Взаимных друзей: {len(mutual)}\n")

    print(f"❌ Вы подписаны, но они НЕ подписаны взаимно ({len(not_following_back)}):")
    if not_following_back:
        for user in sorted(not_following_back, key=str.lower):
            print(f"  - {WEB_URL}/{user}")
    else:
        print("  Таких пользователей нет.")

    print(f"\n⭐ Они подписаны на вас, но вы НЕ подписаны взаимно ({len(fans)}):")
    if fans:
        for user in sorted(fans, key=str.lower):
            print(f"  - {WEB_URL}/{user}")
    else:
        print("  Таких пользователей нет.")


if __name__ == "__main__":
    main()