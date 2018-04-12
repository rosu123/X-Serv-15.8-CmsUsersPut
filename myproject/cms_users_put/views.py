from django.shortcuts import render
from cms_users_put.models import Pages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from sqlite3 import OperationalError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.

def mylogout(request):
    logout(request)
    return redirect(view_info)

def get_absolute_url(self):

    if not (self.startswith("http://") or self.startswith("https://")):
        self = "http://" + self
    return self

def content(request, identificador):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)
    try:
        pag = Pages.objects.get(id = int(identificador))
        print(pag.page)
        return HttpResponse(pag.page)
    except ObjectDoesNotExist:
        return HttpResponse("Content not found", status=404)


def form():
    resp = "<html><body><h1>DB info:</h1>"
    resp += "<form action='/cms/'' method='post'>"
    resp += "Site:<br> <input type='text' name = 'site' value='Google' required><br>"
    resp += "URL:<br> <input type='text' name = 'url' value='www.google.es' required><br>"
    resp += "<input type='submit' value='Submit'></form></body>"
    return(resp)

@csrf_exempt
def view_info(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            resp = '<li><a href="/logout">Logout</a></li>'
        else:
            resp = '<li><a href="/login">Login</a></li>'
        resp += form()
        try:
            list_urls = Pages.objects.all()
            resp += "<p>Saved URLs:</p>"
            resp += "<ol>"
            #print(resp)
            for pag in list_urls:
                resp += '<li><a href="/cms/' + str(pag.id) + '">' + pag.name + "  (" + pag.page + ')</a></li>'
            resp += "</ol>"
            return HttpResponse(resp)
        except OperationalError:
            return HttpResponse("No content", status=404)

    if request.method == "POST" or request.method == "PUT":
        if request.user.is_authenticated():
            name = request.POST['site']
            page = request.POST['url']
            #print("NAME: |" + name + "|    URL: |" + url + "|")
            url = get_absolute_url(page)
            try:
                pag = Pages.objects.get(page = url)
                resp = "It already exist: "
            except ObjectDoesNotExist:
                pag = Pages(name = name, page = url)
                #pag.name = newUrl
                #pag.page = url
                pag.save()
                resp = "URL: "
            resp += "<a href=" + pag.page + ">" + pag.page + "</a>"
            resp += "</br>Shortened: <a href=/cms/" + str(pag.id) + ">" + str(pag.id) + "</a> "
            resp += "</br><a href=/cms/>Back</a> "
        else:
            resp = "You cannot modify the DB if you are not logged: "
            resp += '<a href="/login">Login</a>'
        return HttpResponse(resp)

def msg_error(request, msg):
    return HttpResponse(msg + ": content not found", status=404)

def show_content(request):
    if request.user.is_authenticated():
        logged = 'Logged in as ' + request.user.username
    else:
        logged = 'Not logged in.'
    return HttpResponse(logged)
