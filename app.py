from flask import Flask, request
import cloudinary
import cloudinary.uploader
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import json

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    cam_id        = request.form.get('cid')
    cam_timestamp = request.form.get('ts')
    sensor_data   = json.loads(request.form.get('sensor'))
    img           = request.files.get('img')
    gps_timestamp = sensor_data.get('gpsTs')
    lat           = sensor_data.get('lat')
    lng           = sensor_data.get('lng')
    spd           = sensor_data.get('spd')
    accs          = sensor_data.get('accs')

    if not img:
        return 'Invalid request', 400
    
    result = cloudinary.uploader.upload(img)
    url = result['secure_url']
    
    data = {
        'camera_id':        cam_id,
        'camera_timestamp': cam_timestamp,
        'gps_timestamp':    gps_timestamp,
        'latitude':         lat,
        'longitude':        lng,
        'speed':            spd,
        'accelerations':    accs,
        'image_url':        url,
    }

    try:
        supabase.table('pavement').insert(data).execute()
        return 'Success', 200
    except Exception as e:
        return 'DB error', 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)