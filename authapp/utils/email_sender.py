from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, to_email, template_name, context):
    
    html_content = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,  # Replace with your email
        to=[to_email],
    )
    email.content_subtype = "html"  # Ensure it's sent as HTML
    email.send()

    return  True
    
