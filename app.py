
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, date, timedelta
from sqlalchemy import Numeric, UniqueConstraint
import jwt
import os
from decimal import Decimal, InvalidOperation

# ==============================
# FLASK CONFIGURATION
# ==============================

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY',
    'dev-secret-key-change-before-submission'
)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://root:@localhost/web_store_db'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==============================
# DATABASE MODELS
# ==============================

# Role model
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    users = db.relationship('User', backref='user_role')


# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id'),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Client model
class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    address = db.Column(db.String(255))

    orders = db.relationship('Order', backref='client')


# Category model
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# Brand model
class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# Gender model
class Gender(db.Model):
    __tablename__ = 'genders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# Size model
class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


# Color model
class Color(db.Model):
    __tablename__ = 'colors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# Product model
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    # Original price and initial stock quantity
    price = db.Column(Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=False
    )

    brand_id = db.Column(
        db.Integer,
        db.ForeignKey('brands.id'),
        nullable=False
    )

    gender_id = db.Column(
        db.Integer,
        db.ForeignKey('genders.id'),
        nullable=False
    )

    category = db.relationship('Category')
    brand = db.relationship('Brand')
    gender = db.relationship('Gender')

    sizes = db.relationship(
        'ProductSize',
        backref='product',
        cascade='all, delete-orphan'
    )

    colors = db.relationship(
        'ProductColor',
        backref='product',
        cascade='all, delete-orphan'
    )

    discounts = db.relationship(
        'Discount',
        backref='product',
        cascade='all, delete-orphan'
    )

    order_items = db.relationship('OrderItem', backref='product')


# ProductSize model
class ProductSize(db.Model):
    __tablename__ = 'product_sizes'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    size_id = db.Column(
        db.Integer,
        db.ForeignKey('sizes.id'),
        nullable=False
    )

    size = db.relationship('Size')

    __table_args__ = (
        UniqueConstraint(
            'product_id',
            'size_id',
            name='unique_product_size'
        ),
    )


# ProductColor model
class ProductColor(db.Model):
    __tablename__ = 'product_colors'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    color_id = db.Column(
        db.Integer,
        db.ForeignKey('colors.id'),
        nullable=False
    )

    color = db.relationship('Color')

    __table_args__ = (
        UniqueConstraint(
            'product_id',
            'color_id',
            name='unique_product_color'
        ),
    )


# Discount model
class Discount(db.Model):
    __tablename__ = 'discounts'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    percentage = db.Column(Numeric(5, 2), nullable=False)

    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)


# Order model
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id'),
        nullable=False
    )

    order_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default='pending'
    )

    total_amount = db.Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    items = db.relationship(
        'OrderItem',
        backref='order',
        cascade='all, delete-orphan'
    )


# OrderItem model
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id'),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)

    # Price at the time of purchase
    price = db.Column(Numeric(10, 2), nullable=False)


# ==============================
# HOME AND TEST ROUTES
# ==============================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({
        'message': 'Web Store API is working!'
    })

# ==============================
# JWT AUTHENTICATION
# ==============================

# Generate a JWT token
def generate_token(user):

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return token


# Verify JWT token
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token is missing'}), 401

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256']
            )

            current_user = db.session.get(User, payload['user_id'])

            if current_user is None:
                return jsonify({'error': 'User not found'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# Check user roles
def role_required(*allowed_roles):

    def decorator(f):

        @wraps(f)
        def decorated(current_user, *args, **kwargs):

            if current_user.user_role.name not in allowed_roles:
                return jsonify({
                    'error': 'You do not have permission to access this resource'
                }), 403

            return f(current_user, *args, **kwargs)

        return decorated

    return decorator


# ==============================
# USER REGISTRATION
# ==============================

@app.route('/api/register', methods=['POST'])
def register_user():

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({
            'error': 'Username, email and password are required'
        }), 400

    if len(password) < 8:
        return jsonify({
            'error': 'Password must contain at least 8 characters'
        }), 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return jsonify({
            'error': 'Username or email already exists'
        }), 409

    simple_role = Role.query.filter_by(name='simple_user').first()

    if not simple_role:
        return jsonify({'error': 'Default user role not found'}), 500

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role_id=simple_role.id
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'role': simple_role.name
        }
    }), 201


# ==============================
# USER LOGIN
# ==============================

@app.route('/api/login', methods=['POST'])
def login_user():

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'error': 'Username and password are required'
        }), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({
            'error': 'Invalid username or password'
        }), 401

    token = generate_token(user)

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.user_role.name
        }
    }), 200

# ==============================
# AUTHENTICATION TEST
# ==============================

# GET - View current user's profile
@app.route('/api/profile', methods=['GET'])
@token_required
def user_profile(current_user):

    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.user_role.name
    }), 200


# ==============================
# ROLE PERMISSION TEST
# ==============================

# GET - Admin-only test
@app.route('/api/admin-test', methods=['GET'])
@token_required
@role_required('admin')
def admin_test(current_user):

    return jsonify({
        'message': 'Welcome, Admin!',
        'username': current_user.username
    }), 200


# ==============================
# USER MANAGEMENT API
# ==============================

# Get all registered users (Admin only)
@app.route('/api/users', methods=['GET'])
@token_required
@role_required('admin')
def get_users(current_user):

    users = User.query.all()

    users_list = []

    for user in users:
        users_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.user_role.name
        })

    return jsonify(users_list), 200
# Create a new user (Admin only)
@app.route('/api/users', methods=['POST'])
@token_required
@role_required('admin')
def create_user(current_user):

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')

    # Validate required fields
    if not username or not email or not password or not role_name:
        return jsonify({'error': 'All fields are required'}), 400

    # Validate password length
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    # Check if username or email already exists
    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        return jsonify({
            'error': 'Username or email already exists'
        }), 409

    # Find the requested role
    role = Role.query.filter_by(name=role_name).first()

    if not role:
        return jsonify({'error': 'Invalid role'}), 400

    # Create the new user
    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role_id=role.id
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.user_role.name
        }
    }), 201
# Update a user's role (Admin only)
@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@token_required
@role_required('admin')
def update_user_role(current_user, user_id):

    data = request.get_json()

    role_name = data.get('role')

    # Validate required field
    if not role_name:
        return jsonify({'error': 'Role is required'}), 400

    # Find the user
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Find the new role
    role = Role.query.filter_by(name=role_name).first()

    if not role:
        return jsonify({'error': 'Invalid role'}), 400

    # Update the user's role
    user.role_id = role.id

    db.session.commit()

    return jsonify({
        'message': 'User role updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.user_role.name
        }
    }), 200

# Delete a user (Admin only)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_user(current_user, user_id):

    # Find the user
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Prevent admin from deleting their own account
    if user.id == current_user.id:
        return jsonify({
            'error': 'You cannot delete your own account'
        }), 400

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'message': 'User deleted successfully'
    }), 200
# ==============================
# PRODUCT API
# ==============================

def product_to_dict(product):

    # Find an active discount
    current_time = datetime.now()

    active_discount = Discount.query.filter(
        Discount.product_id == product.id,
        Discount.start_date <= current_time,
        Discount.end_date >= current_time
    ).first()

    original_price = Decimal(str(product.price))
    discount_percentage = Decimal('0')

    if active_discount:
        discount_percentage = Decimal(
            str(active_discount.percentage)
        )

    discounted_price = original_price * (
        Decimal('1') - discount_percentage / Decimal('100')
    )

    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(original_price),
        'discount_percentage': float(discount_percentage),
        'discounted_price': float(discounted_price),
        'quantity': product.quantity - get_sold_quantity(product.id),
'total_quantity': product.quantity,
        'category': product.category.name,
        'brand': product.brand.name,
        'gender': product.gender.name,
        'sizes': [
            item.size.name for item in product.sizes
        ],
        'colors': [
            item.color.name for item in product.colors
        ]
    }


# GET - Retrieve all products
@app.route('/api/products', methods=['GET'])

def get_products():

    products = Product.query.all()

    return jsonify({
        'total': len(products),
        'products': [
            product_to_dict(product)
            for product in products
        ]
    }), 200

# GET - Retrieve one product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def get_product(current_user, product_id):
    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            'error': 'Product not found.'
        }), 404

    return jsonify({
        'product': product_to_dict(product)
    }), 200

# POST - Add a new product
@app.route('/api/products', methods=['POST'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def add_product(current_user):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    # Check required fields
    required_fields = [
        'name',
        'price',
        'quantity',
        'category_id',
        'brand_id',
        'gender_id'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Missing required field: {field}'
            }), 400

    # Validate product name
    if not isinstance(data['name'], str) or not data['name'].strip():
        return jsonify({
            'error': 'Product name cannot be empty.'
        }), 400

    # Validate price
    try:
        price = Decimal(str(data['price']))

        if not price.is_finite() or price <= 0:
            raise InvalidOperation

    except (InvalidOperation, ValueError):
        return jsonify({
            'error': 'Price must be a valid positive number.'
        }), 400

    # Validate quantity
    try:
        quantity = int(data['quantity'])

        if isinstance(data['quantity'], bool):
            raise ValueError

        if quantity < 0 or str(data['quantity']).strip() != str(quantity):
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            'error': 'Quantity must be a non-negative integer.'
        }), 400

    # Find category, brand and gender
    category = db.session.get(Category, data['category_id'])
    brand = db.session.get(Brand, data['brand_id'])
    gender = db.session.get(Gender, data['gender_id'])

    if not category:
        return jsonify({
            'error': 'Category not found.'
        }), 404

    if not brand:
        return jsonify({
            'error': 'Brand not found.'
        }), 404

    if not gender:
        return jsonify({
            'error': 'Gender not found.'
        }), 404

    # Get optional sizes and colors
    size_ids = data.get('size_ids', [])
    color_ids = data.get('color_ids', [])

    if not isinstance(size_ids, list) or not isinstance(color_ids, list):
        return jsonify({
            'error': 'size_ids and color_ids must be lists.'
        }), 400

    sizes = []
    colors = []

    for size_id in size_ids:
        size = db.session.get(Size, size_id)

        if not size:
            return jsonify({
                'error': f'Size with ID {size_id} not found.'
            }), 404

        sizes.append(size)

    for color_id in color_ids:
        color = db.session.get(Color, color_id)

        if not color:
            return jsonify({
                'error': f'Color with ID {color_id} not found.'
            }), 404

        colors.append(color)




    # Create the product
    product = Product(
        name=data['name'].strip(),
        description=data.get('description', ''),
        price=price,
        quantity=quantity,
        category_id=category.id,
        brand_id=brand.id,
        gender_id=gender.id
    )

    db.session.add(product)

    # Save the product first to generate its ID
    db.session.flush()

    # Connect sizes to the product
    for size in sizes:
        db.session.add(ProductSize(
            product_id=product.id,
            size_id=size.id
        ))

    # Connect colors to the product
    for color in colors:
        db.session.add(ProductColor(
            product_id=product.id,
            color_id=color.id
        ))

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not save the product.'
        }), 500

    return jsonify({
        'message': 'Product added successfully!',
        'product': product_to_dict(product)
    }), 201

# PUT - Update an existing product
@app.route('/api/products/<int:product_id>', methods=['PUT'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def update_product(current_user, product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            'error': 'Product not found.'
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    try:
        # Update product name
        if 'name' in data:
            if not isinstance(data['name'], str) or not data['name'].strip():
                return jsonify({
                    'error': 'Product name cannot be empty.'
                }), 400

            product.name = data['name'].strip()

        # Update description
        if 'description' in data:
            product.description = data['description']

        # Update price
        if 'price' in data:
            try:
                price = Decimal(str(data['price']))

                if not price.is_finite() or price <= 0:
                    raise InvalidOperation

                product.price = price

            except (InvalidOperation, ValueError):
                return jsonify({
                    'error': 'Price must be a valid positive number.'
                }), 400

        # Update quantity
        if 'quantity' in data:
            try:
                quantity = int(data['quantity'])

                if (
                    isinstance(data['quantity'], bool)
                    or quantity < 0
                    or str(data['quantity']).strip() != str(quantity)
                ):
                    raise ValueError

                product.quantity = quantity

            except (ValueError, TypeError):
                return jsonify({
                    'error': 'Quantity must be a non-negative integer.'
                }), 400

        # Update category
        if 'category_id' in data:
            category = db.session.get(Category, data['category_id'])

            if not category:
                return jsonify({
                    'error': 'Category not found.'
                }), 404

            product.category_id = category.id

        # Update brand
        if 'brand_id' in data:
            brand = db.session.get(Brand, data['brand_id'])

            if not brand:
                return jsonify({
                    'error': 'Brand not found.'
                }), 404

            product.brand_id = brand.id

        # Update gender
        if 'gender_id' in data:
            gender = db.session.get(Gender, data['gender_id'])

            if not gender:
                return jsonify({
                    'error': 'Gender not found.'
                }), 404

            product.gender_id = gender.id

                # Update sizes if provided
        if 'size_ids' in data:

            if not isinstance(data['size_ids'], list):
                return jsonify({
                    'error': 'size_ids must be a list.'
                }), 400

            if len(data['size_ids']) != len(set(data['size_ids'])):
                return jsonify({
                    'error': 'Duplicate size IDs are not allowed.'
                }), 400

            new_sizes = []

            for size_id in data['size_ids']:
                size = db.session.get(Size, size_id)

                if not size:
                    return jsonify({
                        'error': f'Size with ID {size_id} not found.'
                    }), 404

                new_sizes.append(size)

            # Remove old size relationships
            ProductSize.query.filter_by(
                product_id=product.id
            ).delete(synchronize_session=False)

            # Add new size relationships
            for size in new_sizes:
                db.session.add(ProductSize(
                    product_id=product.id,
                    size_id=size.id
                ))

            db.session.flush()

                # Update colors if provided
        if 'color_ids' in data:

            if not isinstance(data['color_ids'], list):
                return jsonify({
                    'error': 'color_ids must be a list.'
                }), 400

            if len(data['color_ids']) != len(set(data['color_ids'])):
                return jsonify({
                    'error': 'Duplicate color IDs are not allowed.'
                }), 400

            new_colors = []

            for color_id in data['color_ids']:
                color = db.session.get(Color, color_id)

                if not color:
                    return jsonify({
                        'error': f'Color with ID {color_id} not found.'
                    }), 404

                new_colors.append(color)

            # Remove old color relationships
            ProductColor.query.filter_by(
                product_id=product.id
            ).delete(synchronize_session=False)

            # Add new color relationships
            for color in new_colors:
                db.session.add(ProductColor(
                    product_id=product.id,
                    color_id=color.id
                ))

            db.session.flush()
            db.session.commit()

        return jsonify({
            'message': 'Product updated successfully!',
            'product': product_to_dict(product)
        }), 200

    except Exception as e:
        db.session.rollback()

        app.logger.exception("Error while updating product:")

        return jsonify({
            'error': str(e)
        }), 500


# DELETE - Remove a product
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@token_required
@role_required('admin', 'advanced_user')
def delete_product(current_user, product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            'error': 'Product not found.'
        }), 404

    # Do not delete products that have order history
    if product.order_items:
        return jsonify({
            'error': 'This product cannot be deleted because it has order history.'
        }), 409

    try:
        db.session.delete(product)
        db.session.commit()

        return jsonify({
            'message': 'Product deleted successfully!'
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not delete the product.'
        }), 500

# ==============================
# DISCOUNT API
# ==============================

# Convert discount information into JSON
def discount_to_dict(discount):

    return {
        'id': discount.id,
        'product_id': discount.product_id,
        'product_name': discount.product.name,
        'percentage': float(discount.percentage),
        'start_date': discount.start_date.isoformat(),
        'end_date': discount.end_date.isoformat()
    }


# Validate discount dates and percentage
def validate_discount(percentage, start_date, end_date):

    try:
        percentage = Decimal(str(percentage))

        if (
            not percentage.is_finite()
            or percentage <= 0
            or percentage > 100
        ):
            raise InvalidOperation

    except (InvalidOperation, ValueError, TypeError):
        return None, None, None, 'Discount must be between 0 and 100.'

    try:
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)

        # We use local, timezone-naive dates in this API
        if start_date.tzinfo is not None or end_date.tzinfo is not None:
            raise ValueError

        if start_date >= end_date:
            return None, None, None, 'End date must be after start date.'

    except (ValueError, TypeError):
        return None, None, None, (
            'Dates must use YYYY-MM-DDTHH:MM:SS format.'
        )

    return percentage, start_date, end_date, None


# Check whether another discount overlaps with this period
def discount_period_conflicts(
    product_id,
    start_date,
    end_date,
    exclude_discount_id=None
):

    query = Discount.query.filter(
        Discount.product_id == product_id,
        Discount.start_date <= end_date,
        Discount.end_date >= start_date
    )

    if exclude_discount_id is not None:
        query = query.filter(
            Discount.id != exclude_discount_id
        )

    return query.first() is not None


# POST - Add a discount to a product
@app.route('/api/products/<int:product_id>/discounts', methods=['POST'])
@token_required
@role_required('admin')
def add_discount(current_user, product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            'error': 'Product not found.'
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    required_fields = [
        'percentage',
        'start_date',
        'end_date'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Missing required field: {field}'
            }), 400

    percentage, start_date, end_date, error = validate_discount(
        data['percentage'],
        data['start_date'],
        data['end_date']
    )

    if error:
        return jsonify({'error': error}), 400

    if discount_period_conflicts(
        product_id,
        start_date,
        end_date
    ):
        return jsonify({
            'error': 'Another discount already exists during this period.'
        }), 409

    discount = Discount(
        product_id=product_id,
        percentage=percentage,
        start_date=start_date,
        end_date=end_date
    )

    try:
        db.session.add(discount)
        db.session.commit()

        return jsonify({
            'message': 'Discount added successfully!',
            'discount': discount_to_dict(discount)
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not add the discount.'
        }), 500


# GET - Retrieve all discounts for a product
@app.route('/api/products/<int:product_id>/discounts', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def get_product_discounts(current_user, product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            'error': 'Product not found.'
        }), 404

    discounts = Discount.query.filter_by(
        product_id=product_id
    ).order_by(Discount.start_date.desc()).all()

    return jsonify({
        'product_id': product.id,
        'product_name': product.name,
        'total': len(discounts),
        'discounts': [
            discount_to_dict(discount)
            for discount in discounts
        ]
    }), 200

# GET - Retrieve one discount by ID
@app.route('/api/discounts/<int:discount_id>', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def get_discount(current_user, discount_id):

    discount = db.session.get(Discount, discount_id)

    if not discount:
        return jsonify({
            'error': 'Discount not found.'
        }), 404

    return jsonify({
        'discount': discount_to_dict(discount)
    }), 200

# PUT - Update an existing discount
@app.route('/api/discounts/<int:discount_id>', methods=['PUT'])
@token_required
@role_required('admin')
def update_discount(current_user, discount_id):

    discount = db.session.get(Discount, discount_id)

    if not discount:
        return jsonify({
            'error': 'Discount not found.'
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    percentage_value = data.get(
        'percentage',
        discount.percentage
    )

    start_value = data.get(
        'start_date',
        discount.start_date.isoformat()
    )

    end_value = data.get(
        'end_date',
        discount.end_date.isoformat()
    )

    percentage, start_date, end_date, error = validate_discount(
        percentage_value,
        start_value,
        end_value
    )

    if error:
        return jsonify({'error': error}), 400

    if discount_period_conflicts(
        discount.product_id,
        start_date,
        end_date,
        exclude_discount_id=discount.id
    ):
        return jsonify({
            'error': 'Another discount already exists during this period.'
        }), 409

    try:
        discount.percentage = percentage
        discount.start_date = start_date
        discount.end_date = end_date

        db.session.commit()

        return jsonify({
            'message': 'Discount updated successfully!',
            'discount': discount_to_dict(discount)
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not update the discount.'
        }), 500


# DELETE - Remove a discount
@app.route('/api/discounts/<int:discount_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_discount(current_user, discount_id):

    discount = db.session.get(Discount, discount_id)

    if not discount:
        return jsonify({
            'error': 'Discount not found.'
        }), 404

    try:
        db.session.delete(discount)
        db.session.commit()

        return jsonify({
            'message': 'Discount deleted successfully!'
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not delete the discount.'
        }), 500

# ==============================
# STOCK MANAGEMENT API
# ==============================

# PUT - Update product stock quantity
@app.route('/api/products/<int:product_id>/stock', methods=['PUT'])
@token_required
@role_required('admin', 'advanced_user')
def update_product_stock(current_user, product_id):
    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            'error': 'Product not found.'
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    if 'quantity' not in data:
        return jsonify({
            'error': 'Quantity is required.'
        }), 400

    quantity = data['quantity']

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
        return jsonify({
            'error': 'Quantity must be a non-negative integer.'
        }), 400

    try:
        product.quantity = quantity
        db.session.commit()

        return jsonify({
            'message': 'Product stock updated successfully!',
            'product_id': product.id,
            'product_name': product.name,
            'quantity': product.quantity
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not update product stock.'
        }), 500


# GET - Retrieve real-time product quantity
@app.route('/api/products/<int:product_id>/quantity', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def get_product_quantity(current_user, product_id):

    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({
            'error': 'Product not found.'
        }), 404

    # Calculate the quantity sold in confirmed orders
    sold_quantity = db.session.query(
        db.func.coalesce(
            db.func.sum(OrderItem.quantity),
            0
        )
    ).join(
        Order,
        OrderItem.order_id == Order.id
    ).filter(
        OrderItem.product_id == product_id,
        Order.status.in_(['confirmed', 'shipped'])
    ).scalar()

    sold_quantity = int(sold_quantity)

    # Calculate the remaining quantity
    current_quantity = product.quantity - sold_quantity

    return jsonify({
        'product_id': product.id,
        'product_name': product.name,
        'initial_quantity': product.quantity,
        'sold_quantity': sold_quantity,
        'current_quantity': current_quantity
    }), 200

# ==============================
# ADVANCED PRODUCT SEARCH API
# ==============================

# GET - Search products using multiple filters
@app.route('/api/products/search', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def search_products(current_user):
    query = Product.query

    # Filter by category
    category = request.args.get('category')

    if category:
        query = query.filter(
            Product.category.has(
                Category.name.ilike(category)
            )
        )

    # Filter by gender
    gender = request.args.get('gender')

    if gender:
        query = query.filter(
            Product.gender.has(
                Gender.name.ilike(gender)
            )
        )

    # Filter by brand
    brand = request.args.get('brand')

    if brand:
        query = query.filter(
            Product.brand.has(
                Brand.name.ilike(brand)
            )
        )

    # Filter by minimum price
    price_min = request.args.get('price_min')

    if price_min is not None:
        try:
            price_min = Decimal(price_min)

            if not price_min.is_finite() or price_min < 0:
                raise InvalidOperation

            query = query.filter(
                Product.price >= price_min
            )

        except (InvalidOperation, ValueError):
            return jsonify({
                'error': 'Invalid minimum price.'
            }), 400

    # Filter by maximum price
    price_max = request.args.get('price_max')

    if price_max is not None:
        try:
            price_max = Decimal(price_max)

            if not price_max.is_finite() or price_max < 0:
                raise InvalidOperation

            query = query.filter(
                Product.price <= price_max
            )

        except (InvalidOperation, ValueError):
            return jsonify({
                'error': 'Invalid maximum price.'
            }), 400

    # Check that minimum price is not greater than maximum price
    if (
        price_min is not None
        and price_max is not None
        and price_min > price_max
    ):
        return jsonify({
            'error': 'Minimum price cannot exceed maximum price.'
        }), 400

    # Filter by size
    size = request.args.get('size')

    if size:
        query = query.filter(
            Product.sizes.any(
                ProductSize.size.has(
                    Size.name.ilike(size)
                )
            )
        )

    # Filter by color
    color = request.args.get('color')

    if color:
        query = query.filter(
            Product.colors.any(
                ProductColor.color.has(
                    Color.name.ilike(color)
                )
            )
        )

    # Calculate quantities sold in confirmed orders
    sold_quantity = (
        db.session.query(
            db.func.coalesce(
                db.func.sum(OrderItem.quantity),
                0
            )
        )
        .join(Order, OrderItem.order_id == Order.id)
        .filter(
            OrderItem.product_id == Product.id,
            Order.status.in_(['confirmed', 'shipped'])
        )
        .correlate(Product)
        .scalar_subquery()
    )

    # Calculate available quantity
    available_quantity = Product.quantity - sold_quantity

    # Filter by availability
    availability = request.args.get('availability')

    if availability:

        availability = availability.lower()

        if availability == 'in_stock':
            query = query.filter(
                available_quantity > 0
            )

        elif availability == 'out_of_stock':
            query = query.filter(
                available_quantity <= 0
            )

        else:
            return jsonify({
                'error': 'Availability must be in_stock or out_of_stock.'
            }), 400

    # Retrieve matching products
    products = query.distinct().all()

    return jsonify({
        'total': len(products),
        'products': [
            product_to_dict(product)
            for product in products
        ]
    }), 200


# ==============================
# LOOKUP TABLES API
# ==============================

# Available lookup tables
lookup_models = {
    'categories': Category,
    'brands': Brand,
    'genders': Gender,
    'sizes': Size,
    'colors': Color
}


# Convert lookup information into JSON
def lookup_to_dict(item):

    return {
        'id': item.id,
        'name': item.name
    }


# GET - Retrieve all items from a lookup table
# POST - Add a new item
@app.route('/api/lookups/<string:lookup_type>', methods=['GET', 'POST'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def manage_lookups(current_user, lookup_type):

     # Only Admin can add lookup values
    if request.method == 'POST' and current_user.user_role.name != 'admin':
        return jsonify({
            'error': 'Only Admin can manage lookup values'
        }), 403   

    model = lookup_models.get(lookup_type.lower())

    if not model:
        return jsonify({
            'error': 'Invalid lookup table.'
        }), 404

    # GET all items
    if request.method == 'GET':

        items = model.query.order_by(model.id).all()

        return jsonify({
            'total': len(items),
            'items': [
                lookup_to_dict(item)
                for item in items
            ]
        }), 200

    # POST - Add a new item
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    name = data.get('name')

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            'error': 'A valid name is required.'
        }), 400

    name = name.strip()

    existing = model.query.filter(
        db.func.lower(model.name) == name.lower()
    ).first()

    if existing:
        return jsonify({
            'error': 'This item already exists.'
        }), 409

    try:
        item = model(name=name)

        db.session.add(item)
        db.session.commit()

        return jsonify({
            'message': 'Item added successfully!',
            'item': lookup_to_dict(item)
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not add the item.'
        }), 500


# GET - Retrieve one item
# PUT - Update an item
# DELETE - Remove an item
@app.route('/api/lookups/<string:lookup_type>/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
@role_required('admin', 'advanced_user', 'simple_user')
def manage_lookup_item(current_user, lookup_type, item_id):
        # Only Admin can update or delete lookup values
    if request.method in ['PUT', 'DELETE'] and current_user.user_role.name != 'admin':
        return jsonify({
            'error': 'Only Admin can update or delete lookup values'
        }), 403

    model = lookup_models.get(lookup_type.lower())

    if not model:
        return jsonify({
            'error': 'Invalid lookup table.'
        }), 404

    item = db.session.get(model, item_id)

    if not item:
        return jsonify({
            'error': 'Item not found.'
        }), 404

    # GET one item
    if request.method == 'GET':

        return jsonify({
            'item': lookup_to_dict(item)
        }), 200

    # PUT - Update an item
    if request.method == 'PUT':

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                'error': 'Please provide valid JSON data.'
            }), 400

        name = data.get('name')

        if not isinstance(name, str) or not name.strip():
            return jsonify({
                'error': 'A valid name is required.'
            }), 400

        name = name.strip()

        existing = model.query.filter(
            db.func.lower(model.name) == name.lower(),
            model.id != item_id
        ).first()

        if existing:
            return jsonify({
                'error': 'This item already exists.'
            }), 409

        try:
            item.name = name
            db.session.commit()

            return jsonify({
                'message': 'Item updated successfully!',
                'item': lookup_to_dict(item)
            }), 200

        except Exception:
            db.session.rollback()

            return jsonify({
                'error': 'Could not update the item.'
            }), 500

    # DELETE - Remove an item
    if request.method == 'DELETE':

        try:
            db.session.delete(item)
            db.session.commit()

            return jsonify({
                'message': 'Item deleted successfully!'
            }), 200

        except Exception:
            db.session.rollback()

            return jsonify({
                'error': (
                    'Could not delete this item. '
                    'It may be used by existing products.'
                )
            }), 409

# ==============================
# CLIENTS API
# ==============================

# Convert client information into JSON
def client_to_dict(client):

    return {
        'id': client.id,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'email': client.email,
        'phone': client.phone,
        'address': client.address
    }


# GET - Retrieve all clients
@app.route('/api/clients', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user')
def get_clients(current_user):

    clients = Client.query.order_by(Client.id).all()

    return jsonify({
        'total': len(clients),
        'clients': [
            client_to_dict(client)
            for client in clients
        ]
    }), 200


# POST - Add a new client
@app.route('/api/clients', methods=['POST'])
# @token_required
# @role_required('admin')
def add_client():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    required_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'address'
    ]

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({
                'error': f'{field} is required.'
            }), 400

    email = data['email'].strip().lower()

    existing_client = Client.query.filter_by(
        email=email
    ).first()

    if existing_client:
        return jsonify({
            'error': 'A client with this email already exists.'
        }), 409

    try:
        client = Client(
            first_name=data['first_name'].strip(),
            last_name=data['last_name'].strip(),
            email=email,
            phone=data['phone'].strip(),
            address=data['address'].strip()
        )

        db.session.add(client)
        db.session.commit()

        return jsonify({
            'message': 'Client added successfully!',
            'client': client_to_dict(client)
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not add the client.'
        }), 500


# GET - Retrieve one client
@app.route('/api/clients/<int:client_id>', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user')
def get_client(current_user, client_id):

    client = db.session.get(Client, client_id)

    if not client:
        return jsonify({
            'error': 'Client not found.'
        }), 404

    return jsonify({
        'client': client_to_dict(client)
    }), 200


# PUT - Update an existing client
@app.route('/api/clients/<int:client_id>', methods=['PUT'])
@token_required
@role_required('admin')
def update_client(current_user, client_id):

    client = db.session.get(Client, client_id)

    if not client:
        return jsonify({
            'error': 'Client not found.'
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    allowed_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'address'
    ]

    for field in data:
        if field not in allowed_fields:
            return jsonify({
                'error': f'Invalid field: {field}'
            }), 400

        if not isinstance(data[field], str) or not data[field].strip():
            return jsonify({
                'error': f'{field} cannot be empty.'
            }), 400

    if 'email' in data:
        email = data['email'].strip().lower()

        existing_client = Client.query.filter(
            Client.email == email,
            Client.id != client_id
        ).first()

        if existing_client:
            return jsonify({
                'error': 'A client with this email already exists.'
            }), 409

    try:
        for field in data:
            value = data[field].strip()

            if field == 'email':
                value = value.lower()

            setattr(client, field, value)

        db.session.commit()

        return jsonify({
            'message': 'Client updated successfully!',
            'client': client_to_dict(client)
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not update the client.'
        }), 500


# DELETE - Remove a client
@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_client(current_user, client_id):
    client = db.session.get(Client, client_id)

    if not client:
        return jsonify({
            'error': 'Client not found.'
        }), 404

    # Prevent deleting clients who have existing orders
    if Order.query.filter_by(client_id=client_id).first():
        return jsonify({
            'error': 'Cannot delete a client who has existing orders.'
        }), 409

    try:
        db.session.delete(client)
        db.session.commit()

        return jsonify({
            'message': 'Client deleted successfully!'
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            'error': 'Could not delete the client.'
        }), 500

# ==============================
# ORDERS API
# ==============================

# Convert order information into JSON
def order_to_dict(order):

    items = []

    for item in order.items:

        subtotal = Decimal(str(item.price)) * item.quantity

        items.append({
            'product_id': item.product_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.price),
            'subtotal': float(subtotal)
        })

    return {
        'id': order.id,
        'client_id': order.client_id,
        'client_name': (
            order.client.first_name + ' ' +
            order.client.last_name
        ),
        'order_date': order.order_date.isoformat(),
        'status': order.status,
        'total_amount': float(order.total_amount),
        'items': items
    }


# Calculate the current selling price of a product
# Calculate the current selling price of a product
def get_product_selling_price(product):

    price = Decimal(str(product.price))
    now = datetime.now()

    for discount in product.discounts:

        if discount.start_date <= now <= discount.end_date:

            percentage = Decimal(str(discount.percentage))

            price = price * (
                Decimal('100') - percentage
            ) / Decimal('100')

            return price.quantize(Decimal('0.01'))

    return price.quantize(Decimal('0.01'))


# Calculate the quantity sold in confirmed orders
def get_sold_quantity(product_id, exclude_order_id=None):

    query = db.session.query(
        db.func.coalesce(
            db.func.sum(OrderItem.quantity),
            0
        )
    ).join(
        Order,
        OrderItem.order_id == Order.id
    ).filter(
        OrderItem.product_id == product_id,
        Order.status.in_(['confirmed', 'shipped'])
    )

    if exclude_order_id is not None:
        query = query.filter(
            Order.id != exclude_order_id
        )

    return int(query.scalar())


# GET - Retrieve all orders
@app.route('/api/orders', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user')
def get_orders(current_user):

    orders = Order.query.order_by(
        Order.order_date.desc()
    ).all()

    return jsonify({
        'total': len(orders),
        'orders': [
            order_to_dict(order)
            for order in orders
        ]
    }), 200


# POST - Place a new order
@app.route('/api/orders', methods=['POST'])
def create_order():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    client_id = data.get('client_id')
    items_data = data.get('items')

    if (
        isinstance(client_id, bool)
        or not isinstance(client_id, int)
    ):
        return jsonify({
            'error': 'A valid client_id is required.'
        }), 400

    client = db.session.get(Client, client_id)

    if not client:
        return jsonify({
            'error': 'Client not found.'
        }), 404

    if not isinstance(items_data, list) or not items_data:
        return jsonify({
            'error': 'At least one order item is required.'
        }), 400

    # Combine duplicate products into one order item
    quantities = {}

    for item in items_data:

        if not isinstance(item, dict):
            return jsonify({
                'error': 'Each order item must be an object.'
            }), 400

        product_id = item.get('product_id')
        quantity = item.get('quantity')

        if (
            isinstance(product_id, bool)
            or not isinstance(product_id, int)
            or isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity <= 0
        ):
            return jsonify({
                'error': 'Each item needs a valid product_id and positive quantity.'
            }), 400

        quantities[product_id] = (
            quantities.get(product_id, 0) + quantity
        )

    order_items = []
    total_amount = Decimal('0.00')

    # Validate products and calculate order total
    for product_id, quantity in quantities.items():

        product = db.session.get(Product, product_id)

        if not product:
            return jsonify({
                'error': f'Product with ID {product_id} not found.'
            }), 404

        available_quantity = (
            product.quantity -
            get_sold_quantity(product_id)
        )

        if quantity > available_quantity:
            return jsonify({
                'error': (
                    f'Not enough stock for {product.name}. '
                    f'Available quantity: {available_quantity}.'
                )
            }), 400

        price = get_product_selling_price(product)

        subtotal = price * quantity

        total_amount += subtotal

        order_items.append({
            'product': product,
            'quantity': quantity,
            'price': price
        })

    try:

        order = Order(
            client_id=client_id,
            status='pending',
            total_amount=total_amount
        )

        db.session.add(order)
        db.session.flush()

        for item in order_items:

            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )

            db.session.add(order_item)

        db.session.commit()

        return jsonify({
            'message': 'Order created successfully!',
            'order': order_to_dict(order)
        }), 201

    except Exception:

        db.session.rollback()

        return jsonify({
            'error': 'Could not create the order.'
        }), 500


# GET - Retrieve one order by ID
@app.route('/api/orders/<int:order_id>', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user')
def get_order(current_user, order_id):
    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({
            'error': 'Order not found.'
        }), 404

    return jsonify({
        'order': order_to_dict(order)
    }), 200


# PUT - Update order status
@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@token_required
@role_required('admin', 'advanced_user')
def update_order_status(current_user, order_id):

    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({
            'error': 'Order not found.'
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            'error': 'Please provide valid JSON data.'
        }), 400

    new_status = data.get('status')

    allowed_statuses = [
        'pending',
        'confirmed',
        'cancelled',
        'shipped'
    ]

    if (
        not isinstance(new_status, str)
        or new_status.lower() not in allowed_statuses
    ):
        return jsonify({
            'error': (
                'Status must be pending, confirmed,shipped or cancelled.'
            )
        }), 400

    new_status = new_status.lower()

    # Check stock before confirming the order
    if new_status == 'confirmed' and order.status != 'confirmed':

        for item in order.items:

            sold_quantity = get_sold_quantity(
                item.product_id,
                exclude_order_id=order.id
            )

            available_quantity = (
                item.product.quantity - sold_quantity
            )

            if item.quantity > available_quantity:
                return jsonify({
                    'error': (
                        f'Not enough stock for {item.product.name}. '
                        f'Available quantity: {available_quantity}.'
                    )
                }), 400

    try:

        order.status = new_status

        db.session.commit()

        return jsonify({
            'message': 'Order status updated successfully!',
            'order': order_to_dict(order)
        }), 200

    except Exception:

        db.session.rollback()

        return jsonify({
            'error': 'Could not update the order status.'
        }), 500


# DELETE - Delete an order
@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_order(current_user, order_id):

    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({
            'error': 'Order not found.'
        }), 404

    if order.status == 'confirmed':
        return jsonify({
            'error': 'Confirmed orders cannot be deleted.'
        }), 409

    try:

        db.session.delete(order)
        db.session.commit()

        return jsonify({
            'message': 'Order deleted successfully!'
        }), 200

    except Exception:

        db.session.rollback()

        return jsonify({
            'error': 'Could not delete the order.'
        }), 500

# ==============================
# REPORTS API
# ==============================

# GET - Daily earnings report
@app.route('/api/reports/daily-earnings', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user')
def daily_earnings_report(current_user):

    results = db.session.query(
        db.func.date(Order.order_date).label('date'),
        db.func.sum(Order.total_amount).label('earnings'),
        db.func.count(Order.id).label('total_orders')
    ).filter(
        Order.status.in_(['confirmed', 'shipped'])
    ).group_by(
        db.func.date(Order.order_date)
    ).order_by(
        db.func.date(Order.order_date).desc()
    ).all()

    return jsonify({
        'report': 'Daily Earnings',
        'total_days': len(results),
        'earnings': [
            {
                'date': str(row.date),
                'total_earnings': float(row.earnings),
                'total_orders': row.total_orders
            }
            for row in results
        ]
    }), 200


# GET - Monthly earnings report
@app.route('/api/reports/monthly-earnings', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user')
def monthly_earnings_report(current_user):

    results = db.session.query(
        db.func.year(Order.order_date).label('year'),
        db.func.month(Order.order_date).label('month'),
        db.func.sum(Order.total_amount).label('earnings'),
        db.func.count(Order.id).label('total_orders')
    ).filter(
        Order.status.in_(['confirmed', 'shipped'])
    ).group_by(
        db.func.year(Order.order_date),
        db.func.month(Order.order_date)
    ).order_by(
        db.func.year(Order.order_date).desc(),
        db.func.month(Order.order_date).desc()
    ).all()

    return jsonify({
        'report': 'Monthly Earnings',
        'total_months': len(results),
        'earnings': [
            {
                'year': row.year,
                'month': row.month,
                'total_earnings': float(row.earnings),
                'total_orders': row.total_orders
            }
            for row in results
        ]
    }), 200


# GET - Top-selling products report
@app.route('/api/reports/top-products', methods=['GET'])
@token_required
@role_required('admin', 'advanced_user')
def top_products_report(current_user):

    results = db.session.query(
        Product.id,
        Product.name,
        db.func.sum(OrderItem.quantity).label('total_sold'),
        db.func.sum(
            OrderItem.quantity * OrderItem.price
        ).label('total_revenue')
    ).join(
        OrderItem,
        OrderItem.product_id == Product.id
    ).join(
        Order,
        Order.id == OrderItem.order_id
    ).filter(
        Order.status.in_(['confirmed', 'shipped'])
    ).group_by(
        Product.id,
        Product.name
    ).order_by(
        db.func.sum(OrderItem.quantity).desc()
    ).limit(10).all()

    return jsonify({
        'report': 'Top Selling Products',
        'total_products': len(results),
        'products': [
            {
                'product_id': row.id,
                'product_name': row.name,
                'quantity_sold': int(row.total_sold),
                'total_revenue': float(row.total_revenue)
            }
            for row in results
        ]
    }), 200
# ==============================
# DATABASE INITIALIZATION
# ==============================

def initialize_database():

    # Create all database tables
    db.create_all()

    print("Database tables created successfully!")

    # Default roles
    roles = [
        'admin',
        'advanced_user',
        'simple_user'
    ]

    for role_name in roles:
        existing_role = Role.query.filter_by(
            name=role_name
        ).first()

        if not existing_role:
            db.session.add(Role(name=role_name))

    # Default categories
    categories = [
        'Shirts',
        'Pants',
        'Jackets',
        'Dresses',
        'Shoes'
    ]

    for category_name in categories:
        existing_category = Category.query.filter_by(
            name=category_name
        ).first()

        if not existing_category:
            db.session.add(Category(name=category_name))

    # Default brands
    brands = [
        'Nike',
        'Adidas',
        'Zara',
        'Tommy Hilfiger'
    ]

    for brand_name in brands:
        existing_brand = Brand.query.filter_by(
            name=brand_name
        ).first()

        if not existing_brand:
            db.session.add(Brand(name=brand_name))

    # Default genders
    genders = [
        'Men',
        'Women',
        'Children'
    ]

    for gender_name in genders:
        existing_gender = Gender.query.filter_by(
            name=gender_name
        ).first()

        if not existing_gender:
            db.session.add(Gender(name=gender_name))

    # Default sizes
    sizes = [
        'XS',
        'S',
        'M',
        'L',
        'XL',
        'XXL'
    ]

    for size_name in sizes:
        existing_size = Size.query.filter_by(
            name=size_name
        ).first()

        if not existing_size:
            db.session.add(Size(name=size_name))

    # Default colors
    colors = [
        'Black',
        'White',
        'Red',
        'Blue',
        'Green'
    ]

    for color_name in colors:
        existing_color = Color.query.filter_by(
            name=color_name
        ).first()

        if not existing_color:
            db.session.add(Color(name=color_name))

       # Save everything in the database
    db.session.commit()

    print("Default data inserted successfully!")

    # Create initial users
    admin_role = Role.query.filter_by(name='admin').first()
    advanced_role = Role.query.filter_by(name='advanced_user').first()

    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            role_id=admin_role.id
        )

        db.session.add(admin_user)

    if not User.query.filter_by(username='advanced').first():
        advanced_user = User(
            username='advanced',
            email='advanced@example.com',
            password=generate_password_hash('advanced123'),
            role_id=advanced_role.id
        )

        db.session.add(advanced_user)

    db.session.commit()

    print("Initial users created successfully!")
# ==============================
# RUN APPLICATION
# ==============================

if __name__ == '__main__':

    with app.app_context():
        initialize_database()

    app.run(debug=True)