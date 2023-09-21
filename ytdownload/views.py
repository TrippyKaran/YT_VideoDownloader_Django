from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
import json


@csrf_exempt
def download_audio(request):
  
        try:
            data = json.loads(request.body.decode('utf-8'))
            link = data.get('link')
            youtube_object = YouTube(link)
            audio_stream = youtube_object.streams.filter(only_audio=True).first()
            audio_stream.download()
            return JsonResponse({'message': 'Audio download completed successfully'})
        except Exception as e: 
            return JsonResponse({'error': str(e)})
   
      
@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            link = data.get('link')
            youtube_object = YouTube(link)
            video_stream = youtube_object.streams.get_highest_resolution()
            video_stream.download()
            return JsonResponse({'message': 'Video download completed successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

