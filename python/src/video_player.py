"""A video player class."""
import random

from .video_playlist import Playlist
from .video_library import VideoLibrary


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._video_playing = None
        self._video_paused = False
        self._playlist_collection = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        video_list = self._video_library.get_all_videos()
        video_list_string = []
        for i in video_list:
            video_tags = "["
            for x in range(0, len(i.tags)):
                video_tags = video_tags + i.tags[x]
                if x < len(i.tags) - 1:
                    video_tags += " "
            video_tags = video_tags + "]"
            video_string = " ".join([i.title, '(' + i.video_id + ')', video_tags])
            video_list_string.append(video_string)
        video_list_string.sort()
        print("Here's a list of all available videos:")
        for i in video_list_string:
            print(i)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot play video: Video does not exist")
        elif self._video_playing is None:
            self._video_playing = video
            print("Playing video:", self._video_playing.title)
            self._video_paused = False
        else:
            print("Stopping video:", self._video_playing.title)
            self._video_playing = video
            print("Playing video:", self._video_playing.title)
            self._video_paused = False

    def stop_video(self):
        """Stops the current video."""
        if self._video_playing is None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video:", self._video_playing.title)
            self._video_playing = None

    def play_random_video(self):
        """Plays a random video from the video library."""

        video_list = self._video_library.get_all_videos()
        random_video = random.choice(video_list)

        if self._video_playing is None:
            self._video_playing = random_video
            print("Playing video:", self._video_playing.title)
        else:
            print("Stopping video:", self._video_playing.title)
            self._video_playing = random_video
            print("Playing video:", self._video_playing.title)
        self._video_paused = False

    def pause_video(self):
        """Pauses the current video."""

        if self._video_playing is None:
            print("Cannot pause video: No video is currently playing")
        elif self._video_paused is False:
            self._video_paused = True
            print("Pausing video:", self._video_playing.title)
        elif self._video_paused is True:
            print("Video already paused:", self._video_playing.title)

    def continue_video(self):
        """Resumes playing the current video."""

        if self._video_playing is None:
            print("Cannot continue video: No video is currently playing")
        elif self._video_paused is True:
            self._video_paused = False
            print("Continuing video:", self._video_playing.title)
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self._video_playing is None:
            print("No video is currently playing")
        else:
            video = self._video_library.get_video(self._video_playing.video_id)
            video_tags = "["
            for x in range(0, len(video.tags)):
                video_tags = video_tags + video.tags[x]
                if x < len(video.tags) - 1:
                    video_tags += " "
            video_tags = video_tags + "]"
            if self._video_paused is True:
                print("Currently playing:", video.title, '(' + video.video_id + ')', video_tags, "-", "PAUSED")
            else:
                print("Currently playing:", video.title, '(' + video.video_id + ')', video_tags)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.find_playlist(playlist_name) is not None:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlist_collection.append(Playlist(playlist_name))
            print("Successfully created new playlist:", playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if self._video_library.get_video(video_id) is not None and self.find_playlist(playlist_name) is not None:
            for playlist in self._playlist_collection:
                if playlist.name.lower() == playlist_name.lower():
                    if playlist.contains_video(video_id):
                        print("Cannot add video to", playlist_name + ":", "Video already added")
                    else:
                        playlist.add_video(video_id)
                        print("Added video to", playlist_name + ":", self._video_library.get_video(video_id).title)

        elif self.find_playlist(playlist_name) is None:
            print("Cannot add video to", playlist_name + ":", "Playlist does not exist")

        elif self._video_library.get_video(video_id) is None:
            print("Cannot add video to", playlist_name + ":", "Video does not exist")


    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._playlist_collection) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlist_names = []
            for playlist in self._playlist_collection:
                playlist_names.append(playlist.name)
            playlist_names.sort()
            for playlist_name in playlist_names:
                print(playlist_name)


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.find_playlist(playlist_name) is not None:
            print("Showing playlist:", playlist_name)
            playlist = self.find_playlist(playlist_name)
            if len(playlist.videos) > 0:
                for video_id in playlist.videos:
                    video = self._video_library.get_video(video_id)
                    tag_list = video.tags
                    video_tags = "["
                    for x in range(0, len(tag_list)):
                        video_tags = video_tags + tag_list[x]
                        if x < len(tag_list) - 1:
                            video_tags += " "
                    video_tags = video_tags + "]"
                    print(video.title, '(' + video.video_id + ')', video_tags)
            else:
                print("No videos here yet")
        else:
            print("Cannot show playlist", playlist_name + ':', "Playlist does not exist")

    def find_playlist(self, playlist_name):
        for playlist in self._playlist_collection:
            if playlist.name.lower() == playlist_name.lower():
                return playlist
        return None

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self.find_playlist(playlist_name)
        if playlist is None:
            print("Cannot remove video from", playlist_name + ':', "Playlist does not exist")
        elif playlist.contains_video(video_id):
            playlist.remove_video(video_id)
            print("Removed video from", playlist_name + ':', self._video_library.get_video(video_id).title)
        elif self._video_library.get_video(video_id) is None:
            print("Cannot remove video from", playlist_name + ':', "Video does not exist")
        else:
            print("Cannot remove video from", playlist_name + ':', "Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.find_playlist(playlist_name)
        if playlist is None:
            print("Cannot clear playlist", playlist_name + ':', "Playlist does not exist")
        else:
            playlist.clear_videos()
            print("Successfully removed all videos from", playlist_name)


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.find_playlist(playlist_name)
        if playlist is None:
            print("Cannot delete playlist", playlist_name + ':', "Playlist does not exist")
        else:
            for x in range(0, len(self._playlist_collection)):
                if self._playlist_collection[x] == playlist:
                    self._playlist_collection.pop(x)
                    print("Deleted playlist:", playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
