import asyncio
from netschoolapi import NetSchoolAPI
from netschoolapi.data import announcement
from vkbottle.tools.dev_tools.mini_types.bot import message


async def main():

    print('```````````````````````````````````````````')
    print('```````````````````````````````````````````')
    print('```````````````````````````````````````````')


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
    announcements = await ns.announcements()
    print(announcements[0])
    


    # Выходим из сессии
    # Если этого не делать, то при заходе на сайт
    # будет появляться предупреждение о безопасности:
    # "Под вашим логином работает кто-то другой..."
    await ns.logout()



asyncio.run(main())





action = None admin_author_id = None attachments = [MessagesMessageAttachment(audio=None, audio_message=None, call=None, doc=None, gift=None, graffiti=None, group_call_in_progress=None, link=None, market=None, market_market_album=None, photo=PhotosPhoto(access_key='2b72552309a5dc0f1d', album_id=-3, can_comment=None, date=1634391977, has_tags=False, height=None, id=457251027, images=None, lat=None, long=None, owner_id=457641188, photo_256=None, place=None, post_id=None, sizes=[PhotosPhotoSizes(height=75, src=None, type= < PhotosPhotoSizesType.S: 's' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=35x75&quality=96&sign=7855964791c00770e638756feb1e9043&c_uniq_tag=0LfIuFCD3MbUWn_NPyE18trbBqAUWuKFPt6H-WyBfhw&type=album', width=35), PhotosPhotoSizes(height=130, src=None, type= < PhotosPhotoSizesType.M: 'm' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=60x130&quality=96&sign=05c42d267bb0dfecbfb2e9949d9073d9&c_uniq_tag=Ate99x0wo-RaCi_DFzQXAFiuBOnWBSykZIuOUB7lYZ4&type=album', width=60), PhotosPhotoSizes(height=604, src=None, type= < PhotosPhotoSizesType.X: 'x' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=279x604&quality=96&sign=7989a3a3c2ddcda96f01a887e57913da&c_uniq_tag=KXkcB6urLeX2dbTBMdWqw4CAxvDrrujfOYphoyp6DMY&type=album', width=278), PhotosPhotoSizes(height=807, src=None, type= < PhotosPhotoSizesType.Y: 'y' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=372x807&quality=96&sign=91b7089f36f830a05f7f3095f8e30e55&c_uniq_tag=xq6afUdKvmubjyfKQHKMRdmaYH84ovQXWsgi3UtyMXc&type=album', width=372), PhotosPhotoSizes(height=1080, src=None, type= < PhotosPhotoSizesType.Z: 'z' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=498x1080&quality=96&sign=448d8b5efb6c75c7af2d34fa8ea619fa&c_uniq_tag=9rjZEvHuhPKrAszzfwNmOV5bCnyEdjOiMLGBN-S-b6s&type=album', width=498), PhotosPhotoSizes(height=1600, src=None, type= < PhotosPhotoSizesType.W: 'w' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=738x1600&quality=96&sign=85a4ebb7715c653413f3851fafa42477&c_uniq_tag=1v15SeBCZGeht21yR3n5LUUeF9oxBBXV01DL9tFIcp8&type=album', width=738), PhotosPhotoSizes(height=282, src=None, type= < PhotosPhotoSizesType.O: 'o' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=130x282&quality=96&sign=973d2744823f3a84a75736209a76478e&c_uniq_tag=r3hbeo8hIOK6ZXnDC8LKrgeC79DEBXwsGe2MuxT_dXc&type=album', width=130), PhotosPhotoSizes(height=435, src=None, type= < PhotosPhotoSizesType.P: 'p' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=200x434&quality=96&sign=9fddaae1cbee648895798d0e00a57722&c_uniq_tag=uVuDW75cUujTthquVQYqXW4q3hZsLJzVMroPxFJ8ta0&type=album', width=200), PhotosPhotoSizes(height=694, src=None, type= < PhotosPhotoSizesType.Q: 'q' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=320x694&quality=96&sign=cb9659f3dd4a700485b36bdbcd1988e7&c_uniq_tag=j7TmgTO8hfcpBQGvR8A_4bWywuSXQYtQTUiSc9vO3Z0&type=album', width=320), PhotosPhotoSizes(height=900, src=None, type= < PhotosPhotoSizesType.R: 'r' > , url='https://sun9-61.userapi.com/impg/etFyZypwIpkjTyFSpY-NpOxiO_coJeB5lO7szw/rM8f1_Qn2eY.jpg?size=510x900&quality=96&crop=0,0,738,1302&sign=cea83f7c3c6faf7305b031ee9010bb9e&c_uniq_tag=p2Bt4Je2kkQ1KAyUDSVfMboeE2K5p4TghBj1L4MWxOw&type=album', width=510)], text='', user_id=None, width=None), poll=None, sticker=None, story=None, type= < MessagesMessageAttachmentType.PHOTO: 'photo' > , video=None, wall=None, wall_reply=None)] conversation_message_id = 1531 date = 1634392010 deleted = None from_id = 457641188 fwd_messages = [] geo = None id = 1563 important = False is_cropped = None is_hidden = False is_silent = None keyboard = None members_count = None out = <BaseBoolInt.no: 0 > payload = None peer_id = 457641188 pinned_at = None random_id = 0 ref = None ref_source = None reply_message = None text = '' update_time = None was_listened = None group_id = 207442693 client_info = ClientInfoForBots(button_actions=[ < MessagesTemplateActionTypeNames.TEXT: 'text' > , < MessagesTemplateActionTypeNames.VKPAY: 'vkpay' > , < MessagesTemplateActionTypeNames.OPEN_APP: 'open_app' > , < MessagesTemplateActionTypeNames.LOCATION: 'location' > , < MessagesTemplateActionTypeNames.OPEN_LINK: 'open_link' > , < MessagesTemplateActionTypeNames.OPEN_PHOTO: 'open_photo' > , < MessagesTemplateActionTypeNames.CALLBACK: 'callback' > , < MessagesTemplateActionTypeNames.INTENT_SUBSCRIBE: 'intent_subscribe' > , < MessagesTemplateActionTypeNames.INTENT_UNSUBSCRIBE: 'intent_unsubscribe' > ], carousel=True, inline_keyboard=True, keyboard=True, lang_id=0) unprepared_ctx_api = <API token_generator = <<class 'vkbottle.api.token_generator.single.SingleTokenGenerator'>>... > state_peer = None

message.attachments[0].MessagesMessageAttachment.photo.owner_id
