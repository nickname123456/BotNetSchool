from netschoolapi import NetSchoolAPI


async def get_diary(login, password):
    api = NetSchoolAPI(url)
    await api.login(login, password, 'МАОУ "СОШ № 47 г. Челябинска"')
    diary = await api.diary()
    await api.logout()
    return diary
