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



# @csrf_exempt
# def download_video(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             link = data.get('link')
#             youtube_object = YouTube(link)
#             video_streams = youtube_object.streams

#             # Filter 1080p progressive streams
#             high_res_progressive_streams = [stream for stream in video_streams if stream.resolution and int(stream.resolution[:-1]) == 1080 and stream.is_progressive]

#             if high_res_progressive_streams:
#                 # Select the first available 1080p progressive stream
#                 video_stream = high_res_progressive_streams[0]
#             else:
#                 # If no 1080p progressive streams are available, choose the highest available progressive stream below 1080p
#                 progressive_streams = [stream for stream in video_streams if stream.is_progressive and stream.resolution]
#                 progressive_streams.sort(key=lambda x: int(x.resolution[:-1]), reverse=True)
#                 video_stream = progressive_streams[0]

#             print(" Available Resolutions:", [stream.resolution for stream in video_streams])
#             print(" Download Resolution:", video_stream.resolution)

#             download_path = "D:\\Downloads"

#             video_stream.download(output_path=download_path)

#             video_url = f"/downloaded-files/{video_stream.title}.mp4"

#             return JsonResponse({'message': 'Video download completed successfully', 'url': video_url, 'video_title': video_stream.title})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            link = data.get('link')
            youtube_object = YouTube(link)
            video_streams = youtube_object.streams

             # Print information about all video streams
            for stream in video_streams:
               print(stream)

            # Sort streams by resolution in descending order
            video_streams = sorted([stream for stream in video_streams if stream.is_progressive], key=lambda x: (int(x.resolution[:-1]), x.resolution), reverse=True)

            if video_streams:
                video_stream = video_streams[0]
            else:
                return JsonResponse({'error': 'No progressive streams available'})

            print(" Available Resolutions:", [stream.resolution for stream in video_streams])
            print(" Download Resolution:", video_stream.resolution)

            download_path = "D:\\Downloads"

            video_stream.download(output_path=download_path)

            video_url = f"/downloaded-files/{video_stream.title}.mp4"

            return JsonResponse({'message': 'Video download completed successfully', 'url': video_url, 'video_title': video_stream.title})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
