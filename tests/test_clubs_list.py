import allure
import pytest
import requests
from jsonschema import validate
from config import settings
from schemas.club_list_schema import club_list_response


@allure.suite("API: Книжные клубы")
class TestClubsList:

    @allure.tag("api", "smoke")
    @allure.title("Получение списка клубов по умолчанию")
    def test_get_clubs__default_params__returns_200_and_valid_schema(self):
        """Тест 1: Успешное получение списка клубов и валидация схемы."""

        with allure.step("Отправить GET запрос на /clubs"):
            response = requests.get(
                f"{settings.api_base_url}/clubs",
                timeout=settings.api_timeout
            )

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Валидировать JSON схему ответа"):
            body = response.json()
            validate(body, schema=club_list_response)

        with allure.step("Проверить, что список клубов не пустой"):
            assert body["count"] > 0
            assert len(body["results"]) > 0
            print(f"\n✅ Всего клубов: {body['count']}, на странице: {len(body['results'])}")

    @allure.tag("api", "regression")
    @allure.title("Пагинация: проверка размера страницы (page_size)")
    @pytest.mark.parametrize("page_size", [5, 10, 20])
    def test_get_clubs__with_page_size_param__returns_correct_item_count(self, page_size):
        """Тест 2: Проверка параметра page_size."""

        with allure.step(f"Отправить запрос с page_size={page_size}"):
            params = {"page_size": page_size}
            response = requests.get(
                f"{settings.api_base_url}/clubs",
                params=params,
                timeout=settings.api_timeout
            )

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step(f"Проверить, что количество элементов в 'results' <= {page_size}"):
            body = response.json()
            assert len(body["results"]) <= page_size
            print(f"\n✅ Запрошено: {page_size}, получено: {len(body['results'])}")

    @allure.tag("api", "regression")
    @allure.title("Пагинация: проверка перехода по страницам")
    def test_get_clubs__pagination__returns_different_pages(self):
        """Тест 3: Проверка пагинации - первая и вторая страницы разные."""

        with allure.step("Получить первую страницу"):
            page1 = requests.get(
                f"{settings.api_base_url}/clubs",
                params={"page": 1, "page_size": 5},
                timeout=settings.api_timeout
            ).json()
            id_first_item_page1 = page1["results"][0]["id"]
            assert page1["previous"] is None
            assert page1["next"] is not None

        with allure.step("Получить вторую страницу"):
            page2 = requests.get(
                f"{settings.api_base_url}/clubs",
                params={"page": 2, "page_size": 5},
                timeout=settings.api_timeout
            ).json()
            id_first_item_page2 = page2["results"][0]["id"]
            assert page2["previous"] is not None

        with allure.step("Убедиться, что первая и вторая страницы содержат разные клубы"):
            assert id_first_item_page1 != id_first_item_page2
            print(f"\n✅ Страница 1 первый ID: {id_first_item_page1}")
            print(f"✅ Страница 2 первый ID: {id_first_item_page2}")

    @allure.tag("api", "smoke")
    @allure.title("Поиск клубов по названию книги")
    @pytest.mark.parametrize("search_query", [
        "Сети",  # Клуб ID:1 — реально существует
        "fsdfss",  # Клуб ID:2 — реально существует
        "test"  # Клуб ID:3 — реально существует
    ])
    def test_get_clubs__with_search_param__returns_filtered_results(self, search_query):
        """Тест 4: Проверка поиска клубов по названию книги."""

        with allure.step(f"Отправить запрос с search='{search_query}'"):
            params = {"search": search_query}
            response = requests.get(
                f"{settings.api_base_url}/clubs",
                params=params,
                timeout=settings.api_timeout
            )

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step(f"Проверить, что результаты содержат '{search_query}'"):
            body = response.json()
            results = body["results"]

            assert body["count"] > 0, \
                f"По запросу '{search_query}' ничего не найдено, хотя клуб должен существовать"
            assert len(results) > 0, \
                f"Пустой список результатов по запросу '{search_query}'"

            for club in results:
                assert search_query.lower() in club["bookTitle"].lower(), \
                    f"Клуб '{club['bookTitle']}' не содержит '{search_query}'"
            print(f"\n✅ Найдено клубов: {len(results)} по запросу '{search_query}'")

    @allure.tag("api", "regression")
    @allure.title("Проверка структуры клуба: обязательные поля")
    def test_get_clubs__check_club_structure__has_required_fields(self):
        """Тест 5: Проверка, что каждый клуб имеет все обязательные поля."""

        with allure.step("Получить список клубов"):
            response = requests.get(
                f"{settings.api_base_url}/clubs",
                params={"page_size": 10},
                timeout=settings.api_timeout
            )

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить обязательные поля в каждом клубе"):
            body = response.json()
            required_fields = ["id", "bookTitle", "bookAuthors", "publicationYear", "telegramChatLink", "owner"]

            for idx, club in enumerate(body["results"]):
                for field in required_fields:
                    assert field in club, f"В клубе {idx} (id={club.get('id')}) отсутствует поле '{field}'"
            print(f"\n✅ Проверено {len(body['results'])} клубов, все обязательные поля на месте")