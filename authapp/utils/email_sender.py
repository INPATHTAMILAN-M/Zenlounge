from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_email(subject, to_email, template_name, context):
    print("sending_email......")
    try:
        html_content = render_to_string(template_name, context=context)
        plain_text_content = strip_tags(html_content)  # Convert HTML to plain text

        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text_content,  # Plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")  # Attach HTML version
        email.send()

        return True
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        return False
    
