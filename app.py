from flask import Flask, render_template,request,send_file,jsonify
from audio_encrpy import Steganography
from audio_decrpy import Steganaograpy_decryption
import os
from werkzeug.utils import secure_filename
from time import sleep

app=Flask('__name__')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'uploads')
app.config['EXTENSIONS'] = {'wav'}


@app.route('/loader')
def loader():
    return render_template('loader.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hide')
def hide():
    return render_template('hide.html')

@app.route('/encrypt',methods=["POST"])
def stegno_enc():
    msgs=request.form.get("message")
    print("msgs")
    sngs = request.files.get('file')
    file_name = secure_filename(sngs.filename)
    filename=file_name[:file_name.rindex(".")]+" encrypted.wav"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    sngs.save(filepath)
    print("till")
    file_data = Steganography().lsb(filepath,msgs)
    print("work done", filename)
    print('filedata',file_data)
    return render_template("encrpy_success.html")

@app.route('/decrypt',methods=['POST'])
def stegno_dec():
    sngs = request.files.get('file')
    filename = secure_filename(sngs.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    sngs.save(filepath)
    print("till")
    decoded_msg=Steganaograpy_decryption().decoder(filepath)
    print("worked till here")
    print(decoded_msg)

    return render_template("decrpy_success.html",decoded_msg=decoded_msg)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/extract')
def extract():
    return render_template('extract.html')

@app.route('/processes',methods=['POST'])
def process():
    song=request.form["file"]
    mesg=request.form["message"]

    if song and mesg:
        return jsonify({"success":" encryption"})

    else:
        return jsonify({'error':"Missing data"})

@app.route("/return-file/")
def return_file():
    return send_file("outputs/song_emb.wav")

@app.route('/extractsuccess')
def extractsuccess():
    return render_template('extractsuccess.html')


if __name__ == "__main__":
    app.run(debug=True,threaded=True)