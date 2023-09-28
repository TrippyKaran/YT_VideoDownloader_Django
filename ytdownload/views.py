from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
import json
import os


@csrf_exempt
def download_audio(request):
  
        try:
            data = json.loads(request.body.decode('utf-8'))
            link = data.get('link')
            youtube_object = YouTube(link)
            audio_stream = youtube_object.streams.filter(only_audio=True).first()

            download_path = "D:\\Downloads"
            audio_path = os.path.join(download_path, audio_stream.title + '.mp3')

            audio_stream.download(output_path=download_path)

            audio_url = f"/downloaded-files/{audio_stream.title}.mp3"

            return JsonResponse({'message': 'Audio download completed successfully', 'url': audio_url, 'audio_title':audio_stream.title})        
        except Exception as e: 
            return JsonResponse({'error': str(e)})
   
      
@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            link = data.get('link')
            youtube_object = YouTube(link)
            video_streams = youtube_object.streams


            resolutions = list([int(stream.resolution[:-1]) for stream in video_streams if stream.resolution])
            highest_resolution_index = resolutions.index(max(resolutions))
            
            video_stream = youtube_object.streams[highest_resolution_index]


            print(" Available Resolutions:", resolutions)
            print(" Highest Resolutions:", highest_resolution_index)
            print(" Download Resolution:", youtube_object.streams[highest_resolution_index])


            download_path = "D:\\Downloads"

            video_stream.download(output_path=download_path)

            video_url = f"/downloaded-files/{video_stream.title}.mp4"

            return JsonResponse({'message': 'Video download completed successfully', 'url':video_url, 'video_title':video_stream.title})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
