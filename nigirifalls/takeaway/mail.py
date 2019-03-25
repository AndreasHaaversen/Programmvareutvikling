from django.template.loader import render_to_string
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint


def send_order_email_with_pdf(order, message):
    # Create order email
    subject = 'Nigiri Falls - Order no. {}'.format(order.id)
    email = EmailMessage(subject,
                         message,
                         'nigirifalls@gmail.com',
                         [order.email])
    # Generate PDF
    html = render_to_string('takeaway/order/order_pdf.html',
                            {'order': order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(
        out, stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + '/takeaway/pdf_style.css'
            )]
        )

    # Attach email
    email.attach('order_{}.pdf'.format(order.id),
                 out.getvalue(),
                 'application/pdf')
    # Send email
    email.send()


def send_email(order, message):
    # Create order confirmation email
    subject = 'Nigiri Falls - Order no. {}'.format(order.id)
    email = EmailMessage(subject,
                         message,
                         'nigirifalls@gmail.com',
                         [order.email])

    # Send email
    email.send()