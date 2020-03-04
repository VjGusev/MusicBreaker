# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
# from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import time
import hashlib
from spleeter_model.inference import Spleeter
from .models import ProcessedSong
import os
import filetype
from get_voice_server.settings import BASE_DIR, MEDIA_ROOT


global_model = None
fs = FileSystemStorage()

def init_model():
    global global_model
    if global_model is None:
        global_model = Spleeter()


def process_file(input_file_url, processed_song_folder_url):
    init_model()
    global_model.predict(input_file_url, processed_song_folder_url)

def get_md5(file):
    hash_md5 = hashlib.md5()
    for chunk in file.chunks(4096):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def is_wav_mp3_file(file):
    buf = filetype.get_bytes(file)
    kind = filetype.guess(buf)
    return (kind is not None) and (kind.extension in ['mp3', 'wav'])

def save_file_in_media(name, file):
    print("Le's try to save in Google Cloud!")
    filename = default_storage.save(name, file)
    file_url = default_storage.url(filename)
    print("File succesfully saved to Google Cloud:", filename, " with url: ", file_url)
    return file_url

def is_good_request(request):
    return request.method == 'POST' and 'song' in request.FILES

def is_used_hash(test_hash_code):
    return ProcessedSong.objects.filter(pk=test_hash_code).exists()

@csrf_exempt
def download(request):
    cur_hash = request.GET["hash"]
    if not is_used_hash(cur_hash):
        return  HttpResponseServerError('<h1>Hash not found!</h1>')
    return HttpResponse(ProcessedSong.objects.get(pk=cur_hash).vocal_url)

@csrf_exempt
def upload(request):
    if not is_good_request(request):
        return HttpResponseServerError('<h1>Incorrect request format</h1>')
    input_song = request.FILES['song']
    if not is_wav_mp3_file(input_song):
        return HttpResponseServerError('<h1>Incorrect file format</h1>')
    md5_of_song = get_md5(input_song)
    if is_used_hash(md5_of_song):
        # song_url =  ProcessedSong.objects.filter(pk=md5_of_song).first().vocal_url
        return HttpResponse(md5_of_song)
    input_song_url = save_file_in_media(f'{md5_of_song}.wav', input_song)
    folder_url = input_song_url[:-4]
    process_file(input_song_url, folder_url)
    processed_vocal_url = f'{folder_url}/vocals.wav'
    processed_accompaniment_url = f'{folder_url}/accompaniment.wav' 
    _ = ProcessedSong.objects.create(hash_code=md5_of_song,
                                     input_url=input_song_url,
                                     vocal_url=processed_vocal_url,
                                     accompaniment_url=processed_accompaniment_url)
    return HttpResponse(md5_of_song)
    