from vkbottle_types.objects import PhotosPhoto
import requests


def download_photo_as_bytes(photo: PhotosPhoto):
    return requests.get(photo.sizes[-1].url).content