from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_fine_notification(user, borrow):
    subject = 'Overdue Book Notification'
    message = render_to_string('library/overdue_notification_email.html', {
        'user': user,
        'book': borrow.book,
        'fine': borrow.fine,
        'due_date': borrow.due_date,
    })
    send_mail(subject, message, 'your-email@example.com', [user.email])