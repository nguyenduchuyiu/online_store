from flask import Flask, request, jsonify
from flask_cors import CORS
import security as sc
import database_module as dm 
from dotenv import load_dotenv
load_dotenv('backend\key.env')

app = Flask(__name__)
CORS(app)


@app.route('/users/address')
def get_address():
    return jsonify({'result': ['Ha Noi', 'Bac Giang']})


@app.route('/users/check_user', methods=['POST'])
def check_register():
    data = request.get_json()
    contact_info = data.get('userId')
    
    if not contact_info:
        return jsonify({'error': 'Missing email or phone'}), 400
    
    user_exists = dm.is_registered(contact_info)
    
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

    user = dm.get_user_for_login(contact_info) 

    if not sc.check_password(user, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = sc.create_jwt_token(user['_key'])

    return jsonify({'token': token}), 200


'''
Processing a signup request.
'''
@app.route('/users/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = data.get('username')
    contact_info = data.get('userId')
    password = data.get('password')
    
    if not username or not contact_info or not type or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    success = dm.create_user(username, contact_info, password)
    
    if success:
        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create user'}), 400
    


@app.route('/users/user', methods=['GET'])
def get_current_user():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    userKey = sc.decode_jwt_token(token=auth_header)
    
    if userKey is None:
        return jsonify({"error": "Session expired"}), 404
        
    user = dm.get_user_by_key(userKey)
        
    if user is not None:
        return jsonify({'result': user}), 200
    
    return jsonify({'error':'User not found'}), 404


def get_user_info():
    # user_info = dm.get_user_info()
    return jsonify({
        'result': {
                    "_key": 1,
                    "cartItems": [
                        {
                        "productKey": 1,
                        "noOfItems":1,
                        "variationQuantity":1
                        },
                    ],
                    "deliveryAddress": "Ha Noi",
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


@app.route('/products/get-all-products')
def get_products_by_category():
    category = request.args.get('category')
    
    if not category:
        return jsonify({"error": "Category parameter is required"}), 400
    
    product_data_list = dm.get_product_from_category(category)  # Adapt to fetch by category
    
    if product_data_list:
        return jsonify({'result':product_data_list}), 200
    else:
        return jsonify({"error": "Products not found for the given category"}), 404
    
    
@app.route('/products/get-all-categories')
def get_all_categories(): 
    category_data_list = dm.get_categories()
    
    if category_data_list:
        return jsonify({'result': category_data_list}), 200
    else:
        return jsonify({"error": "Categories not found"}), 404


@app.route('/products/search-product')
def search_product():
    search_term = request.args.get('searchTerm')
    if not search_term:
        return jsonify({"error": "Search term parameter is required"}), 400
    
    product_data_list = dm.search_products_by_name(search_term) 
    
    if product_data_list:
        return jsonify({'result':product_data_list}), 200
    else:
        return jsonify({"error": "Product not found"}), 404


@app.route('/users/add-to-cart', methods=['POST'])
def addToCart():
    data = request.get_json()
    cartItem = data['cartItem']
    userKey = data['userKey']
    if dm.add_to_cart(cartItem, userKey):
        return jsonify({"result": "Succesfully add to your cart"}), 200
    return jsonify({"error":"Failure adding to your cart"}), 400
   
    
@app.route('/users/get-cart-items', methods=['POST'])
def getCartItems():
    data = request.get_json()
    userKey = data['userKey']
    cart_items = dm.get_cart_items(userKey)
    
    if cart_items:
        return jsonify({"result":cart_items}), 200
    
    return jsonify({"error":"Cart items not found"}), 404





# @app.route('/images/<string:product_name>')
# def get_image(product_name):
#     image_path = f'/static/images/{product_name}.png'
#     return render_template('template.html', image_path=image_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)