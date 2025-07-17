from flask import Blueprint, jsonify
from supabase_client import supabase

tactile_paving_bp = Blueprint('tactile_paving', __name__)

@tactile_paving_bp.route('/tactile-paving', methods=['GET'])
def tactile_paving():
    res = supabase.table('pavement').select('*').eq('has_tactile_paving', True).execute()
    return jsonify(res.data)