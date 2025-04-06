from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = TextAreaField('Address', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    pincode = StringField('PIN Code', validators=[Optional(), Length(min=6, max=10)])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (₹)', validators=[DataRequired(), NumberRange(min=0)])
    discount_price = FloatField('Discount Price (₹)', validators=[Optional(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', validators=[DataRequired()], 
                           choices=[
                               ('clothing', 'Clothing'),
                               ('handicrafts', 'Handicrafts'),
                               ('spices', 'Spices'),
                               ('jewelry', 'Jewelry'),
                               ('home_decor', 'Home Decor'),
                               ('food_products', 'Food Products'),
                               ('beauty', 'Beauty & Wellness'),
                               ('accessories', 'Accessories'),
                               ('books', 'Books'),
                               ('electronics', 'Electronics')
                           ])
    image_url1 = StringField('Main Image URL', validators=[DataRequired()])
    image_url2 = StringField('Additional Image URL', validators=[Optional()])
    image_url3 = StringField('Additional Image URL', validators=[Optional()])
    is_featured = BooleanField('Featured Product')
    is_gi_tagged = BooleanField('GI Tagged Product')
    gi_tag_details = TextAreaField('GI Tag Details', validators=[Optional()])
    origin = StringField('Origin/Region', validators=[Optional(), Length(max=64)])
    submit = SubmitField('Save Product')

class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField('Shipping Address', validators=[DataRequired()])
    shipping_city = StringField('City', validators=[DataRequired()])
    shipping_state = StringField('State', validators=[DataRequired()])
    shipping_pincode = StringField('PIN Code', validators=[DataRequired(), Length(min=6, max=10)])
    payment_method = SelectField('Payment Method', choices=[('cod', 'Cash On Delivery')], validators=[DataRequired()])
    submit = SubmitField('Place Order')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        ('5', '★★★★★ Excellent'),
        ('4', '★★★★☆ Good'),
        ('3', '★★★☆☆ Average'),
        ('2', '★★☆☆☆ Poor'),
        ('1', '★☆☆☆☆ Very Poor')
    ], validators=[DataRequired()])
    title = StringField('Review Title', validators=[Optional(), Length(max=128)])
    comment = TextAreaField('Your Review', validators=[Optional(), Length(min=10, max=1000)])
    submit = SubmitField('Submit Review')
