from src.schemas.hotels import HotelAddDTO


async def test_add_hotel(db):
    hotel_data = HotelAddDTO(title="Hotel 5 stars", location="Сочи")  # создаем схему
    await db.hotels.add(hotel_data)
    await db.commit()
