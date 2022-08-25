import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram import enums

import os
import shutil
import threading
import pickle
import time

from buttons import *
import aifunctions
import helperfunctions


# env
bot_token = os.environ.get("TOKEN", "5582672566:AAFTEgKiLQOHtEwqNdtb1gYwBDXRbZkPUa8") 
api_hash = os.environ.get("HASH", "3eba5d471162181b8a3f7f5c0a23c307") 
api_id = os.environ.get("ID", "4682685")


# bot
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)
os.system("chmod 777 c41lab.py negfix8 tgsconverter")


# main function to follow
def follow(message,inputt,new,oldmessage):
    output = helperfunctions.updtname(inputt,new)

    if output.upper().endswith(VIDAUD) and inputt.upper().endswith(VIDAUD):

        print("It is VID/AUD option")

        file,msg = down(message)
        srclink = helperfunctions.videoinfo(file)
        cmd = helperfunctions.ffmpegcommand(file,output,new)

        if msg != None:
            app.edit_message_text(message.chat.id, msg.id, '__Converting__')

        os.system(cmd)
        os.remove(file)
        conlink = helperfunctions.videoinfo(output)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            caption=f'**Source File** : __{srclink}__\n\n**Converted File** : __{conlink}__'
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            up(message,output,msg,capt=caption)
        else:
            app.send_message(message.chat.id,"**Error while Conversion**", reply_to_message_id=message.id)
            
        os.remove(output)

    elif output.upper().endswith(IMG) and inputt.upper().endswith(IMG):

        print("It is IMG option")
        file = app.download_media(message)
        srclink = helperfunctions.imageinfo(file)
        cmd = helperfunctions.magickcommand(file,output,new)
        os.system(cmd)
        conlink = helperfunctions.imageinfo(output)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, caption=f'**Source File** : __{srclink}\n\n**Converted File** : __{conlink}__', reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"**Error while Conversion**", reply_to_message_id=message.id)
            
        os.remove(output)

        if new == "ocr":
            cmd = helperfunctions.tesrctcommand(file,message.id)
            os.system(cmd)
            with open(f"{message.id}.txt","r") as ocr:
                text = ocr.read()
            os.remove(f"{message.id}.txt")
            app.send_message(message.chat.id, text, reply_to_message_id=message.id)
            
        if new == "ico":
            slist = ["256", "128", "96", "64", "48", "32", "16"]
            for ele in slist:
                toutput = helperfunctions.updtname(inputt,f"{ele}.png")
                os.remove(toutput)
        
        os.remove(file)

    elif output.upper().endswith(IMG) and inputt.upper().endswith("TGS"):

        if new == "webp" or new == "gif" or new == "png":

            print("It is Animated Sticker option")
            file = app.download_media(message)
            srclink = helperfunctions.imageinfo(file)        
            os.system(f'./tgsconverter "{file}" "{new}"')
            output = helperfunctions.updtname(file,new)
            conlink = helperfunctions.imageinfo(output)

            if os.path.exists(output) and os.path.getsize(output) > 0:
                app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
                app.send_document(message.chat.id,document=output, force_document=True, caption=f'**Source File** : __{srclink}\n\n**Converted File** : __{conlink}__', reply_to_message_id=message.id)
            else:
                app.send_message(message.chat.id,"**Error while Conversion**", reply_to_message_id=message.id)

            os.remove(file)
            os.remove(output)
            
        else:
            app.send_message(message.chat.id,"Only Availble Conversions for Animated Stickers are GIF, PNG and WEBP", reply_to_message_id=message.id)

    elif output.upper().endswith(EB) and inputt.upper().endswith(EB):

        print("It is Ebook option")
        file = app.download_media(message)
        cmd = helperfunctions.calibrecommand(file,output)
        os.system(cmd)
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id, document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"**Error while Conversion**", reply_to_message_id=message.id)
            
        os.remove(output)

    elif (output.upper().endswith(LBW) and inputt.upper().endswith(LBW)) or (output.upper().endswith(LBI) and inputt.upper().endswith(LBI)) or (output.upper().endswith(LBC) and inputt.upper().endswith(LBC)):
        
        print("It is LibreOffice option")
        file = app.download_media(message)
        cmd = helperfunctions.libreofficecommand(file,new)
        os.system(cmd)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"Error while conversion", reply_to_message_id=message.id)
            if msg != None:
                app.delete_messages(message.chat.id,message_ids=[msg.id])
            
        os.remove(file)
        os.remove(output)

    elif output.upper().endswith(FF) and inputt.upper().endswith(FF):
        
        print("It is FontForge option")
        file = app.download_media(message)
        cmd = helperfunctions.fontforgecommand(file,output,message)
        os.system(cmd)
        os.remove(f"{message.id}-convert.pe")
        os.remove(file)

        if os.path.exists(output) and os.path.getsize(output) > 0:
            app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
            app.send_document(message.chat.id,document=output, force_document=True, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id,"**Error while Conversion**", reply_to_message_id=message.id)
            
        os.remove(output)
    else:
        app.send_message(message.chat.id,"Send me valid Extension", reply_to_message_id=message.id)

    # deleting message    
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id+1])


# negative to positive
def negetivetopostive(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    print("using c41lab")
    os.system(f'./c41lab.py "{file}" "{output}"')
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **c41lab**", reply_to_message_id=message.id)
    os.remove(output)
    
    print("using simple tool")
    aifunctions.positiver(file,output)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **simple tool**", reply_to_message_id=message.id)
    os.remove(output)
    
    print("using negfix8")
    os.system(f'./negfix8 "{file}" "{output}"')
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **negfix8**", reply_to_message_id=message.id)
    os.remove(output)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# color image
def colorizeimage(message,oldmessage):
    file = app.download_media(message)
    output = file.split("/")[-1]

    aifunctions.deoldify(file,output)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **Deoldify**", reply_to_message_id=message.id)
    os.remove(output)

    aifunctions.colorize_image(output,file)
    app.send_document(message.chat.id,document=output, force_document=True,caption="used tool -> **simple tool**", reply_to_message_id=message.id)
    os.remove(output)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# dalle
def genrateimages(message,prompt):
    
    # requsting
    # mdhash = aifunctions.mindalle(prompt,AutoCall=False) # min dalle
    # ldhash = aifunctions.latdif(prompt,AutoCall=False) # latent 
    filelist = aifunctions.dallemini(prompt) # dalle mini
    # latfile = aifunctions.latentdiff(prompt) # latent direct
    # imagelist = aifunctions.latdifstatus(ldhash,prompt) # latent get
    # mdfile = aifunctions.mindallestatus(mdhash,prompt) # min dalle get

    # dalle mini
    app.send_message(message.chat.id,"**DALLE MINI**", reply_to_message_id=message.id)
    for ele in filelist:
        app.send_document(message.chat.id,document=ele,force_document=True)
        os.remove(ele)
    os.rmdir(prompt)

    # latent diffusion
    # app.send_message(message.chat.id,f"__LATENT DIFFUSION :__ **{prompt}**", reply_to_message_id=message.id)
    # app.send_document(message.chat.id,document=latfile,force_document=True)
    # os.remove(latfile)
    # for ele in imagelist:
        # app.send_document(message.chat.id,document=ele,force_document=True)
        # os.remove(ele)
        
    # min dalle
    # app.send_message(message.chat.id,f"__MIN-DALLE :__ **{prompt}**", reply_to_message_id=message.id)
    # app.send_document(message.chat.id,document=mdfile,force_document=True)
    # os.remove(mdfile)

    # delete msg
    app.delete_messages(message.chat.id,message_ids=[message.id+1])


# cog video
def genratevideos(message,prompt):

    hash, queuepos = aifunctions.cogvideo(prompt,AutoCall=False)
    msg = app.send_message(message.chat.id,f"Prompt received and Request is sent. Expected waiting time is {(queuepos+1)*3} mins", reply_to_message_id=message.id)

    file = aifunctions.cogvideostatus(hash,prompt)
    app.send_video(message.chat.id, video=file, reply_to_message_id=message.id) #,caption=f"COGVIDEO : {prompt}")
    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[msg.id])


# delete msg
def dltmsg(message,sec=15):
    time.sleep(sec)
    app.delete_messages(message.chat.id,message_ids=[message.id,message.id-1])


# read file
def readf(message,oldmessage,allowrename=False):
    file = app.download_media(message)
    
    try:
        with open(file,"r") as rf:
            txt = rf.read()
        n = 4096
        split = [txt[i:i+n] for i in range(0, len(txt), n)]
        for ele in split:
            app.send_message(message.chat.id, ele, reply_to_message_id=message.id)   
    except:
        if allowrename:
            with open(f'{message.from_user.id}.json', 'wb') as handle:
                pickle.dump(message, handle)
            app.send_message(message.chat.id, "Error in Reading File\nUse **/rename new-filename** to Rename", reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id, "Error in Reading File", reply_to_message_id=message.id)

    os.remove(file)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])


# send video
def sendvideo(message,oldmessage):
    file, msg = down(message)
    up(message, file, msg, video=True)

    app.delete_messages(message.chat.id, message_ids=[oldmessage.id])
    os.remove(file)


# send document
def senddoc(message,oldmessage):
    file = app.download_media(message)
    app.send_document(message.chat.id, document=file, force_document=True, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id, message_ids=[oldmessage.id])
    os.remove(file)


# send photo
def sendphoto(message,oldmessage):
    file = app.download_media(message)
    app.send_photo(message.chat.id, photo=file, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)


# extract file
def extract(message,oldm):
    file = app.download_media(message)
    cmd,foldername,infofile = helperfunctions.zipcommand(file,message)
    os.system(cmd)
    os.remove(file)

    with open(infofile, 'r') as f:
        lines = f.read()
    last = lines.split("Everything is Ok\n\n")[-1]
    app.send_message(message.chat.id, f'__{last}__', reply_to_message_id=message.id)

    if os.path.exists(foldername):
        dir_list = helperfunctions.absoluteFilePaths(foldername)
        for ele in dir_list:
            if os.path.getsize(ele) > 0:
                app.send_document(message.chat.id, document=ele, force_document=True, reply_to_message_id=message.id)
                os.remove(ele)
        shutil.rmtree(foldername)
    else:
        app.send_message(message.chat.id, "**Unable to Extract**", reply_to_message_id=message.id)
    
    app.delete_messages(message.chat.id, message_ids=[oldm.id])


# make file
def makefile(message,oldmessage):
    text = message.text.split("\n")
    firstline = text[0]
    text.remove(text[0])
    
    message.text = ""
    for ele in text: 
        message.text = message.text + f"{ele}\n"
    
    with open(firstline,"w") as file:
        file.write(message.text)
    try:
        app.send_document(message.chat.id, document=firstline, reply_to_message_id=message.id)
    except:
        app.send_message(message.chat.id, "Makefile takes first line of your Text as Filename and File content will start from Second line", reply_to_message_id=message.id)

    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(firstline)      	    


# transcript speech to text
def transcript(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
    output = helperfunctions.updtname(inputt,"wav")
    temp = helperfunctions.updtname(inputt,"txt")

    if file.endswith("wav"):
        aifunctions.splitfn(file,message,temp)
    else:
        cmd = helperfunctions.ffmpegcommand(file,output,"wav")
        os.system(cmd)
        aifunctions.splitfn(output,message,temp)
        os.remove(output)
        
    app.send_document(message.chat.id, document=temp, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(file)
    os.remove(temp)
    

# text to speech 
def speak(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
    output = helperfunctions.updtname(inputt,"mp3")
   
    aifunctions.texttospeech(file,output)
    os.remove(file)

    app.send_document(message.chat.id, document=output, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(output)


# upscaling
def increaseres(message,oldmessage):
    file = app.download_media(message)
    inputt = file.split("/")[-1]
   
    aifunctions.upscale(file,inputt)
    os.remove(file)

    app.send_document(message.chat.id, document=inputt, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldmessage.id])
    os.remove(inputt)


# renaming
def rname(message,newname,oldm):
    app.delete_messages(message.chat.id,message_ids=[message.id+1])
    file = app.download_media(message)
    os.rename(file,newname)
    app.send_document(message.chat.id, document=newname, reply_to_message_id=message.id)
    app.delete_messages(message.chat.id,message_ids=[oldm.id])
    os.remove(newname)


# download with progress
def down(message):

    try:
        size = int(message.document.file_size)
    except:
        try:
            size = int(message.video.file_size)
        except:
            size = 1

    if size > 25000000:
        msg = app.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
        dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',msg),daemon=True)
        dosta.start()
    else:
        msg = None

    file = app.download_media(message,progress=dprogress, progress_args=[message])
    os.remove(f'{message.id}downstatus.txt')
    return file,msg


# uploading with progress
def up(message,file,msg,video=False,capt=None):

    if msg != None:
        app.edit_message_text(message.chat.id, msg.id, '__Uploading__')

    if os.path.getsize(file) > 25000000:
        upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',msg),daemon=True)
        upsta.start()

    if capt == None:
        if not video:
            app.send_document(message.chat.id, document=file, force_document=True ,reply_to_message_id=message.id, progress=uprogress, progress_args=[message])    
        else:
            app.send_video(message.chat.id, video=file ,reply_to_message_id=message.id, progress=uprogress, progress_args=[message])    
    else:
        if not video:
            app.send_document(message.chat.id, document=file, caption=capt, force_document=True ,reply_to_message_id=message.id, progress=uprogress, progress_args=[message])    
        else:
            app.send_video(message.chat.id, video=file, caption=capt, reply_to_message_id=message.id, progress=uprogress, progress_args=[message]) 


    os.remove(f'{message.id}upstatus.txt')

    if msg != None:
        app.delete_messages(message.chat.id,message_ids=[msg.id])


# up progress
def uprogress(current, total, message):
    with open(f'{message.id}upstatus.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# down progress
def dprogress(current, total, message):
    with open(f'{message.id}downstatus.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# upload status
def upstatus(statusfile,message):

    while True:
        if os.path.exists(statusfile):
            break
        
    time.sleep(5)
    while os.path.exists(statusfile):

        with open(statusfile,"r") as upread:
            txt = upread.read()

        #if "%" not in txt:
                #txt = "0.0%"

        try:
            app.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            #if txt == "100.0%":
                #break
            time.sleep(10)
        except:
            time.sleep(5)


# download status
def downstatus(statusfile,message):

    while True:
        if os.path.exists(statusfile):
            break
        
    time.sleep(5)
    while os.path.exists(statusfile):

        with open(statusfile,"r") as upread:
            txt = upread.read()
        
        #if "%" not in txt:
                #txt = "0.0%"

        try:
            app.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            #if txt == "100.0%":
                #break
            time.sleep(10)
        except:
            time.sleep(5)


# app messages
@app.on_message(filters.command(['start']))
def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id, f"Welcome {message.from_user.mention}\nSend a **File** first and then **Extension**\n\n{START_TEXT}", reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(oldm,30),daemon=True)
    dm.start()                        


# help
@app.on_message(filters.command(['help']))
def help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id,
                      "**/start - To Check Availabe Conversions\n/help - This Message\n/cancel - To Cancel\n/rename - To Rename\n/source - Github Source Code\n** \n **[TRUMBOTS]('https://t.me/movie_time_botonly')**", reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(oldm),daemon=True)
    dm.start() 


#source
@app.on_message(filters.command(['source']))
def source(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id, "**GITHUB - https://urlsopen.com/AUnx**"**", disable_web_page_preview=True, reply_to_message_id=message.id)
    dm = threading.Thread(target=lambda:dltmsg(oldm),daemon=True)
    dm.start() 


# rename
@app.on_message(filters.command(['rename']))
def rename(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    try:
        newname = message.text.split("/rename ")[1]
    except:
        app.send_message(message.chat.id, "Usage: **/rename new-file-name** (with extension)", reply_to_message_id=message.id)
        return

    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        oldm = app.send_message(message.chat.id, "Renaming", reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
        rn = threading.Thread(target=lambda:rname(nmessage,newname,oldm),daemon=True)
        rn.start() 
        os.remove(f'{message.from_user.id}.json')
    else:
        app.send_message(message.chat.id, "You need to send me a File first", reply_to_message_id=message.id)   



# cancel
@app.on_message(filters.command(['cancel']))
def source(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')
        app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
        app.send_message(message.chat.id,"Your job was **Canceled**",reply_markup=ReplyKeyboardRemove(), reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id,"No job to Cancel", reply_to_message_id=message.id)     


# dalle command
@app.on_message(filters.command(["imagegen"]))
def getpompt(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# getting prompt from the text
	try:
		prompt = message.text.split("/imagegen ")[1]
	except:
		app.send_message(message.chat.id,'Send Prompt with Command,\nUssage : **/imagegen high defination studio image of pokemon**', reply_to_message_id=message.id)
		return	

	# threding	
	app.send_message(message.chat.id,"Prompt received and Request is sent. Waiting time is 1-2 mins", reply_to_message_id=message.id)
	ai = threading.Thread(target=lambda:genrateimages(message,prompt),daemon=True)
	ai.start()


# cog video
@app.on_message(filters.command(["videogen"]))
def videocog(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    app.send_message(message.chat.id,'Currently Not Working', reply_to_message_id=message.id)
    return
    
    try:
        prompt = message.text.split("/videogen ")[1]    
    except:
        app.send_message(message.chat.id,'Send Prompt with Command,\nUssage : **/videogen a man climbing up a mountain**', reply_to_message_id=message.id)
        return	

	# threding
    vi = threading.Thread(target=lambda:genratevideos(message,prompt),daemon=True)
    vi.start()
    


@app.on_message(filters.document)
def documnet(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.document.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=VAboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(IMG):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__COLORIZE, POSITIVE & UPSCALE__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=IMGboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBW):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 💼 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{LBW_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=LBWboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBC):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 💼 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{LBC_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=LBCboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(LBI):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 💼 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{LBI_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=LBIboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(FF):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 🔤 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{FF_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=FFboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(EB):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📚 \nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{EB_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=EBboard, reply_to_message_id=message.id)

    elif message.document.file_name.upper().endswith(ARC):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.document.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 🗄\nDo you want to Extract ?\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=ARCboard, reply_to_message_id=message.id)

    else:
        oldm = app.send_message(message.chat.id,'No Available Conversions Found, Trying to Read File',reply_markup=ReplyKeyboardRemove())
        rf = threading.Thread(target=lambda:readf(message,oldm,allowrename=True),daemon=True)
        rf.start()


@app.on_message(filters.animation)
def annimations(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    oldm = app.send_message(message.chat.id,'Turning it into Document then you can use that to Convert',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=message.id)
    sd = threading.Thread(target=lambda:senddoc(message,oldm),daemon=True)
    sd.start()


@app.on_message(filters.video)
def video(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    try:
        if message.video.file_name.upper().endswith(VIDAUD):
            with open(f'{message.from_user.id}.json', 'wb') as handle:
                pickle.dump(message, handle)
            dext = message.video.file_name.split(".")[-1].upper()
            app.send_message(message.chat.id,
                            f'Detected Extension: **{dext}** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                            reply_markup=VAboard, reply_to_message_id=message.id)
        else:
            app.send_message(message.chat.id, f'--**Available formats**--:\n\n**VIDEOS/AUDIOS** 📹 / 🔊\n__{VA_TEXT}__',
                            reply_to_message_id=message.id)
   
    except:
        oldm = app.send_message(message.chat.id,'Turning it into Document then you can use that to Convert',reply_markup=ReplyKeyboardRemove())
        sd = threading.Thread(target=lambda:senddoc(message,oldm),daemon=True)
        sd.start()


@app.on_message(filters.video_note)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'Detected Extension: **MP4** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                reply_markup=VAboard, reply_to_message_id=message.id)


@app.on_message(filters.audio)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    if message.audio.file_name.upper().endswith(VIDAUD):
        with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
        dext = message.audio.file_name.split(".")[-1].upper()
        app.send_message(message.chat.id,
                         f'Detected Extension: **{dext}** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                         reply_markup=VAboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id, f'--**Available formats**--:\n\n**VIDEOS/AUDIOS** 📹 / 🔊 \n__{VIDAUD}__',
                         reply_to_message_id=message.id)


@app.on_message(filters.voice)
def audio(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                f'Detected Extension: **OGG** 📹 / 🔊\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{VA_TEXT}__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                reply_markup=VAboard, reply_to_message_id=message.id)


@app.on_message(filters.photo)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
        pickle.dump(message, handle)
    app.send_message(message.chat.id,
                     f'Detected Extension: **JPG** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__COLORIZE, POSITIVE & UPSCALE__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                     reply_markup=IMGboard, reply_to_message_id=message.id)


@app.on_message(filters.sticker)
def photo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    with open(f'{message.from_user.id}.json', 'wb') as handle:
            pickle.dump(message, handle)
    if not message.sticker.is_animated and not message.sticker.is_video:
        app.send_message(message.chat.id,
                     f'Detected Extension: **WEBP** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__COLORIZE, POSITIVE & UPSCALE__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                     reply_markup=IMGboard, reply_to_message_id=message.id)
    else:
        app.send_message(message.chat.id,
                    f'Detected Extension: **TGS** 📷\nNow send extension to Convert to...\n\n--**Available formats**-- \n\n__{IMG_TEXT}__\n\n**SPECIAL** 🎁\n__COLORIZE, POSITIVE & UPSCALE__\n\n{message.from_user.mention} choose or click /cancel to Cancel or use /rename new-filename to rename',
                    reply_markup=IMGboard, reply_to_message_id=message.id)


@app.on_message(filters.text)
def text(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):  

    if os.path.exists(f'{message.from_user.id}.json'):
        with open(f'{message.from_user.id}.json', 'rb') as handle:
            nmessage = pickle.loads(handle.read())
        os.remove(f'{message.from_user.id}.json')

        if "COLOR" == message.text or "POSITIVE" == message.text:

            oldm = app.send_message(message.chat.id,'Processing',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id) 
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])

            if "COLOR" in message.text:
                col = threading.Thread(target=lambda:colorizeimage(nmessage,oldm),daemon=True)
                col.start()
                return
            else:
                pos = threading.Thread(target=lambda:negetivetopostive(nmessage,oldm),daemon=True)
                pos.start() 
                return

        if "READ" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Reading File',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            rf = threading.Thread(target=lambda:readf(nmessage,oldm),daemon=True)
            rf.start()
            return

        if "SENDPHOTO" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Photo',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            sp = threading.Thread(target=lambda:sendphoto(nmessage,oldm),daemon=True)
            sp.start()
            return

        if "SENDDOC" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Document',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            sd = threading.Thread(target=lambda:senddoc(nmessage,oldm),daemon=True)
            sd.start()
            return    

        if "SENDVID" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Sending Video',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            sv = threading.Thread(target=lambda:sendvideo(nmessage,oldm),daemon=True)
            sv.start()
            return

        if "SpeechToText" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Transcripting, takes long time for Long Files',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            stt = threading.Thread(target=lambda:transcript(nmessage,oldm),daemon=True)
            stt.start()
            return

        if "TextToSpeech" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Generating Speech',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            tts = threading.Thread(target=lambda:speak(nmessage,oldm),daemon=True)
            tts.start()
            return

        if "UPSCALE" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Upscaling Your Image',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            upscl = threading.Thread(target=lambda:increaseres(nmessage,oldm),daemon=True)
            upscl.start()
            return

        if "EXTRACT" == message.text:
            app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])
            oldm = app.send_message(message.chat.id,'Extracting File',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=nmessage.id)
            ex = threading.Thread(target=lambda:extract(nmessage,oldm),daemon=True)
            ex.start()
            return 

        if "document" in str(nmessage):
            inputt = nmessage.document.file_name
            print("File is a Document")
        else:
            if "audio" in str(nmessage) or "voice" in str(nmessage):
                try:
                    inputt = nmessage.audio.file_name
                    print("File is a Audio")
                except:
                    inputt = "voice.ogg"
                    print("File is a Voice")
            else:
                if "voice" in str(nmessage):
                    inputt = "voice.ogg"
                    print("File is a Voice")
                else:
                    if "sticker" in str(nmessage):
                        if not nmessage.sticker.is_animated and not nmessage.sticker.is_video:
                            inputt = nmessage.sticker.set_name + ".webp"
                        else:
                            inputt = nmessage.sticker.set_name + ".tgs"
                        print("File is a Sticker")
                    else:
                        if "video" in str(nmessage):
                            try:
                                inputt = nmessage.video.file_name
                                print("File is a Video")
                            except:
                                inputt = "video_note.mp4"
                                print("File is a Video Note")     
                        else:
                            if "video_note" in str(nmessage):
                                inputt = "voice_note.mp4"
                                print("File is a Video Note")   
                            else:
                                if "photo" in str(nmessage):
                                    temp = app.download_media(nmessage)
                                    inputt = temp.split("/")[-1]
                                    os.remove(temp)
                                    print("File is a Photo")
                                else:
                                    inputt = ""

        newext = message.text.lower()
        oldext = inputt.split(".")[-1]

        #if newext == "ico":
            #app.send_message(message.chat.id, "Warning: for ICO, image will be resized and made multi-resolution", reply_to_message_id=message.id)
        
        app.send_message(message.chat.id, f'Converting from **{oldext.upper()}** to **{newext.upper()}**', reply_to_message_id=nmessage.id, reply_markup=ReplyKeyboardRemove())
        app.delete_messages(message.chat.id,message_ids=[nmessage.id+1])

        conv = threading.Thread(target=lambda: follow(nmessage, inputt, newext, message), daemon=True)
        conv.start()

    else:
        if message.from_user.id == message.chat.id:
            #app.send_message(message.chat.id, "First send me a File", reply_to_message_id=message.id)
            oldm = app.send_message(message.chat.id,'Making File',reply_markup=ReplyKeyboardRemove(), reply_to_message_id=message.id)
            mf = threading.Thread(target=lambda:makefile(message,oldm),daemon=True)
            mf.start()
            

#apprun
print("Bot Started")
app.run()
