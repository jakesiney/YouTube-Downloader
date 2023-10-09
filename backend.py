from pytube import YouTube


def get_available_stream_qualities(youtube_url):
    try:
        video = YouTube(youtube_url)
        streams = video.streams.filter(
            file_extension='mp4')  # Consider only mp4 streams
        stream_qualities = [stream.resolution for stream in streams]
        return True, stream_qualities, None
    except Exception as e:
        error_message = f"An error occurred while fetching stream qualities: {e}"
        return False, None, error_message


def download_video(youtube_url, selected_quality):
    try:
        video = YouTube(youtube_url)
        video_stream = video.streams.filter(
            res=selected_quality, progressive=True).first()
        if video_stream:
            video_bytes = video_stream.stream_to_buffer()
            return True, video_bytes, None
        else:
            error_message = f"No stream available for selected quality: {selected_quality}"
            return False, None, error_message
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return False, None, error_message
