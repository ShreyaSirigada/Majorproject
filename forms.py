from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField,SelectField,FileField

from wtforms.validators import DataRequired

class LoginForm(Form):

    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])

    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])


class RegisterForm(Form):
    
    name = StringField("ID", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])
    
    username = StringField("Username", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])
    
    email = StringField("Email", validators=[validators.Email(message="Please enter a valid email address")])
    
    password = PasswordField("Password", validators=[
    
        validators.DataRequired(message="Please Fill This Field"),
    
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])
    
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])

class AdminLoginForm(Form):

    username = StringField("UserName", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])

    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])

class AddBrandForm(Form):
    myChoices = ["Apple","OnePlus","SamSung","Motorola","Realme","Redmi"]
    mobile_brand = SelectField(u'Brand', choices = myChoices, validators=[validators.DataRequired(message="Please Choose fill this Field")])
    
    model_name = StringField("Model Name", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])

    front_c = StringField("Front Camera", validators=[validators.Length(min=2, max=25), validators.DataRequired(message="Please Fill This Field")])
    rear_c = StringField("Rear Camera", validators=[validators.Length(min=2, max=25), validators.DataRequired(message="Please Fill This Field")])

    hdd_choices = ["16 GB","32 GB","64 GB","128 GB","512 GB","1 TB"]
    hdd = SelectField(u'HDD', choices = hdd_choices, validators=[validators.DataRequired(message="Please Choose from this Field")])

    ram_choices = ["2 GB","3 GB","4 GB","6 GB","8 GB","16 GB","32 GB","64 GB"]
    ram = SelectField(u'RAM', choices = ram_choices, validators=[validators.DataRequired(message="Please Choose from this Field")])

    processor_choices = ["A15 Bionic | Apple","Dimensity 9000 | MediaTek ","Snapdragon 8 Gen 1 | Qualcomm "]
    processor = SelectField(u'Processor', choices = processor_choices, validators=[validators.DataRequired(message="Please Choose from this Field")])

    front_image = FileField(u'Image1')

    rear_image = FileField(u'Image2')

    