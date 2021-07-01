"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name):
        self._name = playlist_name
        self._videos = []

    def add_video(self, video_id):
        self._videos.append(video_id)

    def contains_video(self, video_id):
        for video in self._videos:
            if video == video_id:
                return True
        return False

    def remove_video(self, video_id):
        for i in range(0, len(self._videos)):
            if self._videos[i] == video_id:
                self._videos.pop(i)
                return True
        return False

    def clear_videos(self):
        self._videos = []

    @property
    def name(self) -> str:
        """Returns the name of the playlist."""
        return self._name

    @property
    def videos(self) -> list:
        """Returns the title of a video."""
        return self._videos



