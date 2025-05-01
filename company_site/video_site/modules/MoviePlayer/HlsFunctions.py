import os
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from ...models import Movie

# Serve Movie given movie ID
def serve_hls_playlist(request, movie_id):
    try:
        movie = get_object_or_404(Movie, pk=movie_id)
        hls_playlist_path = settings.BASE_DIR / "videos" / movie.movie_file_url

        with open(hls_playlist_path, 'r') as m3u8_file:
            m3u8_content = m3u8_file.read()

        base_url = request.build_absolute_uri('/') 
        serve_hls_segment_url = base_url +"serve_hls_segment/" + str(movie_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)

        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')
    
    except (Movie.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)


# Serve a HLS segement of a movie
def serve_hls_segment(request, movie_id, segment_name):
    try:
        movie = get_object_or_404(Movie, pk=movie_id)
        hls_playlist_path = settings.BASE_DIR / "videos" / movie.movie_file_url

        hls_directory = os.path.dirname(hls_playlist_path)
        segment_path = os.path.join(hls_directory, segment_name)

        # Serve the HLS segment as a binary file response
        return FileResponse(open(segment_path, 'rb'))
    except (Movie.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS segment not found", status=404)