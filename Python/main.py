from dotenv import load_dotenv
load_dotenv()
import json
import os
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory


# Access the API key
bot_token = os.getenv('TELEGRAM-KEY')

# we need to make a basic tele

import requests

def set_webhook(bot_token, webhook_url):
    url = f'https://api.telegram.org/bot{bot_token}/setWebhook'
    payload = {
        'url': webhook_url
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print('Webhook set successfully!')
    else:
        print('Failed to set webhook.')
        print('Error:', response.text)


webhook_url = 'https://server.azalamer.com'
# this needs us to use ngrok, note that we need to find a way to keep this constant, 
# or push it to my domain url as a subaddress

set_webhook(bot_token, webhook_url+'/telegram-webhook')


SAVE_DIRECTORY = "./images"
BASE_URL = f"https://api.telegram.org/bot{bot_token}/"
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

def get_file_path(file_id):
    url = f"{BASE_URL}getFile"
    response = requests.get(url, params={"file_id": file_id})
    return response.json()["result"]["file_path"]

def download_file(file_path):
    url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    response = requests.get(url)
    return BytesIO(response.content)

def process_image(image_data):
    # Example processing: resize image
    return image_data
def databaseAdder(file_id,caption,url):
    # open the file
    with open('imageCaptionDatabase.json', 'r') as f:
        imageCaptionDatabase = json.load(f)
    imageCaptionDatabase[len(imageCaptionDatabase)] = {'url':url,'caption':caption,'file_id':file_id}
    with open('imageCaptionDatabase.json', 'w') as f:
        json.dump(imageCaptionDatabase, f)
        
def renumber_dict_keys(data, n):
    # Convert string keys to integers for sorting
    sorted_keys = sorted(map(int, data.keys()))
    
    # Remove the first n items
    keys_to_remove = sorted_keys[:n]
    for key in keys_to_remove:
        del data[str(key)]
    
    # Create a new dictionary with renumbered keys
    new_data = {}
    for i, key in enumerate(sorted_keys[n:]):
        new_key = str(i)
        new_data[new_key] = data[str(key)]
    
    return new_data



from flask_cors import CORS

app = Flask(__name__)
CORS(app)


IMAGE_DIRECTORY = "./images"

@app.route('/telegram-webhook', methods=['POST'])
# load the imageCaptionDatabase from the json file

def webhook():
    # Get the input data from the request
    input_data = request.json

    # Extract the relevant information from the input data
    
    try:
        file = input_data['message']['photo'][-1] # Get the largest photo
        file_id = file['file_id']  
        caption = ''
        try:
            caption = input_data['message']['caption']
        except Exception as e:
            print('error',e)
        print({'caption':caption,'file_id':file_id})
        file_path = get_file_path(file_id)
        # at this point, we need to add it to our imageCaptionDatabase. The database goes 'url':url,'caption':caption, 'file_id':file_id. each time we get a new image, we add it as the next index in the database
        databaseAdder(file_id,caption,webhook_url+SAVE_DIRECTORY[1:]+'/'+file_id+'.jpg')
        image_data = Image.open(download_file(file_path))
        
        
        # processed_image = process_image(image_data)
        
        # Save the processed image
        save_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.jpg")
        image_data.save(save_path)
    except Exception as e:
        print('error',e)
        print('No image found in the message')
        messange_text = input_data['message']['text']

        if(messange_text.lower() == 'wipe'):
            with open('imageCaptionDatabase.json', 'w') as f:
                json.dump({}, f)
            # delete all the images in the images folder
            for filename in os.listdir(SAVE_DIRECTORY):
                file_path = os.path.join(SAVE_DIRECTORY, filename)
                os.remove(file_path)
            with open('imageCaptionDatabase.json', 'r') as f:
                imageCaptionDatabase = json.load(f)
            response = f'{len(imageCaptionDatabase)} images and captions were deleted.'

        
        elif(messange_text.lower() == 'status'):
            with open('imageCaptionDatabase.json', 'r') as f:
                imageCaptionDatabase = json.load(f)
            response = f"Number of images: {len(imageCaptionDatabase)}"
        else:
            response = 'No image or caption was sent'

        chat_id = input_data['message']['chat']['id']
        result = response
        # TODO we should add a "wipe" command to the bot, and a "status" command to the bot as well
        print(f"message_text: {response}")
        print(f"chat_id: {chat_id}")

        # Send the result back to Telegram
        send_message(chat_id, result)



    return 'OK'
def send_message(chat_id, text):
    # Send a message back to Telegram using the sendMessage method
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)




@app.route('/', methods=['GET'])
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/controller', methods=['POST'])
# on this controller route, we will take a request which contains the number of images requested, so that the user only gets the number of images they want
# then earlier we constructed our imageDatabase which now includes captions, so we will return the imageDatabase to the user

def handle_request():
    # the request should contain the number of images requested
    data = request.json
    num_images = data['numImages']
    # remove .DS_Store file from list of images
    responsePackage = {}
    with open('imageCaptionDatabase.json', 'r') as f:
        imageCaptionDatabase = json.load(f)

    if(num_images > len(imageCaptionDatabase)):
        num_images = len(imageCaptionDatabase)
    # this makes it so we can only accept the number of images we have to give
    for i in range(num_images):
        responsePackage[i] = imageCaptionDatabase[str(i)]
    

    response_data = {
        'success': True,
        'message': 'Image URLs retrieved successfully',
        'imageUrls': imageCaptionDatabase,
        'numImages': num_images
    }

    return jsonify(response_data)


@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(IMAGE_DIRECTORY, filename)


@app.route('/confirmation',methods = ['POST'])
def conformationAndDeletion():
    data = request.json['imageIDs']
    # data is just a list of the fileID's that we need to delete
    # we should delete the image from the images folder
    for i in range(len(data)):
        save_path = os.path.join(SAVE_DIRECTORY, f"{data[i]}.jpg")
        os.remove(save_path)
    # we should also delete the image from the imageCaptionDatabase
    with open('imageCaptionDatabase.json', 'r') as f:
        imageCaptionDatabase = json.load(f)
    with open('imageCaptionDatabase.json', 'w') as f:
        json.dump(renumber_dict_keys(imageCaptionDatabase,len(data)), f)
    
    # 
    
    # find the index in the database that has the fileID that we need to delete
    
    # upon reflection, while this is implicit, the only images that get served are the ones at the top, not the back. So if I want I can just delete the first n entries in the database and renumber

    

    return jsonify({'success':True,'message':'Image deleted successfully'})

if __name__ == '__main__':
    print('Starting the Flask app')
    print(f"bot token: {bot_token[:5]}...{bot_token[-5:]}")
    app.run(port=8000)
