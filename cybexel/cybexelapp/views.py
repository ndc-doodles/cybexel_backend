from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_protect
from .models import Statistic
from django.http import JsonResponse
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.utils.timezone import now
from datetime import timedelta
from dateutil.parser import parse as parse_datetime 





def index(request):
    logos = ClientLogo.objects.all()
    return render(request, 'index.html', {'logos': logos})

def about(request):
    stats = Statistic.objects.all()
    return render(request, 'about.html', {'stats': stats})


def blog(request):
    blogs = Blog.objects.all().order_by('-date')
    paginator = Paginator(blogs, 6) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {'page_obj': page_obj})

def careers(request):
    dept_filter = request.GET.get('department', 'all')
    exp_filter = request.GET.get('experience', 'all')

    departments = Department.objects.all()
    experiences = Experience.objects.all()
    jobs = JobVacancy.objects.all()

    if dept_filter != 'all':
        jobs = jobs.filter(department__name=dept_filter)

    if exp_filter != 'all':
        jobs = jobs.filter(experience__name=exp_filter)


    show_success_modal = request.session.pop('show_success_modal', False)

    context = {
        'departments': departments,
        'experiences': experiences,
        'jobs': jobs,
        'selected_dept': dept_filter,
        'selected_exp': exp_filter,
        'show_success_modal': show_success_modal,  
    }
    return render(request, 'careers.html', context)
ALLOWED_DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com']
def contact(request):
    context = {
        'form_errors': {}
    }

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        form_errors = {}

        if not name:
            form_errors['name'] = "Name is required."
        elif not re.match(r'^[A-Za-z ]+$', name):
            form_errors['name'] = "Name must not contain numbers or special characters."
        elif len(name) > 100:
            form_errors['name'] = "Name is too long (max 100 characters)."



        if not email:
          form_errors['email'] = "Email is required."
        else:
            try:
              validate_email(email)
            except ValidationError:
              form_errors['email'] = "Please enter a valid email address."
    
   
        domain = email.split('@')[-1].lower()
        if domain not in ALLOWED_DOMAINS:
           form_errors['email'] = "Please use a valid common email provider like Gmail or Outlook."

        if len(email) > 100:
            form_errors['email'] = "Email is too long (max 100 characters)."

 
            if not subject:
               form_errors['subject'] = "Subject is required."
            elif not re.match(r'^[A-Za-z ]+$', subject):
               form_errors['subject'] = "Subject must contain only letters and spaces."
            elif len(subject) > 100:
               form_errors['subject'] = "Subject is too long (max 100 characters)."
            elif contains_url(subject):  
               form_errors['subject'] = "Subject cannot contain URLs or links."


        if not message:
            form_errors['message'] = "Message is required."
        elif not re.match(r'^[A-Za-z0-9\s.,\n\r]+$', message):
            form_errors['message'] = "Message can only include letters, numbers, spaces, commas, and periods."
 

        elif len(message) > 2000:
            form_errors['message'] = "Message is too long (max 2000 characters)."

        if form_errors:
            context['form_errors'] = form_errors
            context['form_data'] = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
            }
            return render(request, 'contact.html', context)


        ContactSubmission.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        email_subject = f"New Contact Form Submission: {subject}"
        email_message = f"""
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        """

        email_obj = EmailMessage(
            subject=email_subject,
            body=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['info@cybexel.com'],
            reply_to=[email]
        )
        email_obj.send(fail_silently=False)

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, 'contact.html', context)

def services(request):
    return render(request,'services.html')


def cybexel_life(request):
    entries = LifeEvent.objects.prefetch_related('images').all()
    return render(request, 'cybexelife.html', {'entries': entries})



def detail(request, pk):
    event = get_object_or_404(LifeEvent, pk=pk)
    return render(request, 'detail.html', {'event': event})







ALLOWED_EXTENSIONS = ['pdf']
MAX_RESUME_SIZE = 5 * 1024 * 1024

URL_PATTERN = re.compile(
    r'(https?://|www\.)|(\.com|\.net|\.org|\.in|\.co)'
)



def contains_url(text):
    return bool(URL_PATTERN.search(text))


def submit_job_application(request):
    if request.method == 'POST':
        department_name = request.POST.get('department', '').strip()
        position = request.POST.get('position', '').strip()
        label = request.POST.get('label', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        cover_letter = request.POST.get('cover_letter', '').strip()
        resume = request.FILES.get('resume')

      
        if not all([department_name, position, label, name, email]):
            messages.error(request, "Please fill in all the required fields.")
            return redirect('careers')


        try:
            department = Department.objects.get(name=department_name)
        except Department.DoesNotExist:
            messages.error(request, "Selected department is invalid.")
            return redirect('careers')

        NAME_PATTERN = re.compile(r'^[A-Za-z ]+$')  

        if not NAME_PATTERN.match(name):
           messages.error(request, "Name must contain only letters and spaces (no numbers or special characters).")
           return redirect('careers')



        for field_value in [name, label, position]:
            if contains_url(field_value):
                messages.error(request, "No links or URLs are allowed in the form.")
                return redirect('careers')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect('careers')

        if resume:
            if not resume.name.lower().endswith('.pdf'):
                messages.error(request, "Only PDF files are allowed.")
                return redirect('careers')

            if resume.content_type != 'application/pdf':
                messages.error(request, "Invalid file type. Upload a PDF.")
                return redirect('careers')

            if resume.size > MAX_RESUME_SIZE:
                messages.error(request, "Resume file size should not exceed 5MB.")
                return redirect('careers')

        if cover_letter:
            if len(cover_letter) > 3000:
                messages.error(request, "Cover letter is too long (max 3000 characters).")
                return redirect('careers')
            if contains_url(cover_letter):
                messages.error(request, "Cover letter must not contain any URLs or links.")
                return redirect('careers')

        JobApplication.objects.create(
            department=department,
            position=position,
            label=label,
            name=name,
            email=email,
            cover_letter=cover_letter,
            resume=resume
        )

        admin_subject = f"New Job Application: {position} - {label}"
        admin_body = f"""
        A new job application was submitted.

        Name: {name}
        Email: {email}
        Department: {department.name}
        Position: {position}
        Label: {label}
        Cover Letter: {cover_letter}
        """

        admin_email = EmailMessage(
            subject=admin_subject,
            body=admin_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['info@cybexel.com'],
            reply_to=[email]
        )

        if resume:
            resume.seek(0)
            admin_email.attach(resume.name, resume.read(), resume.content_type)

        admin_email.send(fail_silently=False)

        html_message = render_to_string("job_confirmation.html", {
            "name": name,
            "position": position
        })

        confirmation_email = EmailMessage(
            subject="Thank You for Your Application",
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        confirmation_email.content_subtype = "html"
        confirmation_email.send(fail_silently=False)

        request.session['show_success_modal'] = True
        return redirect('careers')
    
# def admin_register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '').strip()
#         email = request.POST.get('email', '').strip()
#         password1 = request.POST.get('password1', '')
#         password2 = request.POST.get('password2', '')

#         form_errors = {}
#         form_data = {
#             'username': username,
#             'email': email
#         }

#         # Field required check
#         if not username:
#             form_errors['username'] = "Username is required."
#         elif not re.match(r'^[A-Za-z0-9_]+$', username):
#             form_errors['username'] = "Username must not contain spaces or special characters."
#         elif len(username) > 30:
#             form_errors['username'] = "Username must be under 30 characters."
#         elif User.objects.filter(username=username).exists():
#             form_errors['username'] = "Username already exists."

#         if not email:
#             form_errors['email'] = "Email is required."
#         else:
#             try:
#                 validate_email(email)
#             except ValidationError:
#                 form_errors['email'] = "Invalid email address."
#             if User.objects.filter(email=email).exists():
#                 form_errors['email'] = "Email already registered."

#         if not password1:
#             form_errors['password1'] = "Password is required."
#         elif len(password1) < 8:
#             form_errors['password1'] = "Password must be at least 8 characters long."
#         elif not re.search(r'[A-Za-z]', password1) or not re.search(r'[0-9]', password1):
#             form_errors['password1'] = "Password must include letters and numbers."

#         if not password2:
#             form_errors['password2'] = "Please confirm your password."
#         elif password1 != password2:
#             form_errors['password2'] = "Passwords do not match."

#         if form_errors:
#             return render(request, 'admin_register.html', {
#                 'form_errors': form_errors,
#                 'form_data': form_data
#             })
#         # Create user
#         user = User.objects.create_user(username=username, email=email, password=password1)
#         user.is_staff = True
#         user.save()

#         return redirect('admin_login')

#     return render(request, 'admin_register.html')



MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME = timedelta(minutes=5)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        attempts = request.session.get('login_attempts', 0)
        lockout_until_str = request.session.get('lockout_until')

        if lockout_until_str:
            try:
                lockout_until = parse_datetime(lockout_until_str)
                if now() < lockout_until:
                    remaining = (lockout_until - now()).seconds // 60 + 1
                    messages.error(request, f"⛔ Too many failed login attempts. Try again in {remaining} minute(s).")
                    return redirect('admin_login')
                else:
                    request.session['login_attempts'] = 0
                    request.session['lockout_until'] = None
            except Exception:
                request.session['login_attempts'] = 0
                request.session['lockout_until'] = None

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            request.session['login_attempts'] = 0
            request.session['lockout_until'] = None
            return redirect('admin_dashboard')
        else:
            attempts += 1
            request.session['login_attempts'] = attempts

            if attempts >= MAX_LOGIN_ATTEMPTS:
                lockout_until = now() + LOCKOUT_TIME
                request.session['lockout_until'] = lockout_until.isoformat()
                messages.error(request, f"🚫 Account locked. Too many failed attempts. Try again in {LOCKOUT_TIME.seconds // 60} minutes.")
            else:
                remaining = MAX_LOGIN_ATTEMPTS - attempts
                messages.error(request, f"❌ Invalid username or password. {remaining} attempt(s) remaining.")

            return redirect('admin_login')

    return render(request, 'admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='admin_login')  
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('admin_login')

    stats = Statistic.objects.all()
    logos = ClientLogo.objects.all()

    if request.method == "POST":
        alt_text = request.POST.get("alt_text", "")
        images = request.FILES.getlist("images")  

        for image in images:
            ClientLogo.objects.create(image=image, alt_text=alt_text)

        return redirect("admin_dashboard")

    return render(request, "admin_dashboard.html", {"stats": stats, "logos": logos})


def delete_client_logo(request, id):
    logo = get_object_or_404(ClientLogo, id=id)
    logo.delete()
    return redirect('admin_dashboard')

def update_stat(request):
    if request.method == 'POST':
        stat_id = request.POST.get('id')
        new_count = request.POST.get('count')
        try:
            stat = Statistic.objects.get(id=stat_id)
            stat.count = new_count
            stat.save()
            return JsonResponse({'status': 'success', 'new_count': stat.count})
        except Statistic.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Statistic not found'})
    return HttpResponseBadRequest("Invalid request")

def add_stat(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        count = request.POST.get('count')
        Statistic.objects.create(title=title, count=count)
        return redirect('admin_dashboard')
    
def admin_contact(request):
    contacts = ContactSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'admin_contact.html', {'contacts': contacts})

@csrf_protect
def bulk_delete_contacts(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            ContactSubmission.objects.filter(id__in=selected_ids).delete()
    return redirect('admin_contact')



def admin_blog(request):
    if request.method == "POST":
        blog_id = request.POST.get("edit_id")
        if blog_id:
            blog = Blog.objects.get(id=blog_id)
        else:
            blog = Blog()

        blog.keyword = request.POST.get("keyword")
        blog.date = request.POST.get("date")
        blog.short_heading = request.POST.get("short_heading")
        blog.full_heading = request.POST.get("full_heading")
        blog.paragraph1 = request.POST.get("paragraph1")
        blog.paragraph2 = request.POST.get("paragraph2")
        blog.paragraph3 = request.POST.get("paragraph3")
        blog.paragraph4 = request.POST.get("paragraph4")

        if request.FILES.get("image"):
            blog.image = request.FILES.get("image")

        blog.save()
        return redirect("admin_blog")

    blogs = Blog.objects.all().order_by("-date")
    return render(request, "admin_blog.html", {"blogs": blogs})


def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    return redirect("admin_blog")

def get_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        data = {
            'id': blog.id,
            'keyword': blog.keyword,
            'date': blog.date.strftime('%Y-%m-%d'),
            'short_heading': blog.short_heading,
            'full_heading': blog.full_heading,
            'paragraph1': blog.paragraph1,
            'paragraph2': blog.paragraph2,
            'paragraph3': blog.paragraph3,
            'paragraph4': blog.paragraph4,
        }
        return JsonResponse(data)
    except Blog.DoesNotExist:
        return JsonResponse({'error': 'Blog not found'}, status=404)
def update_blog(request):
    if request.method == "POST":
        blog_id = request.POST.get("id")
        blog = get_object_or_404(Blog, id=blog_id)
        blog.keyword = request.POST.get("keyword")
        blog.date = request.POST.get("date")
        blog.short_heading = request.POST.get("short_heading")
        blog.full_heading = request.POST.get("full_heading")
        blog.paragraph1 = request.POST.get("paragraph1")
        blog.paragraph2 = request.POST.get("paragraph2")
        blog.paragraph3 = request.POST.get("paragraph3")
        blog.paragraph4 = request.POST.get("paragraph4")
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        return redirect('admin_blog')

def admin_careers(request):
    edit_department = None
    edit_experience = None
    edit_job = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")

   
        if form_type == "add_department":
            name = request.POST.get("department_name")
            if name:
                Department.objects.create(name=name)

        elif form_type == "edit_department":
            department_id = request.POST.get("department_id")
            department = get_object_or_404(Department, pk=department_id)
            department.name = request.POST.get("department_name")
            department.save()


        elif form_type == "add_experience":
            name = request.POST.get("experience_name")
            duration = request.POST.get("experience_duration")
            if name and duration:
                Experience.objects.create(name=name, duration=duration)

        elif form_type == "edit_experience":
            experience_id = request.POST.get("experience_id")
            experience = get_object_or_404(Experience, pk=experience_id)
            experience.name = request.POST.get("experience_name")
            experience.duration = request.POST.get("experience_duration")
            experience.save()


        elif form_type == "add_job":
            post_name = request.POST.get("post_name")
            department_id = request.POST.get("department_id")
            experience_id = request.POST.get("experience_id")
            job_description = request.POST.get("job_description")
            skills = request.POST.getlist("skills[]")
            department = get_object_or_404(Department, pk=department_id)
            experience = get_object_or_404(Experience, pk=experience_id)
            JobVacancy.objects.create(
                post_name=post_name,
                department=department,
                experience=experience,
                job_description=job_description,
                required_skills=",".join(skills)
            )

        elif form_type == "edit_job":
            job_id = request.POST.get("job_id")
            job = get_object_or_404(JobVacancy, pk=job_id)
            job.post_name = request.POST.get("post_name")
            job.department = get_object_or_404(Department, pk=request.POST.get("department_id"))
            job.experience = get_object_or_404(Experience, pk=request.POST.get("experience_id"))
            job.job_description = request.POST.get("job_description")
            job.required_skills = ",".join(request.POST.getlist("skills[]"))
            job.save()

        return redirect("admin_careers")


    edit_type = request.GET.get("edit_type")
    edit_id = request.GET.get("id")

    if edit_type == "department":
        edit_department = get_object_or_404(Department, pk=edit_id)
    elif edit_type == "experience":
        edit_experience = get_object_or_404(Experience, pk=edit_id)
    elif edit_type == "job":
        edit_job = get_object_or_404(JobVacancy, pk=edit_id)
    

        if edit_job.required_skills:
            skills_list = edit_job.required_skills.split(",")
        else:
            skills_list = []
    else:
        skills_list = []


    context = {
    "departments": Department.objects.all(),
    "experiences": Experience.objects.all(),
    "jobs": JobVacancy.objects.all(),
    "edit_department": edit_department,
    "edit_experience": edit_experience,
    "edit_job": edit_job,
    "skills_list": skills_list,
}

    return render(request, "admin_careers.html", context)


def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect("admin_careers")


def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    experience.delete()
    return redirect("admin_careers")


def delete_job(request, pk):
    job = get_object_or_404(JobVacancy, pk=pk)
    job.delete()
    return redirect("admin_careers")
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        department.name = request.POST.get("department_name")
        department.save()
        return redirect("admin_careers")

    context = {
        "departments": Department.objects.all(),
        "experiences": Experience.objects.all(),
        "jobs": JobVacancy.objects.all(),
        "edit_department": department,
    }
    return render(request, "admin_careers.html", context)



def edit_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == "POST":
        experience.name = request.POST.get("experience_name")
        experience.duration = request.POST.get("duration")
        experience.save()
        return redirect("admin_careers")
    return render(request, "admin_careers.html", {"experience": experience})


def edit_job(request, pk):
    job = get_object_or_404(JobVacancy, pk=pk)
    departments = Department.objects.all()
    experiences = Experience.objects.all()

    if request.method == "POST":
        job.post_name = request.POST.get("post_name")
        job.department = get_object_or_404(Department, id=request.POST.get("department_id"))
        job.experience = get_object_or_404(Experience, id=request.POST.get("experience_id"))
        job.job_description = request.POST.get("job_description")
        job.required_skills = ",".join(request.POST.getlist("skills[]"))
        job.save()
        return redirect("admin_careers")

    return render(request, "admin_careers.html", {
        "job": job,
        "departments": departments,
        "experiences": experiences
    })

def admin_job_applications(request):
    applications = JobApplication.objects.all().order_by('-submitted_at')  # or .created_at if you're using that field
    return render(request, 'admin_job_applications.html', {'applications': applications})



@csrf_protect
def bulk_delete_job_applications(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            JobApplication.objects.filter(id__in=selected_ids).delete()
    return redirect('admin_job_applications')



def delete_job_application(request, id):
    if request.method == 'POST':
        app = get_object_or_404(JobApplication, pk=id)
        app.delete()
        messages.success(request, "Application deleted successfully.")
    return redirect('admin_job_applications')



def admin_cybexelife(request):
    if request.method == 'POST':
        event_id = request.POST.get('edit_id')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        para1 = request.POST.get('paragraph1')
        para2 = request.POST.get('paragraph2')
        para3 = request.POST.get('paragraph3')
        category = request.POST.get('keyword')

        if event_id:  # ✅ Edit existing
            event = get_object_or_404(LifeEvent, id=event_id)
            event.heading = heading
            event.description = description
            event.para1 = para1
            event.para2 = para2
            event.para3 = para3
            event.category = category
            event.save()
        else:  # ✅ Create new
            event = LifeEvent.objects.create(
                heading=heading,
                description=description,
                para1=para1,
                para2=para2,
                para3=para3,
                category=category
            )

        # ✅ Handle new image uploads (for both new/edit)
        for img in request.FILES.getlist('images[]'):
            LifeEventImage.objects.create(event=event, image=img)

        return redirect('admin_cybexelife')

    events = LifeEvent.objects.all()
    return render(request, 'admin_cybexelife.html', {'Events': events})


def delete_event(request, event_id):
    event = get_object_or_404(LifeEvent, id=event_id)
    event.delete()
    return redirect('admin_cybexelife')
def get_event_images(request, event_id):
    images = LifeEventImage.objects.filter(event_id=event_id)
    data = {
        "images": [{"id": img.id, "url": img.image.url} for img in images]
    }
    return JsonResponse(data)
def delete_event_image(request, id):
    image = get_object_or_404(LifeEventImage, id=id)
    image.delete()
    return redirect('admin_cybexelife') 