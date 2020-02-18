from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Farmer

def sendEmailVarificationFarmer(to, user_id , token, type_of ,to):
    " this will send interface token validation"
    html_message = render_to_string(
        "email_font\emailVarification.html", 
        {
            "token": token,
            "user_id":user_id,
            "type":type_of,
        }
    )

    subject = "Email Varification Of Farmer Account"
    from_email = "sup.testkumar678@gmail.com"
    to = to

    text_content = "Please Click the Conformation button given in below"

    msg = (
            subject,
            text_content,
            from_email,
            [to],
    )
    msg.attach_alternative(html_message)
    msg.send()
