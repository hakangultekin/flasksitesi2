import requests
import json
from pytube import YouTube
import urllib.parse

from requests.api import post

def link_kontrol(link):
    url = link

    mediaInfo = dict()
    if url.find("nstagram") == -1:
        print("hata 0")
        mediaInfo["response"] = "failed"
        return mediaInfo

    try:
        if link[-1] == "/":
            shortcode = link.split("/")
            shortcode = shortcode[-2]
        elif link[-1] != "/":
            shortcode= link + "/"
            shortcode = shortcode.split("/")
            if shortcode[-2].find("?") > -1:
                shortcode = shortcode[-3]
            else:
                shortcode = shortcode[-2]

        head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
        # req_link = f"https://www.instagram.com/data/query/?query_hash=a9441f24ac73000fa17fe6e6da11d59d&variables=%7B%22shortcode%22%3A%22{shortcode}%22%7D"
        req_link = f"https://www.instagram.com/p/{shortcode}/?__a=1"
        print(req_link)
        r = requests.get(req_link, headers = head)
        print(r.content)
        json_data = json.loads(r.content)
    except:
        print("hata 1")
        mediaInfo["response"] = "failed"
        return mediaInfo

    mediaType = json_data["graphql"]["shortcode_media"]["__typename"]

    if mediaType =="GraphVideo":
        mediaUrl = json_data["graphql"]["shortcode_media"]["video_url"]
        uzanti = json_data["graphql"]["shortcode_media"]["shortcode"]
        user_id = json_data["graphql"]["shortcode_media"]["owner"]["id"]
        ppurl = json_data["graphql"]["shortcode_media"]["owner"]["profile_pic_url"]
        username = json_data["graphql"]["shortcode_media"]["owner"]["username"]
        mediacount = json_data["graphql"]["shortcode_media"]["owner"]["edge_owner_to_timeline_media"]["count"]
        followercount = json_data["graphql"]["shortcode_media"]["owner"]["edge_followed_by"]["count"]
        fullname = json_data["graphql"]["shortcode_media"]["owner"]["full_name"]
        poster = json_data["graphql"]["shortcode_media"]["thumbnail_src"]

        if int(followercount) >= 1000000:
            followercount = f"{round(followercount/1000000)}M"
        elif int(followercount) >= 100000 & int(followercount) <= 999999:
            followercount = f"{round(followercount/1000,1)}K"
        elif int(followercount) >= 10000 & int(followercount) <= 100000:
            followercount = f"{round(followercount/1000,1)}K"

        mediaInfo["username"] = username
        mediaInfo["fullname"] = fullname
        mediaInfo["mediaUrl"] = mediaUrl
        mediaInfo["mediaDL"] = f"{mediaUrl}&dl=1"
        mediaInfo["ppurl"] = ppurl
        mediaInfo["mediacount"] = mediacount
        mediaInfo["followercount"] = followercount
        mediaInfo["uzanti"] = uzanti
        mediaInfo["type"] = mediaType
        mediaInfo["poster"] = poster
        mediaInfo["response"] = "success"
        return mediaInfo

    elif mediaType =="GraphImage":
        mediaUrl = json_data["graphql"]["shortcode_media"]["display_resources"][-1]["src"]
        uzanti = json_data["graphql"]["shortcode_media"]["shortcode"]
        user_id = json_data["graphql"]["shortcode_media"]["owner"]["id"]
        ppurl = json_data["graphql"]["shortcode_media"]["owner"]["profile_pic_url"]
        username = json_data["graphql"]["shortcode_media"]["owner"]["username"]
        mediacount = json_data["graphql"]["shortcode_media"]["owner"]["edge_owner_to_timeline_media"]["count"]
        followercount = json_data["graphql"]["shortcode_media"]["owner"]["edge_followed_by"]["count"]
        mediaType = json_data["graphql"]["shortcode_media"]["__typename"]
        fullname = json_data["graphql"]["shortcode_media"]["owner"]["full_name"]

        if int(followercount) >= 1000000:
            followercount = f"{round(followercount/1000000)}M"
        elif int(followercount) >= 100000 & int(followercount) <= 999999:
            followercount = f"{round(followercount/1000,1)}K"
        elif int(followercount) >= 10000 & int(followercount) <= 100000:
            followercount = f"{round(followercount/1000,1)}K"

        mediaInfo["username"] = username
        mediaInfo["fullname"] = fullname
        mediaInfo["mediaUrl"] = mediaUrl
        mediaInfo["mediaDL"] = f"{mediaUrl}&dl=1"
        mediaInfo["ppurl"] = ppurl
        mediaInfo["mediacount"] = mediacount
        mediaInfo["followercount"] = followercount
        mediaInfo["uzanti"] = uzanti
        mediaInfo["type"] = mediaType
        mediaInfo["response"] = "success"
        print(mediaInfo)
        return mediaInfo

    elif mediaType=="GraphSidecar":
        uzanti = json_data["graphql"]["shortcode_media"]["shortcode"]
        user_id = json_data["graphql"]["shortcode_media"]["owner"]["id"]
        ppurl = json_data["graphql"]["shortcode_media"]["owner"]["profile_pic_url"]
        username = json_data["graphql"]["shortcode_media"]["owner"]["username"]
        mediacount = json_data["graphql"]["shortcode_media"]["owner"]["edge_owner_to_timeline_media"]["count"]
        followercount = json_data["graphql"]["shortcode_media"]["owner"]["edge_followed_by"]["count"]
        mediaType = json_data["graphql"]["shortcode_media"]["__typename"]
        fullname = json_data["graphql"]["shortcode_media"]["owner"]["full_name"]

        base_links = json_data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
        photo_links = []
        for i in base_links:
            photo_links.append(i["node"]["display_resources"][-1]["src"])

        if int(followercount) >= 1000000:
            followercount = f"{round(followercount/1000000)}M"
        elif int(followercount) >= 100000 & int(followercount) <= 999999:
            followercount = f"{round(followercount/1000,1)}K"
        elif int(followercount) >= 10000 & int(followercount) <= 100000:
            followercount = f"{round(followercount/1000,1)}K"

        mediaInfo["username"] = username
        mediaInfo["fullname"] = fullname
        mediaInfo["mediaUrl"] = photo_links
        mediaInfo["ppurl"] = ppurl
        mediaInfo["mediacount"] = mediacount
        mediaInfo["followercount"] = followercount
        mediaInfo["uzanti"] = uzanti
        mediaInfo["type"] = mediaType
        mediaInfo["response"] = "success"
        print(mediaInfo)
        return mediaInfo

    else:
        mediaInfo["response"] = "failed"
        print("hata 2")
        return mediaInfo


def youtubedl(link):
    mediadata = dict()

    arama_kelimeleri = ["watch?v=","youtu.be/","youtube.com/watch?v="]
    validLink = False
    for i in arama_kelimeleri:
        if link.find(i) > -1:
            validLink = True

    if validLink == False:
        mediadata["response"] = "failed"
        return mediadata
    else:
        if link.find("youtube.com/watch?v=") > -1:
            link2 = link.split("=")
            if len(link2[-1]) != 11:
                validLink = False
        if link.find("youtu.be/") > -1:
            link2 = link.split("/")
            if len(link2[-1]) != 11:
                validLink = False

        if validLink == True:
            try:
                ytLink = YouTube(link)
                mediadata["videoAdi"] = ytLink.title
                encoded_title = urllib.parse.quote(ytLink.title)
                mediadata["author"] = ytLink.author
                mediadata["description"] = ytLink.description
                mediadata["thumbnail"] = ytLink.thumbnail_url
                mediadata["lenght"] = ytLink.length
                mediadata["publish_date"] = ytLink.publish_date
                hdvid = ytLink.streams.get_by_itag(22)
                mediadata["720_dl_url"] = hdvid.url
                mediadata["720_dl_coded_url"] = hdvid.url + "&title=" + encoded_title
                sdvid = ytLink.streams.get_by_itag(18)
                mediadata["360_dl_url"] = sdvid.url
                mediadata["360_dl_coded_url"] = sdvid.url + "&title=" + encoded_title
                mp3= ytLink.streams.get_by_itag(251)
                mediadata["mp3_dl_url"] = mp3.url
                mediadata["mp3_dl_coded_url"] = mp3.url + "&title=" + encoded_title
                mediadata["response"] = "success"
                return mediadata
            except:
                ytLink = YouTube(link)
                mediadata["videoAdi"] = ytLink.title
                encoded_title = urllib.parse.quote(ytLink.title)
                mediadata["author"] = ytLink.author
                mediadata["description"] = ytLink.description
                mediadata["thumbnail"] = ytLink.thumbnail_url
                mediadata["lenght"] = ytLink.length
                mediadata["publish_date"] = ytLink.publish_date
                sdvid = ytLink.streams.get_by_itag(18)
                mediadata["360_dl_url"] = sdvid.url
                mediadata["360_dl_coded_url"] = sdvid.url + "&title=" + encoded_title
                mp3= ytLink.streams.get_by_itag(140)
                mediadata["mp3_dl_url"] = mp3.url
                mediadata["mp3_dl_coded_url"] = mp3.url + "&title=" + encoded_title
                mediadata["response"] = "korumali"
                return mediadata
        else:
            mediadata["response"] = "failed"
            return mediadata


def facebookdl(link):
    mediadata = dict()
    if link.find("facebook.com/") > -1:
        if link.find("/videos/") > -1 or link.find("/watch/") > -1:
            mediadata["response"] = "success"
            return mediadata
    elif link.find("fb.watch/") > -1:
        mediadata["response"] = "success"
        return mediadata
    else:
        mediadata["response"] = "failed"
        return mediadata

print(link_kontrol("https://www.instagram.com/p/CRjuQKBn82a/"))
