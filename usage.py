from Hub import HubLib as Ph

pHub = Ph() # create a new instance of the HubLib class

homepage_videos = pHub.get_homepage() # get the homepage videos

for video in homepage_videos: # for each video in the homepage videos list print the title, link, and thumbnail
    print(video["title"])
    print(video["link"])
    print(video["thumbnail"])
    print("\n")

search_query = "Step Sister" # the search query
page = 1 # the page number to query videos from
search_results = pHub.search(search_query, page) # get the search results

for video in search_results: # for each video in the search results print the title, link, and thumbnail
    print(video["title"])
    print(video["link"])
    print(video["thumbnail"])
    print("\n")

# get the video info of the first video in the search results
video_info = pHub.get_video_info(search_results[0]["link"])
# format the video info for printing
print("Title: {}".format(video_info["title"]))
print("Link: {}".format(video_info["link"]))
print("Thumbnail: {}".format(video_info["thumbnail"]))
print("Favorited: {}".format(video_info["favorited"]))
print("Posted: {}".format(video_info["posted"]))
print("Views: {}".format(video_info["views"]))
print("Description: {}".format(video_info["description"]))
print("\n")
