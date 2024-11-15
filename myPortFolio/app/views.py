import asyncio
import json

import django.shortcuts
from aiosmtplib import SMTP
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import date

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from . import models
from .models import Skill, User, Framework, Resume, Education, Message, Experience


# Create your views here.

def main(request):
    user = User.objects.get(id=1)
    skills = Skill.objects.filter(Q(user=1)).values()
    user.set_skills(skills)
    skills = user.get_skills()
    n_skills = user.get_n_skill()
    half = n_skills // 2
    column1 = [skills[sk] for sk in range(0, half)]
    column2 = [skills[sk] for sk in range(half, n_skills)]

    resume = Resume.objects.get(id=1)
    educations = Education.objects.filter(Q(id=1)).values()
    frameworks = Framework.objects.all()
    experiences = Experience.objects.all()
    start_year = date.fromisoformat(str(educations[0]['start_year'])).year
    end_year = date.fromisoformat(str(educations[0]['end_year'])).year
    context = {
        'name': user.name,
        'lastname': user.lastname,
        'degree': user.degree,
        'email': user.email,
        'city': user.address,
        'phone': user.phone,
        'website': None,
        'title': user.title,
        'about': user.about,
        'sub_section': user.title_description,
        'end_section': user.title_description_1,
        'skills': user.get_skills(),
        'column1': column1,
        'column2': column2,
        'frameworks': frameworks,
        'resume': resume,
        'educations': educations,
        'experiences': experiences,
        'present': models.MY_CHOICES2[0][1]
    }

    return render(request, "app/main.html", context)


async def sendEmail(name_, email_, subject_, message_):
    # Extract values
    name = name_
    email = email_
    subject = subject_
    message = message_

    # Render HTML template with dynamic values
    html_message = render_to_string('app/email_template.html', {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })

    # Create plain text version of the email
    text_content = strip_tags(html_message)

    # Set up email parameters
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["ralphdumera00@gmail.com"]

    # Create the email message
    msg = f"Subject: New message from your PORT-FOLIO - {subject}\n" \
          f"From: {email_from}\n" \
          f"To: {', '.join(recipient_list)}\n" \
          f"MIME-Version: 1.0\n" \
          f"Content-Type: text/html; charset=\"utf-8\"\n\n" \
          f"{html_message}"

    # Send email asynchronously
    async with SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT, use_tls=settings.EMAIL_USE_TLS) as smtp:
        await smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        await smtp.sendmail(email_from, recipient_list, msg)


def contact(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extracting data from JSON
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')

            # Save the message to the database
            # Message.objects.create(
            #     idUser=1,
            #     name=name,
            #     email=email,
            #     subject=subject,
            #     message=message
            # )
            print([name, email, subject, message])
            print("before sent")
            # Run the sendEmail function asynchronously
            asyncio.run(sendEmail(name, email, subject, message))
            print("after sent")
            return JsonResponse({"result": "ok"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
