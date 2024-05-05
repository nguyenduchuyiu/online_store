import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from security import check_password, create_jwt_token
from database_module import get_product_data, get_user, is_registered, create_user
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required, get_jwt_identity
load_dotenv('backend\key.env')

app = Flask(__name__)
CORS(app)

''' 
Check if a user exists in database.
'''
@app.route('/users/check_user', methods=['POST'])
def check_register():
    data = request.get_json()
    contact_info = data.get('userId')
    
    if not contact_info:
        return jsonify({'error': 'Missing email or phone'}), 400
    
    user_exists = is_registered(contact_info)
    
    return jsonify({'result': user_exists}), 200
    
    
'''
Processing a login request.
'''
@app.route('/users/login', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    contact_info = data.get('userId')
    password = data.get('password')
    if not contact_info or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = get_user(contact_info) 

    if not check_password(user, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_jwt_token(user['id'])

    return jsonify({'token': token}), 200


'''
Processing a signup request.
'''
@app.route('/users/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = data.get('username')
    contact_info = data.get('userId')
    info_type = data.get('type')
    password = data.get('password')
    
    if not username or not contact_info or not type or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    success = create_user(username, contact_info, info_type, password)
    
    if success:
        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create user'}), 400
    

'''
Processing an user getting request.
'''
# @jwt_required()  # Requires a valid JWT token
@app.route('/users/user', methods=['GET'])
def get_user_info():
    return jsonify({
        'result': {
                    "_key": "ex_key",
                    "cartItems": [
                        {
                        "productKey": "ex_productKey",
                        "noOfItems":1,
                        "variationQuantity":1
                        },
                    ],
                    "deliveryAddress": [
                        {
                        "address": "ex_address",
                        "point": "ex_point"
                        }
                    ],
                    "deviceToken": "ex_deviceToken",
                    "dob": 1678886400000,
                    "emailId": "huy@gmail.com",
                    "shopName": "nguyenduchuyiu",
                    "orders": ["ex_order1", "ex_order2"],
                    "phoneNo": "0337 118 147",
                    "profilePic": "ex_profilePic",
                    "userType": "customer",
                    "proprietorName": "Nguyen Duc Huy",
                    "gst": "2354123412" 
                    }
    })
# @jwt_required()
# def get_user_info():
#     try:
#         user_id = get_jwt_identity()
#         user = get_user(user_id)

#         if not user:
#             return jsonify({'error': 'User not found'}), 404

#         return jsonify({
#             "result": {
#                 "id": user['id'],
#                 "name": user['username']
#                 # ... other user information
#             }
#         })

#     except Exception as e:
#         logging.error(f"Error retrieving user information: {e}")
#         return jsonify({'error': 'An error occurred while processing your request'}), 500


@app.route('/products/get-all-products')
def get_products_by_category():
    category = request.args.get('category')
    
    if not category:
        return jsonify({"error": "Category parameter is required"}), 400
    
    product_data_list = get_product_data(category=category)  # Adapt to fetch by category
    
    if product_data_list:
        return product_data_list, 200
    else:
        return jsonify({"error": "Products not found for the given category"}), 404

    
UPLOAD_FOLDER = 'backend/assets/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import os
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'Không có file được chọn'
        file = request.files['image']
        if file.filename == '':
            return 'Không có file được chọn'
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return 'File đã được upload!'
    return render_template('upload.html')

@app.route('/images/<string:product_name>')
def get_image(product_name):
    image_path = f'/static/images/{product_name}.png'
    return render_template('template.html', image_path=image_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)