from django.shortcuts import render, redirect








def general_login(request):
    """Render the role selector page. If a POST with 'role' is received, redirect accordingly."""
    error_message = None

    if request.method == 'POST':
        role = request.POST.get('role')

        if role == 'student':
            return redirect('student_login')
        if role == 'staff':
            return redirect('staff_login')

        error_message = "Please select a role to continue."

    # reuse the existing choose_role template for role selection
    return render(request, 'choose_role.html', {'error_message': error_message})


def choose_role(request):
    return render(request, 'choose_role.html')


def student_login(request):
    # simple form handling: on POST, redirect to student dashboard (placeholder)
    if request.method == 'POST':
        # here you would authenticate; for now, accept any POST and redirect
        return redirect('student_dashboard')
    return render(request, 'student_login.html')


def staff_login(request):
    return render(request, 'staff_login.html')


def student_dashboard(request):
    # placeholder student dashboard page
    return render(request, 'student_dashboard.html')
