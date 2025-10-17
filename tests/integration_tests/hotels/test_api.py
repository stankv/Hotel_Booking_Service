async def test_get_hotels(ac):  # принимаем асинхронный клиент из conftest.py
    response = await ac.get(  # получаем не отели, а объект response
        "/hotels",
        params={  # params - для передачи именно Query-параметров
            "date_from": "2030-08-01",  # передаем именно как строку
            "date_to": "2030-08-10",
        },
    )
    print(f"{response.json()=}")
    assert response.status_code == 200  # объект response имеет параметр status_code
