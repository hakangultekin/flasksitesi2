from os import link
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from mediaindir import facebookdl, link_kontrol, youtubedl

app = Flask(__name__)
app.secret_key = "hakan"

@app.route("/", methods = ["GET","POST"])
def index():

    if request.method == "POST":
        linkvideo = request.form.get("medialink")
        resultlink = link_kontrol(linkvideo)
        print("*******************resultlink yazdırıldı**********************")
        print(resultlink)
        if resultlink["response"] == "success":
            hakan = dict(resultlink)
            return render_template("download.html", sonucdict = hakan, site = "instagram")
        else:
            flash("Lütfen geçerli bir link giriniz.","danger")
            return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/instagram-downloader", methods = ["GET","POST"])
def instagram():

    if request.method == "POST":
        linkvideo = request.form.get("medialink")
        resultlink = link_kontrol(linkvideo)
        print("*******************resultlink yazdırıldı**********************")
        print(resultlink)
        if resultlink["response"] == "success":
            hakan = dict(resultlink)
            return render_template("download.html", sonucdict = hakan, site = "instagram")
        else:
            flash("Lütfen geçerli bir link giriniz.","danger")
            return render_template("instagram-downloader.html")
    else:
        return render_template("instagram-downloader.html")

@app.route("/youtube-downloader", methods = ["GET","POST"])
def youtubeDownload():

    if request.method == "POST":
        linkvideo = request.form.get("medialink")
        resultlink = youtubedl(linkvideo)
        if resultlink["response"] == "success":
            hakan = dict(resultlink)
            return render_template("download.html", sonucdict = hakan, site = "youtube", originlink = linkvideo, korumali = False)
        elif resultlink["response"] == "korumali":
            hakan = dict(resultlink)
            if linkvideo.find("youtube.com")>-1:
                embedlink = "https://www.youtube.com/" + "embed/" + linkvideo.split("watch?v=")[-1]
            elif linkvideo.find("youtu.be")>-1:
                embedlink = "https://www.youtube.com/" + "embed/" + linkvideo.split("/")[-1]
            else:
                flash("Hatalı veya korumalı bir link girdiniz.","danger")
                return render_template("youtube-downloader.html")
            return render_template("download.html",sonucdict = hakan, site = "youtube", originlink = linkvideo, korumali = True, embedlink = embedlink)
        else:
            flash("Lütfen geçerli bir link giriniz.","danger")
            return render_template("youtube-downloader.html")
    else:
        return render_template("youtube-downloader.html")


@app.route("/facebook-downloader", methods = ["GET","POST"])
def facebookDownload():

    if request.method == "POST":
        linkvideo = request.form.get("medialink")
        resultlink = facebookdl(linkvideo)
        if resultlink["response"] == "success":
            hakan = dict(resultlink)
            return render_template("download.html", sonucdict = hakan, site = "facebook", originlink = linkvideo)
        else:
            flash("Lütfen geçerli bir link giriniz.","danger")
            return render_template("facebook-downloader.html")
    else:
        return render_template("facebook-downloader.html")


@app.route("/yardim", methods = ["GET","POST"])
def yardim():
    if request.method =="GET":
        return render_template("yardim.html")
    else:
        return render_template("yardim.html")



if (__name__) == "__main__":
    app.run(debug=True)