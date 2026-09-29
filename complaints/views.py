import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from .models import Complaint
from .models import Notification, UserProfile



# ---------------- HOME PAGE ----------------

def home(request):
    return render(request, 'complaints/home.html')


# ---------------- USER REGISTRATION ----------------

def register(request):

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        mobile_number = request.POST.get('mobile_number', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        errors = []

        if not full_name:
            errors.append('Please enter your full name.')
        elif len(full_name) > 150:
            errors.append('Your full name must be 150 characters or fewer.')

        if not email:
            errors.append('Please enter your email address.')
        elif len(email) > 150:
            errors.append('Your email address must be 150 characters or fewer.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Please enter a valid email address.')
            if User.objects.filter(Q(email__iexact=email) | Q(username__iexact=email)).exists():
                errors.append('An account with this email already exists.')

        mobile_digits = re.sub(r'\D', '', mobile_number)
        if not mobile_number:
            errors.append('Please enter your mobile number.')
        elif not re.fullmatch(r'[0-9+() -]{10,20}', mobile_number) or not 10 <= len(mobile_digits) <= 15:
            errors.append('Enter a valid mobile number with 10 to 15 digits.')
        elif UserProfile.objects.filter(mobile_number=mobile_number).exists():
            errors.append('An account with this mobile number already exists.')

        if not password:
            errors.append('Please enter a password.')
        elif not confirm_password:
            errors.append('Please confirm your password.')
        elif password != confirm_password:
            errors.append('Passwords do not match.')

        if password:
            try:
                validate_password(
                    password,
                    user=User(username=email, first_name=full_name, email=email),
                )
            except ValidationError as error:
                errors.extend(error.messages)

        if errors:
            return render(request, 'complaints/register.html', {
                'errors': errors,
                'form_data': {
                    'full_name': full_name,
                    'email': email,
                    'mobile_number': mobile_number,
                },
            })

        user = User.objects.create_user(
            username=email,
            first_name=full_name,
            email=email,
            password=password
        )
        UserProfile.objects.create(user=user, mobile_number=mobile_number)

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'complaints/register.html')


# ---------------- USER LOGIN ----------------
def user_login(request):

    if request.method == "POST":

        identifier = request.POST.get("identifier", '').strip()
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        user = User.objects.filter(
            Q(email__iexact=identifier) |
            Q(profile__mobile_number=identifier)
        ).first()
        user = authenticate(request, username=user.username, password=password) if user else None

        if user is not None:
            login(request, user)
            request.session.set_expiry(0 if not remember_me else None)

            # Redirect to HOME page
            return redirect('home')

        else:
            return render(request, 'complaints/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'complaints/login.html')


# ---------------- USER LOGOUT ----------------

def user_logout(request):

    logout(request)

    return redirect('home')


# ---------------- PUBLIC EYE ----------------

def public_eye(request):

    complaints = Complaint.objects.all().order_by('-created_at')

    return render(request, 'complaints/public_eye.html', {
        'complaints': complaints
    })


# ---------------- USER DASHBOARD ----------------

@login_required
def dashboard(request):

    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')[:5]

    total_complaints = Complaint.objects.filter(user=request.user).count()
    pending_count = Complaint.objects.filter(user=request.user, status="Pending").count()
    resolved_count = Complaint.objects.filter(user=request.user, status="Resolved").count()
    high_priority = Complaint.objects.filter(user=request.user, priority="High").count()

    context = {
        "complaints": complaints,
        "total_complaints": total_complaints,
        "pending_count": pending_count,
        "resolved_count": resolved_count,
        "high_priority": high_priority
    }

    return render(request, "complaints/dashboard.html", context)


# ---------------- MY COMPLAINTS ----------------

@login_required
def my_complaints(request):

    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'complaints/my_complaints.html', {
        'complaints': complaints
    })


# ---------------- FORGOT PASSWORD ----------------

def forgot_password(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if len(password) < 8:
            return render(request, 'complaints/forgot_password.html',
                          {'error': 'Password must be at least 8 characters'})

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()

            messages.success(request, "Password updated successfully")
            return redirect('login')

        except User.DoesNotExist:
            return render(request, 'complaints/forgot_password.html',
                          {'error': 'User not found'})

    return render(request, 'complaints/forgot_password.html')


# ---------------- SUBMIT COMPLAINT ----------------

@login_required
def submit_complaint(request):

    if request.method == "POST":

        category = request.POST.get("category")
        other_category = request.POST.get("other_category")

        if category == "Other" or not category:
            category = other_category

        description = request.POST.get("description")
        state = request.POST.get("state")
        city = request.POST.get("city")
        address = request.POST.get("address")
        zipcode = request.POST.get("zipcode")
        priority = request.POST.get("priority")
        image = request.FILES.get("image")

        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        complaint = Complaint.objects.create(
            user=request.user,
            category=category,
            description=description,
            state=state,
            city=city,
            address=address,
            zipcode=zipcode,
            priority=priority,
            image=image,
            latitude=latitude,
            longitude=longitude
        )

        messages.success(
            request,
            f"Complaint submitted successfully. Your Complaint ID is #{complaint.id}."
        )
        return redirect("dashboard")

    return render(request, "complaints/submit_complaint.html")


# ---------------- VIEW SINGLE COMPLAINT ----------------

@login_required
def complaint_detail(request, complaint_id):

    complaint = get_object_or_404(Complaint, id=complaint_id)

    return render(request, 'complaints/complaint_detail.html', {
        'complaint': complaint
    })


# ---------------- EDIT COMPLAINT ----------------

@login_required
def edit_complaint(request, complaint_id):

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if complaint.user != request.user:
        messages.error(request, "You are not allowed to edit this complaint.")
        return redirect('my_complaints')

    if request.method == "POST":

        complaint.category = request.POST.get("category")
        complaint.description = request.POST.get("description")
        complaint.address = request.POST.get("address")
        complaint.city = request.POST.get("city")
        complaint.state = request.POST.get("state")
        complaint.zipcode = request.POST.get("zipcode")
        complaint.priority = request.POST.get("priority")

        complaint.latitude = request.POST.get("latitude")
        complaint.longitude = request.POST.get("longitude")

        if request.FILES.get("image"):
            complaint.image = request.FILES.get("image")

        complaint.save()

        messages.success(request, "Complaint updated successfully")
        return redirect("complaint_detail", complaint_id=complaint.id)

    return render(request, "complaints/edit_complaint.html", {
        "complaint": complaint
    })


# ---------------- DELETE COMPLAINT ----------------

@login_required
def delete_complaint(request, complaint_id):

    complaint = get_object_or_404(Complaint, id=complaint_id)

    # only owner can delete
    if complaint.user != request.user:
        messages.error(request, "You cannot delete this complaint.")
        return redirect('my_complaints')

    complaint.delete()

    messages.success(request, "Complaint deleted successfully.")

    return redirect('my_complaints')


# ---------------- ADMIN DASHBOARD ----------------

@staff_member_required
def admin_dashboard(request):

    complaints = Complaint.objects.all()

    total = complaints.count()
    pending = complaints.filter(status='Pending').count()
    progress = complaints.filter(status='In Progress').count()
    resolved = complaints.filter(status='Resolved').count()

    # Category statistics
    category_data = complaints.values('category').annotate(count=Count('category'))

    categories = []
    category_counts = []

    for item in category_data:
        categories.append(item['category'])
        category_counts.append(item['count'])

    context = {
        'complaints': complaints,
        'total': total,
        'pending': pending,
        'progress': progress,
        'resolved': resolved,
        'categories': categories,
        'category_counts': category_counts,
    }

    return render(request, 'complaints/admin_dashboard.html', context)

# ---------------- UPDATE COMPLAINT STATUS ----------------

@staff_member_required

def update_status(request,id):

    complaint = get_object_or_404(Complaint,id=id)

    if request.method == "POST":

        new_status = request.POST.get("status")
        complaint.status = new_status
        complaint.save()

        Notification.objects.create(
            user=complaint.user,
            message=f"Your complaint '{complaint.title}' status updated to {new_status}"
        )

    return redirect('admin_dashboard')
    return render(request, 'complaints/update_status.html', {
        'complaint': complaint
    })


# ---------------- ADMIN REPORTS ----------------

@staff_member_required
def reports(request):

    pending = Complaint.objects.filter(status='Pending').count()
    in_progress = Complaint.objects.filter(status='In Progress').count()
    resolved = Complaint.objects.filter(status='Resolved').count()

    return render(request, 'complaints/reports.html', {
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
    })
@login_required
def profile(request):

    user = request.user
    profile_updated = False
    profile_errors = []
    form_username = user.username
    form_email = user.email

    # Edit profile details
    if request.method == "POST":
        form_username = request.POST.get("username", "").strip()
        form_email = request.POST.get("email", "").strip().lower()

        if not form_username:
            profile_errors.append("Please enter a username.")
        elif len(form_username) > 150:
            profile_errors.append("Username must be 150 characters or fewer.")
        elif User.objects.filter(username__iexact=form_username).exclude(pk=user.pk).exists():
            profile_errors.append("That username is already in use.")

        if not form_email:
            profile_errors.append("Please enter an email address.")
        else:
            try:
                validate_email(form_email)
            except ValidationError:
                profile_errors.append("Please enter a valid email address.")
            if User.objects.filter(
                Q(email__iexact=form_email) | Q(username__iexact=form_email)
            ).exclude(pk=user.pk).exists():
                profile_errors.append("An account with this email already exists.")

        if not profile_errors:
            user.username = form_username
            user.email = form_email
            user.save()
            profile_updated = True

    # Recent complaints
    recent_complaints = Complaint.objects.filter(user=user).order_by('-created_at')[:5]

    context = {
        "user": user,
        "recent_complaints": recent_complaints,
        "profile_updated": profile_updated,
        "profile_errors": profile_errors,
        "form_username": form_username,
        "form_email": form_email,
    }

    return render(request, "complaints/profile.html", context)

@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})



def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notification_count': count}
    return {'notification_count': 0}

@login_required
def notifications(request):

# Get user notifications
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

# Mark them as read
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)

    return render(request, "complaints/notifications.html", {
        "notifications": notifications
})
@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()

    return redirect('notifications')