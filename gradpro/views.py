import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import base64
from io import BytesIO
import numpy as np
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from gradpro.forms import UserForm, SelfManagementForm, SocialIntelligenceForm, InnovationForm, SocialComposureForm, \
    SocialConfirmationForm, SocialExperienceForm, AppropriateDisclosureForm, ArticulationForm, WitForm, \
    AdaptabilityFirstForm, AdaptabilitySecondForm, AdaptabilityThirdForm, AdaptabilityFourthForm, AdaptabilityFifthForm
from gradpro.models import User, Response, SelfManagement, SocialIntelligence, Innovation, Communication, \
    ComResponse, Adaptability, AdaResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
# Renders the homepage
def index(request):
    response = render(request, 'gradpro/index.html')
    if request.session.get_expiry_age() > 0:
        if not request.user.is_anonymous:
            # Creates a context dictionary that will be passed to the template and retrieves the current user
            context_dict = dict()
            user = get_user(request.user)
            context_dict['user_obj'] = user
            response = render(request, 'gradpro/index.html', context=context_dict)
    return response


# Renders the dashboard
# The login_required() decorator to ensure only those logged in can access the view.
@login_required
def dashboard(request):
    context_dict = dict()
    user = get_user(request.user)
    context_dict['user_obj'] = user

    # Retrieves the last responses of the user in the tests
    last_response = Response.objects.filter(user=user).last()
    last_comresponse = ComResponse.objects.filter(user=user).last()
    last_adaresponse = AdaResponse.objects.filter(user=user).last()

    # If there is no previous attempt at the meta-skills test, that is passed to the template
    if not last_response:
        context_dict['no_data'] = "You have not taken the general test yet. Please click the button below!"
    else:
        # Retrieves the last model instances of the meta-skills test and saves them in the context dict
        self_management = SelfManagement.objects.get(response=last_response)
        social_intelligence = SocialIntelligence.objects.get(response=last_response)
        innovation = Innovation.objects.get(response=last_response)
        context_dict['self_management'] = self_management
        context_dict['social_intelligence'] = social_intelligence
        context_dict['innovation'] = innovation
        # Calls helper functions to generate the dashboard graphs and saves them to the context dict
        context_dict['bar_chart'] = bar_chart(self_management, social_intelligence, innovation)
        context_dict['line_chart'] = line_chart(user)
        context_dict['self_graph'] = self_graph(self_management)
        context_dict['social_graph'] = social_graph(social_intelligence)
        context_dict['inno_graph'] = inno_graph(innovation)

    # As above but for the communication test
    if not last_comresponse:
        context_dict['no_comdata'] = "You have not taken the communication test yet. Please click the button below!"
    else:
        communication = Communication.objects.get(response=last_comresponse)
        context_dict['communication'] = communication
        context_dict['com_bar_chart'] = com_bar_chart(communication)
        context_dict['com_line_chart'] = com_line_chart(user)
        context_dict['com_graphic'] = com_graph(communication)
        context_dict['com_graphic_average'] = com_graph_average()

    # As above but for the adaptability test
    if not last_adaresponse:
        context_dict['no_adadata'] = "You have not taken the adaptability test yet. Please click the button below!"
    else:
        adaptability = Adaptability.objects.get(response=last_adaresponse)
        context_dict['adaptability'] = adaptability
        context_dict['ada_bar_chart'] = ada_bar_chart(adaptability)
        context_dict['ada_line_chart'] = ada_line_chart(user)
        context_dict['ada_graphic'] = ada_graph(adaptability)
        context_dict['ada_graphic_average'] = ada_graph_average()

    return render(request, 'gradpro/dashboard.html', context=context_dict)


# Renders the about page
def about(request):
    # context_dict = dict()
    # user = get_user(request.user)
    # context_dict['user_obj'] = user
    response = render(request, 'gradpro/about.html')
    return response


# Function used to render registration page and register users
def register(request):
    registered = False
    registered_message = 'Thank you for registering!'
    # Passes the appropriate data to the template after the user has registered
    if request.method == 'GET':
        if 'registered' in request.GET:
            if 'registered_message' in request.GET:
                registered_message = request.GET['registered_message']
            return render(request, 'gradpro/register.html',
                          context={'registered': request.GET['registered'], 'registered_message': registered_message})
    # If the user submits the form
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        # If the form is valid, a new user object is created
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            # Handles invalid requests
            email = request.POST.get('email')
            if email:
                # If an account already exists with this email, an appropriate message is passed to the template
                if User.objects.filter(email=email).count() > 0:
                    registered = True
                    registered_message = "Account already exists with email '" + email + "'"
                else:
                    return HttpResponse("Bad request")
            else:
                return HttpResponse("Bad request")
                print(user_form.errors)
    else:
        # If it's a GET request, creates the registration form
        user_form = UserForm()

    return render(request, 'gradpro/register.html', context={'user_form': user_form,
                                                             'registered': registered,
                                                             'registered_message': registered_message})


# Function used to render login page and log in the user
def user_login(request):
    context_dict = dict()
    # If it's a POST request, retrieves the relevant information.
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Try to login the user with Django's authenticate method
        user = authenticate(email=email, password=password)
        # If the user exists in the database
        if user:
            if request.POST.get('remember_me', None) == "on":
                # The session will expire after 2 weeks
                request.session['user'] = email
                request.session.set_expiry(settings.SESSION_EXPIRY)
            else:
                # Sets the global session expiry policy
                request.session.set_expiry(0)
            # If the account is valid, logs the user in and redirects them to the homepage.
            login(request, user)
            return redirect(reverse('gradpro:index'))
        else:
            # If invalid login details were provided, the user cannot login and an appropriate message is sent
            context_dict['message'] = "Invalid login details supplied."

        return render(request, 'gradpro/login.html', context=context_dict)
    # If it's not a POST request
    else:
        # If the user is already logged in, return them to the homepage
        if not request.user.is_anonymous:
            return redirect(reverse('gradpro:index'))
        # Render the login page
        return render(request, 'gradpro/login.html', context=context_dict)


# Function used to log the user out
@login_required
def user_logout(request):
    # Logs the user out with Django's logout method, then redirects them to the login page
    logout(request)
    return redirect(reverse('gradpro:login'))


# The first of three functions that handle the meta-skills questionnaire
@login_required
def questionnaire(request):
    # If it's a POST request, retrieve the date from the form
    if request.method == 'POST':
        self_management_form = SelfManagementForm(request.POST)
        # If the form is valid
        if self_management_form.is_valid():
            # Retrieves the user, creates a new Response object and links them
            user = get_user(request.user)
            response = Response.objects.create(user=user)
            # Creates a self-management object and links it to the response instance
            self_management = self_management_form.save(commit=False)
            self_management.response = response

            # Call a helper function to calculate the scores for self-management
            self_management_scores = calc_self_management(self_management)
            # Save the scores to the model
            self_management.score = self_management_scores['gen_score']
            self_management.concentration_score = self_management_scores['avg_concentration']
            self_management.adaptability_score = self_management_scores['avg_adaptability']
            self_management.initiative_score = self_management_scores['avg_initiative']
            # Save the self-management object to the database
            self_management.save()

            # Redirect to the second page/form
            return redirect(reverse('gradpro:questionnaire2'))
    else:
        # If it's a GET request, create the self-management form
        self_management_form = SelfManagementForm()

    return render(request, 'gradpro/questionnaire.html', context={'self_management_form': self_management_form})


# The second of three functions that handle the meta-skills questionnaire. Similar logic as above but for the social
# intelligence model
@login_required
def questionnaire2(request):
    if request.method == 'POST':
        social_intelligence_form = SocialIntelligenceForm(request.POST)

        if social_intelligence_form.is_valid():
            user = get_user(request.user)
            response = Response.objects.filter(user=user).last()
            social_intelligence = social_intelligence_form.save(commit=False)
            social_intelligence.response = response

            social_intelligence_scores = calc_social_intelligence(social_intelligence)
            social_intelligence.score = social_intelligence_scores['gen_score']
            social_intelligence.communication_score = social_intelligence_scores['avg_communication']
            social_intelligence.collaborating_score = social_intelligence_scores['avg_collaborating']
            social_intelligence.feeling_score = social_intelligence_scores['avg_feeling']
            social_intelligence.save()

            # Redirect to the third page/form
            return redirect(reverse('gradpro:questionnaire3'))
    else:
        social_intelligence_form = SocialIntelligenceForm()

    return render(request, 'gradpro/questionnaire2.html',
                  context={'social_intelligence_form': social_intelligence_form})


# The third of three functions that handle the meta-skills questionnaire. Similar logic as above but for the innovation
# model
@login_required
def questionnaire3(request):
    completed = False
    completed_message = 'Thank you for completing the questionnaire!'
    # If it's a GET request and the form was submitted, an appropriate message is sent to the user
    if request.method == 'GET':
        if 'completed' in request.GET:
            if 'completed_message' in request.GET:
                completed_message = request.GET['completed_message']
            return render(request, 'gradpro/questionnaire3.html',
                          context={'completed': request.GET['completed'], 'completed_message': completed_message})

    if request.method == 'POST':
        innovation_form = InnovationForm(request.POST)

        if innovation_form.is_valid():
            user = get_user(request.user)
            response = Response.objects.filter(user=user).last()
            innovation = innovation_form.save(commit=False)
            innovation.response = response

            innovation_scores = calc_innovation(innovation)
            innovation.score = innovation_scores['gen_score']
            innovation.sense_making_score = innovation_scores['avg_sense_making']
            innovation.curiosity_score = innovation_scores['avg_curiosity']
            innovation.creativity_score = innovation_scores['avg_creativity']
            innovation.critical_thinking_score = innovation_scores['avg_critical_thinking']
            innovation.save()

            # Since the survey is completed, that is passed to the template
            completed = True
    else:
        innovation_form = InnovationForm()

    return render(request, 'gradpro/questionnaire3.html',
                  context={'innovation_form': innovation_form, 'completed': completed})


# The first of three functions that handle the communication questionnaire. Each function contains two forms
# (corresponding to the equivalent dimensions of communication)
@login_required
def communication(request):
    # If it's a POST request, retrieve the date from the social composure form
    if request.method == 'POST':
        social_composure_form = SocialComposureForm(request.POST)
        # If the form is valid
        if social_composure_form.is_valid():
            # Retrieves the user, creates a new ComResponse object and links them
            user = get_user(request.user)
            response = ComResponse.objects.create(user=user)
            # Creates a communication object and links it to the response instance
            communication = social_composure_form.save(commit=False)
            communication.response = response

            # Calls a helper function to reverse the score on certain questions
            communication.q1 = reverse_score(communication.q1)
            communication.q2 = reverse_score(communication.q2)
            communication.q3 = reverse_score(communication.q3)
            communication.q4 = reverse_score(communication.q4)
            # Calculates the social composure score and save the communication object to the database
            communication.social_composure_score = round(
                (communication.q1 + communication.q2 + communication.q3 + communication.q4 + communication.q5) / 5)
            communication.save()

            # Retrieve the data from the social confirmation, linking it to the previously created communication object
            social_confirmation_form = SocialConfirmationForm(request.POST, instance=communication)
            # If the form is valid
            if social_confirmation_form.is_valid():
                communication = social_confirmation_form.save(commit=False)
                # Calculate the social confirmation score and save the updates communication object
                communication.social_confirmation_score = round(
                    (communication.q6 + communication.q7 + communication.q8 + communication.q9 + communication.q10) / 5)
                communication.save()
                # Redirect the user to the second page of the test
                return redirect(reverse('gradpro:communication2'))
    else:
        # If it's a GET request, create the Social Composure and Social Confirmation forms
        social_composure_form = SocialComposureForm()
        social_confirmation_form = SocialConfirmationForm()

    return render(request, 'gradpro/communication.html',
                  context={'social_composure_form': social_composure_form,
                           'social_confirmation_form': social_confirmation_form})


# The second of three functions that handle the communication questionnaire. Similar logic as above but for the social
# experience and appropriate disclosure forms
@login_required
def communication2(request):
    # If it's a POST request, retrieve the user and their last ComRespose and Communication objects
    if request.method == 'POST':
        user = get_user(request.user)
        response = ComResponse.objects.filter(user=user).last()
        communication = Communication.objects.get(response=response)

        # Retrieve the date from the social experience form, linking it to the communication object
        social_experience_form = SocialExperienceForm(request.POST, instance=communication)
        if social_experience_form.is_valid():
            communication = social_experience_form.save(commit=False)
            communication.q15 = reverse_score(communication.q15)
            communication.social_experience_score = round(
                (communication.q11 + communication.q12 + communication.q13 + communication.q14 + communication.q15) / 5)
            communication.save()

            appropriate_disclosure_form = AppropriateDisclosureForm(request.POST, instance=communication)
            if appropriate_disclosure_form.is_valid():
                communication = appropriate_disclosure_form.save(commit=False)
                communication.appropriate_disclosure_score = round(
                    (communication.q16 + communication.q17 + communication.q18 + communication.q19 +
                     communication.q20) / 5)
                communication.save()
                # Redirect the user to the third page of the test
                return redirect(reverse('gradpro:communication3'))
    else:
        social_experience_form = SocialExperienceForm()
        appropriate_disclosure_form = AppropriateDisclosureForm()

    return render(request, 'gradpro/communication2.html',
                  context={'social_experience_form': social_experience_form,
                           'appropriate_disclosure_form': appropriate_disclosure_form})


# The third of three functions that handle the communication questionnaire. Similar logic as above but for the
# articulation and wit forms
@login_required
def communication3(request):
    completed = False
    completed_message = 'Thank you for completing the questionnaire!'
    # If it's a GET request and the form was submitted, an appropriate message is sent to the user
    if request.method == 'GET':
        if 'completed' in request.GET:
            if 'completed_message' in request.GET:
                completed_message = request.GET['completed_message']
            return render(request, 'gradpro/communication3.html',
                          context={'completed': request.GET['completed'], 'completed_message': completed_message})

    if request.method == 'POST':
        user = get_user(request.user)
        response = ComResponse.objects.filter(user=user).last()
        communication = Communication.objects.get(response=response)
        articulation_form = ArticulationForm(request.POST, instance=communication)
        if articulation_form.is_valid():
            communication = articulation_form.save(commit=False)
            communication.q21 = reverse_score(communication.q21)
            communication.q22 = reverse_score(communication.q22)
            communication.q23 = reverse_score(communication.q23)
            communication.q24 = reverse_score(communication.q24)
            communication.q25 = reverse_score(communication.q25)
            communication.articulation_score = round(
                (communication.q21 + communication.q22 + communication.q23 + communication.q24 + communication.q25) / 5)

            wit_form = WitForm(request.POST, instance=communication)
            if wit_form.is_valid():
                communication = wit_form.save(commit=False)

                communication.wit_score = round(
                    (communication.q26 + communication.q27 + communication.q28 + communication.q29 +
                     communication.q30) / 5)

                # Since all forms have been completes, calculates the general communication score and saves it
                communication.score = round((communication.social_composure_score +
                                             communication.social_confirmation_score +
                                             communication.social_experience_score +
                                             communication.appropriate_disclosure_score +
                                             communication.articulation_score +
                                             communication.wit_score) / 6)
                communication.save()

                # Since the survey is completed, that is passed to the template
                completed = True
    else:
        articulation_form = ArticulationForm()
        wit_form = WitForm()

    return render(request, 'gradpro/communication3.html',
                  context={'articulation_form': articulation_form, 'wit_form': wit_form, 'completed': completed})


# The first of five functions that handle the adaptability questionnaire
@login_required
def adaptability(request):
    # If it's a POST request, retrieve the date from the social composure form
    if request.method == 'POST':
        adaptability_first_form = AdaptabilityFirstForm(request.POST)
        # If the form is valid
        if adaptability_first_form.is_valid():
            # Retrieves the user, creates a new AdaResponse object and links them
            user = get_user(request.user)
            response = AdaResponse.objects.create(user=user)

            # Creates an adaptability n object and links it to the response instance
            adaptability = adaptability_first_form.save(commit=False)
            adaptability.response = response

            # Calls a helper function to reverse the score on a question
            adaptability.q3 = reverse_score(adaptability.q3)
            # Save the adaptability instance
            adaptability.save()
            # Redirects the user to the second page
            return redirect(reverse('gradpro:adaptability2'))
    else:
        # If it's a GET request, create the first adaptability form
        adaptability_first_form = AdaptabilityFirstForm()

    return render(request, 'gradpro/adaptability.html',
                  context={'adaptability_first_form': adaptability_first_form})


# The second of five functions that handle the adaptability questionnaire. Similar logic as above
@login_required
def adaptability2(request):
    if request.method == 'POST':
        user = get_user(request.user)
        response = AdaResponse.objects.filter(user=user).last()
        adaptability = Adaptability.objects.get(response=response)
        adaptability_second_form = AdaptabilitySecondForm(request.POST, instance=adaptability)
        if adaptability_second_form.is_valid():
            adaptability = adaptability_second_form.save(commit=False)
            adaptability.q15 = reverse_score(adaptability.q15)
            adaptability.q20 = reverse_score(adaptability.q20)
            adaptability.q21 = reverse_score(adaptability.q21)
            adaptability.save()

            return redirect(reverse('gradpro:adaptability3'))
    else:
        adaptability_second_form = AdaptabilitySecondForm()

    return render(request, 'gradpro/adaptability2.html',
                  context={'adaptability_second_form': adaptability_second_form})


# The third of five functions that handle the adaptability questionnaire. Similar logic as above
@login_required
def adaptability3(request):
    if request.method == 'POST':
        user = get_user(request.user)
        response = AdaResponse.objects.filter(user=user).last()
        adaptability = Adaptability.objects.get(response=response)

        adaptability_third_form = AdaptabilityThirdForm(request.POST, instance=adaptability)
        if adaptability_third_form.is_valid():
            adaptability = adaptability_third_form.save(commit=False)
            adaptability.q23 = reverse_score(adaptability.q23)
            adaptability.q26 = reverse_score(adaptability.q26)
            adaptability.q28 = reverse_score(adaptability.q28)
            adaptability.q32 = reverse_score(adaptability.q32)
            adaptability.save()

            return redirect(reverse('gradpro:adaptability4'))
    else:
        adaptability_third_form = AdaptabilityThirdForm()

    return render(request, 'gradpro/adaptability3.html',
                  context={'adaptability_third_form': adaptability_third_form})


# The fourth of five functions that handle the adaptability questionnaire. Similar logic as above
@login_required
def adaptability4(request):
    if request.method == 'POST':
        user = get_user(request.user)
        response = AdaResponse.objects.filter(user=user).last()
        adaptability = Adaptability.objects.get(response=response)

        adaptability_fourth_form = AdaptabilityFourthForm(request.POST, instance=adaptability)
        if adaptability_fourth_form.is_valid():
            adaptability = adaptability_fourth_form.save(commit=False)
            adaptability.q35 = reverse_score(adaptability.q35)
            adaptability.q39 = reverse_score(adaptability.q39)
            adaptability.q41 = reverse_score(adaptability.q41)
            adaptability.save()

            return redirect(reverse('gradpro:adaptability5'))
    else:
        adaptability_fourth_form = AdaptabilityFourthForm()

    return render(request, 'gradpro/adaptability4.html',
                  context={'adaptability_fourth_form': adaptability_fourth_form})


# The fifth of five functions that handle the adaptability questionnaire. Similar logic as above
@login_required
def adaptability5(request):
    completed = False
    completed_message = 'Thank you for completing the questionnaire!'
    if request.method == 'GET':
        # If it's a GET request and the form was submitted, an appropriate message is sent to the user
        if 'completed' in request.GET:
            if 'completed_message' in request.GET:
                completed_message = request.GET['completed_message']
            return render(request, 'gradpro/communication3.html',
                          context={'completed': request.GET['completed'], 'completed_message': completed_message})

    if request.method == 'POST':
        user = get_user(request.user)
        response = AdaResponse.objects.filter(user=user).last()
        adaptability = Adaptability.objects.get(response=response)

        adaptability_fifth_form = AdaptabilityFifthForm(request.POST, instance=adaptability)
        if adaptability_fifth_form.is_valid():
            adaptability = adaptability_fifth_form.save(commit=False)
            adaptability.q51 = reverse_score(adaptability.q51)

            # Since the form is complete, calculates the scores for all the dimensions of adaptability
            adaptability.crisis_score = round(
                (adaptability.q1 + adaptability.q9 + adaptability.q12 + adaptability.q17 + adaptability.q22 +
                 adaptability.q27) / 6)

            adaptability.work_stress_score = round(
                (adaptability.q3 + adaptability.q15 + adaptability.q21 + adaptability.q32 + adaptability.q35) / 5)

            adaptability.creativity_score = round(
                (adaptability.q10 + adaptability.q16 + adaptability.q24 + adaptability.q36 + adaptability.q37) / 5)

            adaptability.uncertainty_score = round(
                (adaptability.q23 + adaptability.q28 + adaptability.q29 + adaptability.q39 + adaptability.q40
                 + adaptability.q43 + adaptability.q47 + adaptability.q52 + adaptability.q54) / 9)

            adaptability.learning_score = round(
                (adaptability.q5 + adaptability.q11 + adaptability.q31 + adaptability.q34 + adaptability.q38
                 + adaptability.q44 + adaptability.q46 + adaptability.q49 + adaptability.q53) / 9)

            adaptability.interpersonal_score = round(
                (adaptability.q4 + adaptability.q7 + adaptability.q18 + adaptability.q30 + adaptability.q33
                 + adaptability.q42 + adaptability.q50) / 7)

            adaptability.cultural_score = round(
                (adaptability.q2 + adaptability.q6 + adaptability.q14 + adaptability.q19 + adaptability.q25) / 5)

            adaptability.physical_score = round(
                (adaptability.q8 + adaptability.q13 + adaptability.q20 + adaptability.q26 + adaptability.q41
                 + adaptability.q45 + adaptability.q48 + adaptability.q51 + adaptability.q55) / 9)

            # Calculates the general adaptability score and saves the object to the database
            adaptability.score = round((adaptability.crisis_score + adaptability.work_stress_score +
                                        adaptability.creativity_score + adaptability.uncertainty_score +
                                        adaptability.learning_score + adaptability.interpersonal_score +
                                        adaptability.cultural_score + adaptability.physical_score) / 8)
            adaptability.save()
            # Since the survey is completed, that is passed to the template
            completed = True
    else:
        adaptability_fifth_form = AdaptabilityFifthForm()

    return render(request, 'gradpro/adaptability5.html',
                  context={'adaptability_fifth_form': adaptability_fifth_form, 'completed': completed})


# This helper method creates the bar chart for the meta-skills survey results. It is passed the three meta-skills
# instances and returns a graph. The bar chart displays the user's last scores in the test, as well as the average
# score for all users
def bar_chart(self_management, social_intelligence, innovation):
    self_score = self_management.score
    social_score = social_intelligence.score
    inno_score = innovation.score
    # Retrieves all users
    users = User.objects.all()

    responses = []
    # Save the last responses of all users to an array
    for user in users:
        last_response = Response.objects.filter(user=user).last()
        responses.append(last_response)

    # Retrieves the last responses of all users for the three metaskills
    self_qs = SelfManagement.objects.filter(response__in=responses)
    social_qs = SelfManagement.objects.filter(response__in=responses)
    inno_qs = SelfManagement.objects.filter(response__in=responses)

    # Saves the count of the responses
    self_count = self_qs.count()
    social_count = social_qs.count()
    inno_count = inno_qs.count()

    # Calculates the average user score for the metaskills
    self_sum = 0
    for i in self_qs:
        self_sum += i.score
    avg_self_score = round(self_sum / self_count)

    social_sum = 0
    for i in social_qs:
        social_sum += i.score
    avg_social_score = round(social_sum / social_count)

    inno_sum = 0
    for i in inno_qs:
        inno_sum += i.score
    avg_inno_score = round(inno_sum / inno_count)

    np.random.seed(19680801)
    plt.rcdefaults()

    # Creates the figure and sets the size
    fig = plt.figure(figsize=(5, 4))
    # The labels for the bar groups
    labels = ["Self-Management", "Social Intelligence", "Innovation"]
    # Sets the values that will be plotted
    user_vals = [self_score, social_score, inno_score]
    avg_vals = [avg_self_score, avg_social_score, avg_inno_score]

    width = 0.25
    r1 = np.arange(len(labels))
    r2 = [x + width for x in r1]

    # Creates the plot with appropriate values
    plt.bar(r1, user_vals, color='blue', width=width, edgecolor='white', label='Your Score')
    plt.bar(r2, avg_vals, color='red', width=width , edgecolor='white', label='Average score')

    # Sets the tick marks of the plot and the y axis label
    plt.xticks([r + width for r in range(len(labels))], labels)
    plt.ylim(0, 5)
    plt.ylabel('Scores')

    # Sets the legend and title of the plot
    plt.legend()
    plt.title('Metaskills Scores')
    plt.tight_layout()

    # Save the graph and return it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


# This helper method creates the line graph for the meta-skills survey results. It is passed the user instance and
# returns a graph. The line chart displays the progress of the user's scores in the test throughout all attempts
def line_chart(u):
    # Retrieves all the responses of the user
    responses = Response.objects.filter(user=u)
    self_res = SelfManagement.objects.filter(response__in=responses)
    social_res = SocialIntelligence.objects.filter(response__in=responses)
    inno_res = Innovation.objects.filter(response__in=responses)

    self_scores = []
    social_scores = []
    inno_scores = []

    # Saves the scores for each metaskill in arrays
    for i in self_res:
        self_scores.append(i.score)
    for i in social_res:
        social_scores.append(i.score)
    for i in inno_res:
        inno_scores.append(i.score)

    # Create the number of tick marks
    xticks = []
    i = 1
    while i < len(self_scores) + 1:
        xticks.append(i)
        i += 1

    # Set the data to be plotted
    x = np.arange(1, len(self_scores) + 1)
    y1 = np.array(self_scores)
    y2 = np.array(social_scores)
    y3 = np.array(inno_scores)

    # Create and plot the figure with appropriate values
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot()
    ax.plot(x, y1, color='blue', label="Self-Management", marker='o', markerfacecolor='blue', markersize=12)
    ax.plot(x, y2, color='red', label="Social Intelligence", linewidth=2)
    ax.plot(x, y3, color='green', label="Innovation", linestyle='dashed')

    # Set the y and x axes tick marks and label
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xticks(xticks)
    ax.set(xlabel='Attempts', ylabel='Score', title='Previous Performance')

    # Set the legend and create a grid in the plot
    ax.legend()
    ax.grid()
    plt.tight_layout()

    # Save the graph and return it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


# This helper method creates the radar chart that displays the self-management subskill scores for the user as well as
# the average score for all users. It is passed the self management instance and returns a graph.
def self_graph(o):
    # Retrieve the users
    users = User.objects.all()
    responses = []
    # Save the last responses of all users to an array
    for user in users:
        last_response = Response.objects.filter(user=user).last()
        responses.append(last_response)

    # Retrieves the last responses of all users for self-management and their count
    self_qs = SelfManagement.objects.filter(response__in=responses)
    count = self_qs.count()

    concentration_sum = 0
    adaptability_sum = 0
    initiative_sum = 0
    # Calculate the average score for all subskills of self-management
    for i in self_qs:
        concentration_sum += i.concentration_score
        adaptability_sum += i.adaptability_score
        initiative_sum += i.initiative_score

    avg_concentration = round(concentration_sum / count)
    avg_adaptability = round(adaptability_sum / count)
    avg_initiative = round(initiative_sum / count)

    # Set the data to be plotted
    df = pd.DataFrame({
        'group': ['A', 'B'],
        'concentration': [o.concentration_score, avg_concentration],
        'adaptability': [o.adaptability_score, avg_adaptability],
        'initiative': [o.initiative_score, avg_initiative]
    })
    # Set the appropriate values for the plot
    categories = list(df)[1:]
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Create the figure and add a subplot
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Set the x and y axes tick marks
    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3], ["1", "2", "3"], color="grey", size=7)
    plt.ylim(0, 3)

    # Create the first plot(user's scores) with appropriate values
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Your Score")
    ax.fill(angles, values, 'b', alpha=0.1)

    # Create the second plot(average scores) with appropriate values
    values = df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Average for all users")
    ax.fill(angles, values, 'r', alpha=0.1)

    ax.tick_params(axis='x', which='major', pad=10)

    # Set the plot legend and title
    plt.legend()
    plt.title("Self-Management sub-skills")
    plt.tight_layout()

    # Save the graph and return it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


# As above, but for social-management
def social_graph(o):
    users = User.objects.all()
    responses = []
    for user in users:
        last_response = Response.objects.filter(user=user).last()
        responses.append(last_response)

    social_qs = SocialIntelligence.objects.filter(response__in=responses)
    count = social_qs.count()

    communication_sum = 0
    collaborating_sum = 0
    feeling_sum = 0
    for i in social_qs:
        communication_sum += i.communication_score
        collaborating_sum += i.collaborating_score
        feeling_sum += i.feeling_score

    avg_communication = round(communication_sum / count)
    avg_collaborating = round(collaborating_sum / count)
    avg_feeling = round(feeling_sum / count)

    df = pd.DataFrame({
        'group': ['A', 'B'],
        'communication': [o.communication_score, avg_communication],
        'collaborating ': [o.collaborating_score, avg_collaborating],
        'feeling': [o.feeling_score, avg_feeling]
    })

    categories = list(df)[1:]
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3], ["1", "2", "3"], color="grey", size=7)
    plt.ylim(0, 3)

    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Your Score")
    ax.fill(angles, values, 'b', alpha=0.1)

    values = df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Average for all users")
    ax.fill(angles, values, 'r', alpha=0.1)

    ax.tick_params(axis='x', which='major', pad=10)

    plt.legend()
    plt.title("Social Intelligence sub-skills")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


# As above, but for innovation
def inno_graph(o):
    users = User.objects.all()
    responses = []
    for user in users:
        last_response = Response.objects.filter(user=user).last()
        responses.append(last_response)

    inno_qs = Innovation.objects.filter(response__in=responses)
    count = inno_qs.count()

    sense_making_sum = 0
    curiosity_sum = 0
    creativity_sum = 0
    critical_thinking_sum = 0
    for i in inno_qs:
        sense_making_sum += i.sense_making_score
        curiosity_sum += i.curiosity_score
        creativity_sum += i.creativity_score
        critical_thinking_sum += i.critical_thinking_score

    avg_sense_making = round(sense_making_sum / count)
    avg_curiosity = round(curiosity_sum / count)
    avg_creativity = round(creativity_sum / count)
    avg_critical_thinking = round(critical_thinking_sum / count)

    df = pd.DataFrame({
        'group': ['A', 'B'],
        'sense_making': [o.sense_making_score, avg_sense_making],
        'curiosity': [o.curiosity_score, avg_curiosity],
        'creativity': [o.creativity_score, avg_creativity],
        'critical_thinking': [o.critical_thinking_score, avg_critical_thinking]
    })

    categories = list(df)[1:]
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3], ["1", "2", "3"], color="grey", size=7)
    plt.ylim(0, 3)

    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Your Score")
    ax.fill(angles, values, 'b', alpha=0.1)

    values = df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Average for all users")
    ax.fill(angles, values, 'r', alpha=0.1)
    ax.tick_params(axis='x', which='major', pad=10)

    plt.legend()
    plt.title("Innovation sub-skills")
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    plt.close()
    return graphic


# This helper method creates the horizontal bar chart for the communication survey results. It is passed the
# communication instance and returns a graph. The bar chart displays the user's last score in the test, as well as the
# average score for all users
def com_bar_chart(o):
    com_score = o.score
    # Retrieves all users
    users = User.objects.all()
    responses = []
    # Saves the users' last responses in an array
    for user in users:
        last_response = ComResponse.objects.filter(user=user).last()
        responses.append(last_response)
    com_qs = Communication.objects.filter(response__in=responses)

    # Retrieves the array's count and calculates the average communication score
    count = com_qs.count()
    sum = 0
    for i in com_qs:
        sum += i.score
    avg_com_score = round(sum / count)

    np.random.seed(19680801)
    plt.rcdefaults()

    # Create the plot figure and set the size
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot()
    # Sets the data to be plotted
    bars = ('Your Score', 'Average Score\nfor all users')
    y_pos = np.arange(len(bars))
    values = [com_score, avg_com_score]

    # Plots the horizontal bar chart with appropriate values
    ax.barh(y_pos, values, color=['blue', 'red'], height=0.7, align='center')
    # Set the y axis tick marks and labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(bars)
    # Invert the y axis
    ax.invert_yaxis()
    # Set the limti for the x axis marks
    ax.set_xlim(0, 5)

    # Set the title of the plot
    ax.set_title('Communication')
    plt.tight_layout()

    # Save the graph and return it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic

# This helper method creates the line graph for the communication survey results. It is passed the user instance and
# returns a graph. The line chart displays the progress of the user's scores in the test throughout all attempts
def com_line_chart(u):
    # Retrieves all the responses of the user
    responses = ComResponse.objects.filter(user=u)
    communication_res = Communication.objects.filter(response__in=responses)

    # Saves all communication scores in an array
    scores = []
    for i in communication_res:
        scores.append(i.score)

    # Create the number of tick marks
    xticks = []
    i = 1
    while i < len(scores) + 1:
        xticks.append(i)
        i += 1

    # Set the data to be plotted
    x = np.arange(1, len(scores) + 1)
    y = np.array(scores)

    # Create and plot the figure with appropriate values
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot()
    ax.plot(x, y)

    # Set the y and x axes tick marks and labels
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xticks(xticks)
    ax.set(xlabel='Attempts', ylabel='Score',
           title='Previous Performance in Communication')

    # Create a grid in the plot
    ax.grid()
    plt.tight_layout()

    # Save the graph and return it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


# This helper method creates the radar chart that displays the communication dimension scores for the user. It is
# passed the communication instance and returns a graph.
def com_graph(o):
    # Set the data to be plotted
    df = pd.DataFrame({
        'group': ['A'],
        'social\ncomposure': o.social_composure_score,
        'social confirmation': o.social_confirmation_score,
        'social experience': o.social_experience_score,
        'appropriate\ndisclosure': o.appropriate_disclosure_score,
        'articulation': o.articulation_score,
        'wit': o.wit_score,
    })
    # Set the appropriate values for the plot
    categories = list(df)[1:]
    N = len(categories)
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Create the figure and add a subplot
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, polar=True)

    # Set the x and y axes tick marks and labels
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.tick_params(axis='x', which='major', pad=12)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
    plt.ylim(0, 5)

    # Create the plot with appropriate values
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    # Set the plot title
    plt.title("Your Score")
    plt.tight_layout()

    # Save the graph and return it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic

# This helper method creates the radar chart that displays the average communication dimension scores for all users.
def com_graph_average():
    # Retrieve the users
    users = User.objects.all()
    responses = []
    # Save the last responses of all users to an array
    for user in users:
        last_response = ComResponse.objects.filter(user=user).last()
        responses.append(last_response)

    # Retrieves the last responses of all users for communication and their count
    ada_qs = Communication.objects.filter(response__in=responses)
    count = ada_qs.count()

    social_composure_sum = 0
    social_experience_sum = 0
    social_confirmation_sum = 0
    appropriate_disclosure_sum = 0
    articulation_sum = 0
    wit_sum = 0
    # Calculate the average score for all dimensions of communication
    for o in ada_qs:
        social_composure_sum += o.social_composure_score
        social_experience_sum += o.social_confirmation_score
        social_confirmation_sum += o.social_experience_score
        appropriate_disclosure_sum += o.appropriate_disclosure_score
        articulation_sum += o.articulation_score
        wit_sum += o.wit_score
    avg_social_composure = round(social_composure_sum / count)
    avg_social_experience = round(social_experience_sum / count)
    avg_social_confirmation = round(social_confirmation_sum / count)
    avg_appropriate_disclosure = round(appropriate_disclosure_sum / count)
    avg_articulation = round(articulation_sum / count)
    avg_wit = round(wit_sum / count)

    # Set the data to be plotted
    df = pd.DataFrame({
        'group': ['A'],
        'social\ncomposure': avg_social_composure,
        'social confirmation': avg_social_experience,
        'social experience': avg_social_confirmation,
        'appropriate\ndisclosure': avg_appropriate_disclosure,
        'articulation': avg_articulation,
        'wit': avg_wit,
    })
    # Set the appropriate values for the plot
    categories = list(df)[1:]
    N = len(categories)
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Create the figure and add a subplot
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, polar=True)

    # Set the x and y axes tick marks and labels
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.tick_params(axis='x', which='major', pad=12)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
    plt.ylim(0, 5)

    # Create the plot with appropriate values
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    # Set the plot title
    plt.title("Average Score for all users")
    plt.tight_layout()

    # Save the graph and return it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic

# The graphs for adaptability follow the same logic as the ones for communication
def ada_bar_chart(o):
    ada_score = o.score
    users = User.objects.all()
    responses = []
    for user in users:
        last_response = AdaResponse.objects.filter(user=user).last()
        responses.append(last_response)
    ada_qs = Adaptability.objects.filter(response__in=responses)

    count = ada_qs.count()
    sum = 0
    for i in ada_qs:
        sum += i.score
    avg_ada_score = round(sum / count)

    np.random.seed(19680801)
    plt.rcdefaults()

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot()
    bars = ('Your Score', 'Average Score\nfor all users')
    y_pos = np.arange(len(bars))
    values = [ada_score, avg_ada_score]

    ax.barh(y_pos, values, color=['blue', 'red'], height=0.7, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(bars)
    ax.invert_yaxis()

    ax.set_xlim(0, 5)
    ax.set_title('Adaptability')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


def ada_line_chart(u):
    responses = AdaResponse.objects.filter(user=u)
    adaptability_res = Adaptability.objects.filter(response__in=responses)
    scores = []
    for i in adaptability_res:
        scores.append(i.score)

    xticks = []
    i = 1
    while i < len(scores) + 1:
        xticks.append(i)
        i += 1

    x = np.arange(1, len(scores) + 1)
    y = np.array(scores)

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot()
    ax.plot(x, y)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xticks(xticks)
    ax.set(xlabel='Attempts', ylabel='Score',
           title='Previous Performance in Adaptability')

    ax.grid()
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


def ada_graph(o):
    df = pd.DataFrame({
        'group': ['A'],
        'crisis': o.crisis_score,
        'work stress': o.work_stress_score,
        'creativity': o.creativity_score,
        'uncertainty': o.uncertainty_score,
        'learning': o.learning_score,
        'interpersonal': o.interpersonal_score,
        'cultural': o.cultural_score,
        'physical': o.physical_score
    })

    categories = list(df)[1:]
    N = len(categories)
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, polar=True)

    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.tick_params(axis='x', which='major', pad=12)
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
    plt.ylim(0, 5)

    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.title("Your Score")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


def ada_graph_average():
    users = User.objects.all()
    responses = []
    for user in users:
        last_response = AdaResponse.objects.filter(user=user).last()
        responses.append(last_response)

    ada_qs = Adaptability.objects.filter(response__in=responses)
    count = ada_qs.count()

    crisis_sum = 0
    work_stress_sum = 0
    creativity_sum = 0
    uncertainty_sum = 0
    learning_sum = 0
    interpersonal_sum = 0
    cultural_sum = 0
    physical_sum = 0

    for o in ada_qs:
        crisis_sum += o.crisis_score
        work_stress_sum += o.work_stress_score
        creativity_sum += o.creativity_score
        uncertainty_sum += o.uncertainty_score
        learning_sum += o.learning_score
        interpersonal_sum += o.interpersonal_score
        cultural_sum += o.cultural_score
        physical_sum += o.physical_score
    avg_crisis = round(crisis_sum / count)
    avg_work_stress = round(work_stress_sum / count)
    avg_creativity = round(creativity_sum / count)
    avg_uncertainty = round(uncertainty_sum / count)
    avg_learning = round(learning_sum / count)
    avg_interpersonal = round(interpersonal_sum / count)
    avg_cultural = round(cultural_sum / count)
    avg_physical = round(physical_sum / count)

    df = pd.DataFrame({
        'group': ['A'],
        'crisis': avg_crisis,
        'work stress': avg_work_stress,
        'creativity': avg_creativity,
        'uncertainty': avg_uncertainty,
        'learning': avg_learning,
        'interpersonal': avg_interpersonal,
        'cultural': avg_cultural,
        'physical': avg_physical
    })

    categories = list(df)[1:]
    N = len(categories)
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111, polar=True)

    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.tick_params(axis='x', which='major', pad=12)

    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
    plt.ylim(0, 5)

    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.title("Average Score for all users")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()
    return graphic


# Helper method that reverses the score of the question that is passed as parameter
def reverse_score(question):
    if question == 1:
        return 5
    elif question == 2:
        return 4
    elif question == 4:
        return 2
    elif question == 5:
        return 1
    else:
        return 3


# Helper method that is used to calculate the scores for self-management and its subskills
def calc_self_management(self_management):
    # Create a dictionary that will hold the values to be returned
    res = dict()

    # Retrieves the average score for the concentration subskill
    avg_concentration = round((self_management.c_q1 + self_management.c_q2 + self_management.c_q3) / 3)
    # If the average score is less than 3 (possible range is 1-7) sets the score to 1 (low)
    if avg_concentration < 3:
        concentration_score = 1
    # If the average score is more than five, sets the score to 3 (high)
    elif avg_concentration > 5:
        concentration_score = 3
    # Else, sets the score to 2 (average)
    else:
        concentration_score = 2

    # Retrieves the average score for the adaptability subskill
    avg_adaptability = self_management.a_q1
    if avg_adaptability == 1:
        adaptability_score = 3
    elif avg_adaptability == 2:
        adaptability_score = 2
    else:
        adaptability_score = 1

    # Retrieves the average score for the initiative subskill, using the same logic as for concentration
    avg_initiative = round((self_management.i_q1 + self_management.i_q2 + self_management.i_q3 +
                            self_management.i_q4) / 4)
    if avg_initiative < 3:
        initiative_score = 1
    elif avg_initiative > 5:
        initiative_score = 3
    else:
        initiative_score = 2


    high_count = 0
    low_count = 0
    avg_count = 0
    # Sets the count of high, average and low scores
    for i in (concentration_score, adaptability_score, initiative_score):
        if i == 3:
            high_count += 1
        elif i == 1:
            low_count += 1
        else:
            avg_count += 1

    # Algorithm that calculates the overall score for self-management based on the subskills scores, on a scale of
    # 1(Low) to 5(High)
    if high_count == 3 or (high_count == 2 and avg_count == 1):
        gen_score = 5
    elif high_count == 2 and low_count == 1:
        gen_score = 4
    elif low_count == 3 or (low_count == 2 and avg_count == 1):
        gen_score = 1
    elif low_count == 2 and high_count == 1:
        gen_score = 2
    else:
        gen_score = 3

    # Assigns the values to the dictionary and returns it to be assigned to the self-management model
    res['gen_score'] = gen_score
    res['avg_concentration'] = concentration_score
    res['avg_adaptability'] = adaptability_score
    res['avg_initiative'] = initiative_score
    return res


# Similar logic as above but for social intelligence
def calc_social_intelligence(social_intelligence):
    res = dict()

    avg_communication = round((social_intelligence.com_q1 + social_intelligence.com_q2 + social_intelligence.com_q3 +
                               social_intelligence.com_q4) / 4)
    if avg_communication == 1:
        communication_score = 1
    elif avg_communication == 2:
        communication_score = 2
    else:
        communication_score = 3

    avg_collaborating = round((social_intelligence.col_q1 + social_intelligence.col_q2 + social_intelligence.col_q3 +
                               social_intelligence.col_q4) / 4)
    if avg_collaborating == 1:
        collaborating_score = 1
    elif avg_collaborating == 2:
        collaborating_score = 2
    else:
        collaborating_score = 3

    # Retrieves the score for the feeling subskill
    avg_feeling = social_intelligence.f_q1
    # If the average score is less than 4 (possible range is 1-10) sets the score to 1 (low)
    if avg_feeling < 4:
        feeling_score = 1
    # If the average score is more than 6 sets the score to 3 (high)
    elif avg_feeling > 6:
        feeling_score = 3
    # Else sets the score to 2 (average)
    else:
        feeling_score = 2

    high_count = 0
    low_count = 0
    avg_count = 0
    for i in (communication_score, collaborating_score, feeling_score):
        if i == 3:
            high_count += 1
        elif i == 1:
            low_count += 1
        else:
            avg_count += 1

    #  Algorithm that calculates the overall score for social intelligence based on the subskills scores, on a scale of
    #  1(Low) to 5(High)
    if high_count == 3 or (high_count == 2 and avg_count == 1):
        gen_score = 5
    elif high_count == 2 and low_count == 1:
        gen_score = 4
    elif low_count == 3 or (low_count == 2 and avg_count == 1):
        gen_score = 1
    elif low_count == 2 and high_count == 1:
        gen_score = 2
    else:
        gen_score = 3

    res['gen_score'] = gen_score
    res['avg_communication'] = communication_score
    res['avg_collaborating'] = collaborating_score
    res['avg_feeling'] = feeling_score
    return res


# Similar logic as above but for innovation
def calc_innovation(innovation):
    res = dict()

    avg_sense_making = round((innovation.s_q1 + innovation.s_q2 + innovation.s_q3 + innovation.s_q4 +
                              innovation.s_q5) / 5)
    if avg_sense_making == 1:
        sense_making_score = 1
    elif avg_sense_making == 2:
        sense_making_score = 2
    else:
        sense_making_score = 3

    avg_curiosity = round((innovation.cu_q1 + innovation.cu_q2 + innovation.cu_q3 + innovation.cu_q4) / 4)
    if avg_curiosity < 3:
        curiosity_score = 1
    elif avg_curiosity > 5:
        curiosity_score = 3
    else:
        curiosity_score = 2

    avg_creativity = innovation.crea_q1
    if avg_creativity == 1:
        creativity_score = 1
    elif avg_creativity == 2:
        creativity_score = 2
    else:
        creativity_score = 3

    avg_critical_thinking = innovation.crit_q1
    if avg_critical_thinking < 4:
        critical_thinking_score = 1
    elif avg_critical_thinking > 6:
        critical_thinking_score = 3
    else:
        critical_thinking_score = 2

    high_count = 0
    low_count = 0
    avg_count = 0
    for i in (sense_making_score, curiosity_score, creativity_score, critical_thinking_score):
        if i == 3:
            high_count += 1
        elif i == 1:
            low_count += 1
        else:
            avg_count += 1

    #  Algorithm that calculates the overall score for innovation based on the subskills scores, on a scale of
    #  1(Low) to 5(High)
    if high_count > 2:
        gen_score = 5
    elif high_count == 2 and low_count != 2:
        gen_score = 4
    elif low_count > 2:
        gen_score = 1
    elif low_count == 2 and high_count != 2:
        gen_score = 2
    else:
        gen_score = 3

    res['gen_score'] = gen_score
    res['avg_sense_making'] = sense_making_score
    res['avg_curiosity'] = curiosity_score
    res['avg_creativity'] = creativity_score
    res['avg_critical_thinking'] = critical_thinking_score
    return res


# Helper function to get the user
def get_user(user):
    if not user.is_anonymous:
        return User.objects.get(pk=user.pk)
    return None
