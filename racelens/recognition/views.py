from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings

from .forms import UploadForm, UploadSelfie, CreateEvent, ContactForm
from .models import Photo, Selfie, Event

import boto3
from slugify import slugify

rekognition = boto3.client("rekognition")

# Check if user is staff
def is_member(user):
    return user.groups.filter(name='staff').exists()

def error_404(request, exception):
    return render(request, 'errors.html', {'error': 'La pagina que buscabas no existe.'})

def error_500(request):
    return render(request, 'errors.html', {'error': 'Ocurrio un problema, intentalo mas tarde.'})


def index(request):
    return render(request, "index.html")


@login_required
@user_passes_test(is_member, login_url="/eventos/", redirect_field_name=None)
def uploadPhoto(request, slug):
    """ /upload """
    event = get_object_or_404(Event, slug=slug)
    if request.method == "POST":
        print(request.FILES)
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("form valid")
            instance = form.save(commit=False)
            instance.user = request.user
            instance.event = event
            instance.save()
            # print(instance.id)

            sleep(.5)

            db_object = Photo.objects.get(pk=instance.id)

            img_url = db_object.image.url
            result = rekognition.index_faces(
                CollectionId=slug,
                Image={
                    "S3Object": {
                        "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                        "Name": img_url.split("?")[0].split(".com/")[
                            1
                        ],  # TODO refactor this function
                    }
                },
            )

            try:
                db_object.imageId = result["FaceRecords"][0]["Face"]["ImageId"]
            except:
                #No faces recognized in the image
                return HttpResponse("No faces were recongizen in this picture")
            else:
                db_object.save()

                return HttpResponse("This picture ID is " + db_object.imageId)
        
        else:
            print("form not valid")

    else:
        form = UploadForm(request.user)

    return render(request, "recognition/upload.html", {"form": form})



@login_required
def uploadSelfie(request, slug):
    """ /selfie """
    event = get_object_or_404(Event,slug=slug)
    if request.method == "POST":
        form = UploadSelfie(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            selfie_image = instance.image.url.split("?")[0].split(".com/")[1]

            result = rekognition.search_faces_by_image(
                CollectionId=slug,
                Image={"S3Object": {"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Name": selfie_image}},
            )
            
            images = []

            for i in result['FaceMatches']:
                images.append(i['Face']['ImageId'])

            response = []

            for image in images:
                curr_image = Photo.objects.get(imageId=image)
                instance.photos.add(curr_image)
                response.append(curr_image.image.url)
            
            return JsonResponse(response, safe=False)
    

    else:
        form = UploadSelfie()

    return render(request, "recognition/selfie.html", {"form": form, "event": event})


@login_required
@user_passes_test(is_member, login_url="/eventos/", redirect_field_name=None)
def create_event(request):
    """ /event """
    if request.method == "POST":
        form = CreateEvent(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.slug = slugify(event.event_name)
            event.save()

            rekognition.create_collection(CollectionId=event.slug)

            return HttpResponseRedirect(reverse('recognition:get_event', args=[event.slug]))

    else:
        form = CreateEvent()

    return render(request, "recognition/create_event.html", {"form": form})


def get_event(request, slug):
    event = get_object_or_404(Event,slug=slug)
    return render(request, 'add_event.html', {'event': event})

def list_events(request):
    return render(request, 'recognition/events_list.html', {'events': Event.objects.all()})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("mail")
            subject = name + " envio un mensaje: " + form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")

            new_message = "Nombre: " + name + "\n"
            new_message += "Correo: " + email + "\n"
            new_message += "Asunto: " + form.cleaned_data.get("subject") + "\n"
            new_message += "Mensaje: \n" + message

            send_mail(subject, new_message, email, ['racelens.io@gmail.com'])

            return HttpResponse("Message sent")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def politica_de_privacidad(request):
    return render(request, 'politica-de-privacidad.html')