from flask import *

import IC_Flask, AES

app = Flask(__name__)
app.secret_key="sec"



@app.route('/')
def sender():
	return render_template("index.html")

@app.route('/', methods=['POST'])
def encrypt():
	if request.method=='POST':

		f=request.files['userfile']
		img_path="./static/{}".format(f.filename)  #.static/images.jpg
		f.save(img_path)

		caption=IC_Flask.caption_this_image(img_path)
		caption_path=img_path[:-4]
		caption_path+='.txt'


		with open(caption_path, "w") as f:
			f.write(caption)    

		enc_img=AES.convertFile(img_path, 1)
		enc_caption=AES.convertFile(caption_path, 1)
		
		result_dic={
			'image': enc_img,
			'caption': enc_caption
		}

		session['enc_dic']=result_dic


	return render_template("index.html", your_result=result_dic)


@app.route('/receiver')
def receiver():
	enc_dic={}

	if 'enc_dic' in session:
		enc_dic = session['enc_dic']

	enc_img=enc_dic['image']
	enc_caption=enc_dic['caption']

	# print(enc_img)	
	# print(enc_caption)
	
	dec_img=AES.convertFile(enc_img, 2)
	dec_caption=AES.convertFile(enc_caption, 2)
	caption=""

	with open(dec_caption, "r") as f:
		caption = f.read()

	result_dic={
		'image': dec_img,
		'caption': caption
	}
  	

	return render_template("receiver.html", your_result=result_dic)

if __name__ == '__main__':
	app.run(debug = True)	