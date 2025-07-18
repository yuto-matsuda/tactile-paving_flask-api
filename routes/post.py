from flask import Blueprint, request
from supabase_client import supabase
import cloudinary_config
import cloudinary.uploader
import json

post_bp = Blueprint('post', __name__)

@post_bp.route('/post', methods=['POST'])
def post():
    img           = request.data
    cam_id        = int(request.headers.get('cid'))
    cam_timestamp = request.headers.get('ts')
    sensor_data   = json.loads(request.headers.get('sensor'))
    gps_timestamp = sensor_data.get('gpsTs')
    lat           = sensor_data.get('lat')
    lng           = sensor_data.get('lng')
    spd           = sensor_data.get('spd')
    accs          = sensor_data.get('accs')

    for acc in accs:
        acc['ax'] = float(acc['ax'])
        acc['ay'] = float(acc['ay'])
        acc['az'] = float(acc['az'])

    # print(cam_id)
    # print(cam_timestamp)
    # print(sensor_data)

    if not img:
        return 'Invalid request', 400
    
    fname = f'{cam_id}_{cam_timestamp}'.replace(':', '-')
    result = cloudinary.uploader.upload(img, public_id=fname)
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

# multipart/form-data用
# @post_bp.route('/post', methods=['POST'])
# def post():
#     data = request.get_data()
#     print("Actual received body length:", len(data))

#     cam_id        = int(request.form.get('cid'))
#     cam_timestamp = request.form.get('ts')
#     sensor_data   = json.loads(request.form.get('sensor'))
#     img           = request.files.get('img')
#     gps_timestamp = sensor_data.get('gpsTs')
#     lat           = sensor_data.get('lat')
#     lng           = sensor_data.get('lng')
#     spd           = sensor_data.get('spd')
#     accs          = sensor_data.get('accs')

#     for acc in accs:
#         acc['ax'] = float(acc['ax'])
#         acc['ay'] = float(acc['ay'])
#         acc['az'] = float(acc['az'])

#     if not img:
#         return 'Invalid request', 400
    
#     fname = f'{cam_id}_{cam_timestamp}'.replace(':', '-')
#     result = cloudinary.uploader.upload(img, public_id=fname)
#     url = result['secure_url']
    
#     data = {
#         'camera_id':        cam_id,
#         'camera_timestamp': cam_timestamp,
#         'gps_timestamp':    gps_timestamp,
#         'latitude':         lat,
#         'longitude':        lng,
#         'speed':            spd,
#         'accelerations':    accs,
#         'image_url':        url,
#     }

#     try:
#         supabase.table('pavement').insert(data).execute()
#         return 'Success', 200
#     except Exception as e:
#         return 'DB error', 500