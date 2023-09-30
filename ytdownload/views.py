from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube
import json
import os
from moviepy.editor import *


@csrf_exempt
def download_audio(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        link = data.get("link")
        youtube_object = YouTube(link)
        audio_stream = youtube_object.streams.filter(only_audio=True).first()

        download_path = "D:\\Downloads"
        audio_path = os.path.join(download_path, audio_stream.title + ".mp3")

        audio_stream.download(output_path=download_path)

        audio_url = f"/downloaded-files/{audio_stream.title}.mp3"

        return JsonResponse(
            {
                "message": "Audio download completed successfully",
                "url": audio_url,
                "audio_title": audio_stream.title,
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)})


@csrf_exempt
def download_video(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print("Link Mil Gya")
            link = data.get("link")

            print("Function call krr rha hu")
            result = download_video_file(link, "HD")
            print("download ho gya")

            print("Final Video Url : ", result.get("video_url"))

            # Prepare the video file response
            video_path = result.get("video_url")
            video_file = open(video_path, "rb")
            response = FileResponse(video_file, content_type="video/mp4")
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{result.get("video_title")}.mp4"'

            return response

        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid request method"})


def download_video_file(link, res_level):
    yt = YouTube(link)
    result = {}

    print("All Streams : ")
    for stream in yt.streams:
        print(stream)

    if res_level == "4K":
        dynamic_streams = ["2160p"]
        print("4K")
    elif res_level == "FHD":
        dynamic_streams = ["1080p"]
        print("FHD")
    elif res_level == "HD":
        dynamic_streams = ["720p"]
        print("HD")
    elif res_level == "SD":
        dynamic_streams = ["480p"]
        print("SD")

    # Get the current user's username
    current_user = os.getlogin()

    # Construct download paths using the username
    download_path_c = f"C:\\Users\\{current_user}\\Downloads"
    download_path_desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    if os.path.exists(download_path_c):
        download_path = download_path_c
    else:
        download_path = download_path_desktop

    for ds in dynamic_streams:
        print("Selected Stream : ", ds)
        try:
            if res_level == "4K" or res_level == "FHD":
                if res_level == "4K":
                    video_stream = yt.streams.filter(
                        res=ds, file_extension="webm", progressive=False
                    ).first()

                else:
                    video_stream = yt.streams.filter(
                        res=ds, file_extension="mp4", progressive=False
                    ).first()

                    audio_stream = yt.streams.filter(
                        only_audio=True, file_extension="webm"
                    ).first()

                if video_stream and audio_stream:
                    video_filename = clean_filename(yt.title) + "_video.mp4"
                    audio_filename = clean_filename(yt.title) + "_audio.webm"

                    # Download video and audio streams with dynamic filenames
                    video_stream.download(filename=video_filename)
                    audio_stream.download(filename=audio_filename)

                    audio_path = os.path.join("", audio_filename)
                    video_path = os.path.join("", video_filename)

                    # Create instances of VideoFileClip and AudioFileClip
                    video_clip = VideoFileClip(video_path)
                    audio_clip = AudioFileClip(audio_path)

                    video_clip_with_audio = video_clip.set_audio(audio_clip)

                    # Output filename for merged video
                    merged_filename = os.path.join(
                        "", clean_filename(yt.title) + "_merged.mp4"
                    )

                    # Write the merged video file
                    video_clip_with_audio.write_videofile(merged_filename)

                    # Delete temporary video and audio files
                    os.remove(audio_path)
                    os.remove(video_path)

                    result["video_url"] = merged_filename
                    result["video_title"] = yt.title

                    print(f"Successfully merged streams for {ds} from {link}")
                    break

            else:
                print("720p")
                video_stream = yt.streams.filter(
                    res="720p", file_extension="mp4", progressive=True
                ).first()

                video_filename = clean_filename(yt.title) + "_video.mp4"
                video_stream.download(filename=video_filename)

                result["video_url"] = video_filename
                result["video_title"] = yt.title

        except Exception as e:
            print(f"Error while merging streams: {str(e)}")
            continue
    return result


def clean_filename(name):
    # Clean and limit the filename as needed
    forbidden_chars = "\"*\\/'.|?:<>"
    filename = (
        ("".join([x if x not in forbidden_chars else "#" for x in name]))
        .replace("  ", " ")
        .strip()
    )
    if len(filename) >= 176:
        filename = filename[:170] + "..."
    return filename
