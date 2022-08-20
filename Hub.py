# Made By : Zach with love <3 <3 <3
# Date : 2022-08-19
# Version : 1.0
# Description : This is an API wrapper for PornHub.com that allows you to search for videos and get the info of the video.

from requests import Session
from bs4 import BeautifulSoup

class HubLib: # This is the class that will be used to search for videos and get the info of the video.
    def __init__(self) -> None:
        self.session = Session() # create a session for the requests library
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:58.0) Gecko/20100101 Firefox/58.0", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "Accept-Language": "en-US,en;q=0.5", 
            "Accept-Encoding": "gzip, deflate, br" 
        }) # set the headers for the session
        self.homepage_url = "https://www.pornhub.com/video?page=1" # the homepage url
        pass

    def parse_video_page(self, video_page_url: str) -> dict: # parse the video page for videos
        videos = []
        response = self.session.get(video_page_url) # get the video page
        soup = BeautifulSoup(response.text, "html.parser") # parse the video page for info
        li_elements = soup.find_all("li") # find all li elements

        for li in li_elements:
            title = li.find("span", {"class": "title"})
            if title is not None: # if the title is not None then we have a video
                title_text = title.text.strip()
                link = "https://www.pornhub.com"+li.find("a")["href"]
                if "view_video.php?" in link:
                    video_thumbnail = li.findAll("img")[0].get("data-mediumthumb") # get the video thumbnail
                    if video_thumbnail is not None:
                        json_data = {
                            "title": title_text, # get the title
                            "link": link, # get the video link
                            "thumbnail": video_thumbnail # add the video thumbnail to the json data
                        } # add the video to the list of videos
                        if json_data not in videos:
                            videos.append(json_data) # add the video to the list if it is not already in the list

        return videos # return the list of videos parsed from url

    def get_homepage(self) -> list: # get the homepage and return a list of dictionaries with the results.
        videos = self.parse_video_page(self.homepage_url) 
        return videos # return the list of videos from the homepage
    
    def get_video_info(self, video_url: str) -> dict: # get the info of a video
        response = self.session.get(video_url)
        soup = BeautifulSoup(response.text, "html.parser") # parse the video page for info

        video_info = {} # create a dictionary to store the video info
        
        meta_tags = soup.find_all("meta") # find all meta tags

        for meta in meta_tags: # for each meta tag find the name and content
            if meta.get("property") == "og:title":
                video_info["title"] = meta.get("content")
            if meta.get("property") == "og:description":
                video_info["description"] = meta.get("content")
            if meta.get("property") == "og:image":
                video_info["thumbnail"] = meta.get("content").strip()
            if meta.get("property") == "og:url":
                video_info["link"] = meta.get("content").strip()
        
        # find video info, views, posted date, favorites, likes, dislikes, etc.
        video_info["favorited"] = soup.find("div", {"class": "video-actions-menu"}).find("span", {"class":"favoritesCounter"}).text.strip()
        video_info["posted"] = soup.find("div", {"class": "video-actions-menu"}).find("div", {"class":"videoInfo"}).text
        video_info["views"] = soup.find("div", {"class": "video-actions-menu"}).find("span", {"class":"count"}).text.strip()
        video_info["likes"] = soup.find("div", {"class": "video-actions-menu"}).find("span", {"class":"votesUp"}).get("data-rating").strip()
        video_info["dislikes"] = soup.find("div", {"class": "video-actions-menu"}).find("span", {"class":"votesDown"}).get("data-rating").strip()

        #  video owner info
        video_info["owner"] = soup.find("div", {"class": "userInfo"}).find("a",{"class":"bolded"}).text.strip()
        video_info["owner_link"] = "https://www.pornhub.com"+soup.find("div", {"class": "userInfo"}).find("a",{"class":"bolded"})["href"]
        video_info["owner_thumbnail"] = soup.find("div", {"class": "userAvatar"}).find("img", {"class":"lazy"}).get("data-src").strip()
        return video_info # return the video info dictionary for the video with the given url

    # Search for videos on PornHub.com and return a list of dictionaries with the results.
    def search(self, search_term: str, page:str = 1) -> list: # page is optional and defaults to 1 if not specified
        search_term = search_term.replace(" ", "+")
        search_url = "https://www.pornhub.com/video/search?search={}&page={}".format(search_term, page) 
        videos = self.parse_video_page(search_url) # parse the search page for videos
        return videos # return the list of videos
