import asyncio
from netschoolapi import NetSchoolAPI


async def main():

    # Создаём клиент. Через него мы будем обращаться
    # к АПИ электронного дневника
    ns = NetSchoolAPI('https://sgo.edu-74.ru')

    # Логинимся в "Сетевой город"
    await ns.login(
        'мТаскаеваЕ1Е',    # Логин
        '123456789',       # Пароль
        'МАОУ "СОШ № 47 г. Челябинска"',    # Название школы
    )

    # Печатаем дневник на текущую неделю
    # О полях дневника в "Справочнике"
    diary = await ns.diary()
    print(diary.schedule[0].lessons[0].assignments[1].mark)

    # Выходим из сессии
    # Если этого не делать, то при заходе на сайт
    # будет появляться предупреждение о безопасности:
    # "Под вашим логином работает кто-то другой..."
    await ns.logout()


if __name__ == '__main__':
    asyncio.run(main())
