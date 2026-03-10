from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LoginForm,RegisterForm,ForgotPasswordForm,ResetPasswordForm,UserProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .ai_service import generate_roadmap,generate_coding_questions,generate_aptitude_questions,generate_interview_questions,chat_with_ai,extract_resume_text,analyze_resume
from datetime import timedelta
from django.utils import timezone
from .models import LoginActivity,PlacementProgress,UserProfile,PracticeQuestion,Roadmap

# Create your views here.

#Template pages

@login_required
def roadmap_history_generate(request):
    return render(request,'roadmap_history_generate.html')

@login_required
def practice(request):
    return render(request,'practice.html')

@login_required
def ask_ai(request):
    return render (request,'ask_ai.html')

# Home page
@login_required
def home_page(request):
    user = request.user
    aptitude_pages = PracticeQuestion.objects.filter(
        user=user,
        question_type="aptitude"
    ).values("page_number").distinct().count()
    
    coding_pages = PracticeQuestion.objects.filter(
        user=user,
        question_type="coding"
    ).values("page_number").distinct().count()

    interview_pages = PracticeQuestion.objects.filter(
        user=user,
        question_type="interview"
    ).values("page_number").distinct().count()

    context = {
        "aptitude_pages": aptitude_pages,
        "coding_pages": coding_pages,
        "interview_pages": interview_pages,
    }

    return render(request, "home.html", context)

# Roadmap views start
@login_required
def roadmap_view(request):

    if request.method == "POST":
        domain = request.POST.get("domain")
        company = request.POST.get("company")
        timeline = request.POST.get("timeline")

        roadmap_content = generate_roadmap(domain, company, timeline)

        # Save in database
        new_roadmap = Roadmap.objects.create(
            user=request.user,
            domain=domain,
            company=company,
            content=roadmap_content
        )

        # Redirect to detail page
        return redirect("prep:roadmap_detail", roadmap_id=new_roadmap.id)

    return render(request, "roadmap_form.html")

@login_required
def my_roadmaps(request):
    roadmaps = Roadmap.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "my_roadmaps.html", {
        "roadmaps": roadmaps
    })

@login_required
def roadmap_detail(request, roadmap_id):
    roadmap = Roadmap.objects.get(id=roadmap_id, user=request.user)

    return render(request, "roadmap_detail.html", {
        "roadmap": roadmap
    })

@login_required
def delete_roadmap(request, roadmap_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id, user=request.user)

    if request.method == "POST":
        roadmap.delete()
        return redirect("prep:my_roadmaps")

    return redirect("prep:my_roadmaps")

# User login
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,"Registration is Successfully Completed!!!")
            return redirect('prep:login')
    return render(request,'register.html',{'form':form})   

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect("prep:home")
    return render(request,'login.html',{'form':form})

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            # send reset email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password requested"
            message = render_to_string('reset_password_email.html',{'domain':domain,'uid':uid,'token':token})
            send_mail(subject,message,'noreply@example.com',[email])
            messages.success(request,'Email has been sent')
    return render(request,'forgot_password.html',{'form':form})

def reset_password(request, uidb64, token):
        form = ResetPasswordForm()
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                try:
                    uid = force_str(urlsafe_base64_decode(uidb64))

                    user = User.objects.get(pk = uid)
                except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                    user = None
                
                if user is not None and default_token_generator.check_token(user , token):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,"Reset password is successful!")
                    return redirect('prep:login')
                else:
                    messages.error(request,'Invalid link!')
                
        return render(request,'reset_password.html',{'form':form})

def logout(request):
    auth_logout(request)
    return redirect('prep:home')

# Pages in Profile
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Profile completion calculation
    total_fields = 10
    filled_fields = 0

    fields = [
        profile.profile_image,
        profile.phone_number,
        profile.college_name,
        profile.branch,
        profile.graduation_year,
        profile.linkedin_url,
        profile.github_url,
        profile.portfolio_url,
        profile.resume_file,
        profile.bio,
    ]

    for field in fields:
        if field:
            filled_fields += 1

    completion_percentage = int((filled_fields / total_fields) * 100)

    context = {
        'profile': profile,
        'completion': completion_percentage,
    }

    today = timezone.now().date()
    streak = 0
    longest_streak = 0

    activities = LoginActivity.objects.filter(user=request.user).order_by('-login_date')

    current_day = today

    for activity in activities:
        if activity.login_date == current_day:
            streak += 1
            current_day -= timedelta(days=1)
        else:
            break

    # Calculate longest streak
    all_dates = LoginActivity.objects.filter(user=request.user).order_by('login_date')
    temp_streak = 1

    for i in range(1, len(all_dates)):
        if all_dates[i].login_date == all_dates[i-1].login_date + timedelta(days=1):
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    context.update({
        'streak': streak,
        'longest_streak': longest_streak,
    })

    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('prep:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'profile':profile})

@login_required
def progress_dashboard(request):
    progress, created = PlacementProgress.objects.get_or_create(user=request.user)

    context = {
        'progress': progress,
        'overall': progress.overall_progress(),
    }

    return render(request, 'progress_dashboard.html', context)

# AI Chat Box
@login_required
def ai_chat_view(request):
    response_text = None
    user_message = None

    if request.method == "POST":
        user_message = request.POST.get("message")
        response_text = chat_with_ai(user_message)

    return render(request, "ai_chat.html", {
        "response": response_text,
        "user_message": user_message
    })

#Questions for practice
@login_required
def aptitude_view(request):

    user = request.user

    # 🔥 Get page number from URL
    page = int(request.GET.get("page", 1))

    # 🔥 Get user's domain & company
    profile = user.userprofile
    domain = profile.target_domain
    company = profile.target_company

    # 🔍 Check if questions already exist
    questions = PracticeQuestion.objects.filter(
        user=user,
        domain=domain,
        company=company,
        question_type="aptitude",
        page_number=page
    )

    # If not found → generate from AI
    if questions.count() < 5:

        ai_questions = generate_aptitude_questions(domain, company, count=5)

        for q in ai_questions:
            PracticeQuestion.objects.create(
                user=user,
                domain=domain,
                company=company,
                question_type="aptitude",
                page_number=page,
                question_text=q["question"] + "\n\n" + "\n".join(q["options"]),
                answer=q["answer"]
            )

        # Fetch again after saving
        questions = PracticeQuestion.objects.filter(
            user=user,
            domain=domain,
            company=company,
            question_type="aptitude",
            page_number=page
        )

    context = {
        "questions": questions,
        "page": page
    }

    return render(request, "aptitude.html", context)

@login_required
def coding_view(request):

    user = request.user
    page = int(request.GET.get("page", 1))

    profile = user.userprofile
    domain = profile.target_domain
    company = profile.target_company

    questions = PracticeQuestion.objects.filter(
        user=user,
        domain=domain,
        company=company,
        question_type="coding",
        page_number=page
    )

    if questions.count() < 5:

        ai_questions = generate_coding_questions(domain, company, count=5)

        for q in ai_questions:
            PracticeQuestion.objects.create(
                user=user,
                domain=domain,
                company=company,
                question_type="coding",
                page_number=page,
                question_text=q["title"] + "\n\n" + q["description"],
                leetcode_link=q["leetcode_link"]
            )

        questions = PracticeQuestion.objects.filter(
            user=user,
            domain=domain,
            company=company,
            question_type="coding",
            page_number=page
        )

    context = {
        "questions": questions,
        "page": page
    }

    return render(request, "coding.html", context)

@login_required
def interview_view(request):


    user = request.user
    page = int(request.GET.get("page", 1))

    profile = user.userprofile
    domain = profile.target_domain
    company = profile.target_company

    questions = PracticeQuestion.objects.filter(
        user=user,
        domain=domain,
        company=company,
        question_type="interview",
        page_number=page
    )

    if questions.count() < 5:

        ai_questions = generate_interview_questions(domain, company, count=5)

        for q in ai_questions:
            PracticeQuestion.objects.create(
                user=user,
                domain=domain,
                company=company,
                question_type="interview",
                page_number=page,
                question_text=q["question"],
                answer=q["answer"]
            )

        questions = PracticeQuestion.objects.filter(
            user=user,
            domain=domain,
            company=company,
            question_type="interview",
            page_number=page
        )

    context = {
        "questions": questions,
        "page": page
    }

    return render(request, "interview.html", context)

# AI Resume
@login_required
def resume_analyzer(request):

    if request.method == "POST":

        resume = request.FILES["resume"]
        job_description = request.POST["job_description"]
        company = request.POST["company"]

        resume_text = extract_resume_text(resume)

        
        ai_feedback = analyze_resume(resume_text, job_description, company)

        context = {
            
            "analysis": ai_feedback
        }

        return render(request,"resume_result.html",context)

    return render(request,"resume_analyzer.html")