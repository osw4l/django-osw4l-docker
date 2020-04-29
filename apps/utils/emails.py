from django.template import loader
from django.conf import settings
from sendgrid import Mail, SendGridAPIClient, Content
from apps.utils.print_colors import _green, _red


def send(**kwargs):
    print('sending message')
    print(_green(kwargs))
    result = True
    body = Content("text/html", loader.render_to_string(
        kwargs.get('email_template'),
        kwargs.get('context')
    ))
    try:
        message = Mail(
            from_email=settings.SENGRID_SENDER_EMAIL,
            to_emails=kwargs.get('to_email'),
            subject=kwargs.get('subject'),
            html_content=body
        )
        sengrid_email = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        email_request = sengrid_email.send(message)
        print(_green('----------- sendgrid email response -----------'))
        print(email_request.status_code)
        print(email_request.body)
        print(email_request.headers)
        print(_green('----------- sendgrid email response -----------'))
    except Exception as e:
        result = False
        if not settings.DEBUG:
            slack_messages.run(
                msg='Error sending email to {} : Error: {}'.format(kwargs.get('to_email'), str(e)),
                channel_id=settings.SLACK_BUGS_CHANNEL_ID
            )
        print(_red('Error sending email caused by : {}'.format(str(e))))
    return result
