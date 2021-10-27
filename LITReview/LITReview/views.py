from itertools import chain

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from django.shortcuts import render, redirect

from .forms import UserRegisterForm, UserLoginForm, UserUnfollowForm, UserFollowForm, CreateTicketForm, \
    CreateReviewForm, GetIdForm, AddReviewForm, UpdateTicketForm, GetReviewAndTicketIdForm, UpdateReviewForm
from .models import UserFollows, Ticket, Review


def index(request):
    return render(request, "index.html")


def inscription(request):
    form = UserRegisterForm(request.POST)
    errors = []
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        passwordconfirmation = form.cleaned_data.get('passwordconfirmation')

        if password == passwordconfirmation:

            if User.objects.filter(username=username).exists():
                errors.append("Username already exists. Registration Failed. Try again.")
                return render(request, "inscription.html", {'form': form, 'errors': errors})
            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                login(request, new_user)
                return redirect("/flux")

        else:
            errors.append("password and confirmpassword does not match. Try again")
            return render(request, "inscription.html", {'form': form, 'errors': errors})

    else:
        return render(request, "inscription.html", {'form': form})


def loginMe(request):
    form = UserLoginForm(request.POST)
    errors = []
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_active:
                return redirect("/flux")
            else:
                return redirect('/loginMe')

        else:
            errors.append("Wrong Username or Password")
            return render(request, "loginMe.html", {'form': form, 'errors': errors})

    elif request.user.is_authenticated:
        return redirect('/flux')
    else:
        return render(request, 'loginMe.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/loginMe')


def unfollow(request):
    form = UserUnfollowForm(request.POST)
    messages = []
    if form.is_valid():
        user_id = form.cleaned_data.get('user_id')
        user = UserFollows.objects.get(pk=user_id)
        messages.append("you are no longer following " + str(user.followed_user))
        user.delete()
        return Abonnements(request, messages)


def follow(request):
    form = UserFollowForm(request.POST)
    messages = []
    if form.is_valid():
        username = form.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() and request.user.username != username:
            followed_user = User.objects.get(username=username)
            try:
                UserFollows.objects.create(user=request.user, followed_user=followed_user)
                messages.append("you are now following " + str(followed_user.username))
            except IntegrityError:
                messages.append("you are already following " + str(followed_user.username))
            return Abonnements(request, messages)
        elif request.user.username == username:
            messages.append("you cant follow yourself")
            return Abonnements(request, messages)
        else:
            messages.append("The user you are trying to follow dont exist in the db")
            return Abonnements(request, messages)

    return redirect('/Abonnements')


def Abonnements(request, messages = None):
    if request.user.is_authenticated:
        users = UserFollows.objects.all()
        my_subscriptions = []
        my_subscribers = []

        for u in users:
            if u.user.id == request.user.id:
                my_subscriptions.append(u)
            elif u.followed_user.id == request.user.id:
                my_subscribers.append(u)

        return render(request, "Abonnements.html",
                      {'my_subscriptions': my_subscriptions, 'my_subscribers': my_subscribers, 'messages': messages})
    else:
        return redirect('/loginMe')


def create_ticket(request):
    form = CreateTicketForm(request.POST)

    if form.is_valid():
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        new_ticket = Ticket.objects.create(title=title, description=description, user=request.user)
        new_ticket.save()
        return redirect('/flux')

    else:
        return render(request, "create_ticket.html", {'form': form})


def create_review(request):
    form = CreateReviewForm(request.POST)

    if form.is_valid():
        ticket_title = form.cleaned_data.get('ticket_title')
        description = form.cleaned_data.get('description')
        new_ticket = Ticket.objects.create(title=ticket_title, description=description, user=request.user)
        new_ticket.save()
        review_title = form.cleaned_data.get('review_title')
        rating = form.cleaned_data.get('rating')
        comments = form.cleaned_data.get('comments')
        new_review = Review.objects.create(ticket=new_ticket, rating=rating, headline=review_title, body=comments,
                                           user=request.user)
        new_review.save()
        return redirect('/flux')

    else:
        return render(request, "create_review.html", {'form': form})


def flux(request):
    if request.user.is_authenticated:

        my_reviews = []
        my_tickets = []

        their_reviews = []
        their_tickets = []

        review = Review.objects.filter(user=request.user)
        ticket = Ticket.objects.filter(user=request.user)

        for t in ticket:
            for r in review:
                if t.id == r.ticket.id and t.user.id == request.user.id and r.user.id == request.user.id:
                    t.is_having_a_reveiw = True
                    r.is_having_a_reveiw = True

        for r in review:
            my_reviews.append(r)

        for t in ticket:
            my_tickets.append(t)

        users = UserFollows.objects.filter(user=request.user)

        for u in users:
            review = Review.objects.filter(user=u.followed_user.id)
            ticket = Ticket.objects.filter(user=u.followed_user.id)

            for t in my_reviews:
                for r in review:
                    if t.ticket.id == r.ticket.id and t.ticket.user.id == request.user.id and t.user.id == request.user.id:
                        r.is_having_a_reveiw = True

            for t in ticket:
                for r in my_reviews:
                    if t.id == r.ticket.id and t.user.id == u.followed_user.id and r.user.id == request.user.id:
                        t.is_having_a_reveiw = True
                        r.is_having_a_reveiw = True

            for t in my_reviews:
                for r in review:
                    if t.ticket.id == r.ticket.id and t.ticket.user.id == u.followed_user.id and t.user.id == request.user.id:
                        r.is_having_a_reveiw = True

            for r in review:
                their_reviews.append(r)

            for t in ticket:
                their_tickets.append(t)

        reviews = my_reviews + their_reviews
        tickets = my_tickets + their_tickets

        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return render(request, "flux.html", {'posts': posts})
    else:
        return redirect('/loginMe')


def posts(request):
    if request.user.is_authenticated:
        reviews = []
        tickets = []

        review = Review.objects.filter(user_id=request.user.id)
        ticket = Ticket.objects.filter(user_id=request.user.id)

        for r in review:
            reviews.append(r)
        for t in ticket:
            tickets.append(t)

        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return render(request, "posts.html", {'posts': posts})
    else:
        return redirect('/loginMe')


def add_review(request):
    form2 = GetIdForm(request.POST)
    form = AddReviewForm(request.POST)
    ticket = None

    if form2.is_valid():
        id = form2.cleaned_data.get('id')
        ticket = Ticket.objects.get(pk=id)

    if form.is_valid():
        id = form.cleaned_data.get('ticket_id')
        ticket = Ticket.objects.get(pk=id)
        new_ticket = ticket
        review_title = form.cleaned_data.get('review_title')
        rating = form.cleaned_data.get('rating')
        comments = form.cleaned_data.get('comments')
        new_review = Review.objects.create(ticket=new_ticket, rating=rating, headline=review_title, body=comments,
                                           user=request.user)
        new_review.save()
        return redirect('/flux')

    else:
        return render(request, "add_review.html", {'form': form, 'ticket': ticket})


def update_ticket(request):
    form = GetIdForm(request.POST)
    ticket = None
    form2 = UpdateTicketForm(request.POST)

    if form.is_valid():
        id = form.cleaned_data.get('id')
        ticket = Ticket.objects.get(pk=id)

    if form2.is_valid():
        ticket_id = form2.cleaned_data.get('ticket_id')
        updated_ticket = Ticket.objects.get(pk=ticket_id)
        updated_ticket.title = form2.cleaned_data.get('title')
        updated_ticket.description = form2.cleaned_data.get('description')
        updated_ticket.save()
        return redirect('/posts')

    else:
        form2 = UpdateTicketForm({'title': ticket.title, 'description': ticket.description})
        return render(request, "update_ticket.html", {'form': form2, 'ticket': ticket})


def delete_ticket(request):
    form = GetIdForm(request.POST)

    if form.is_valid():
        id = form.cleaned_data.get('id')
        ticket = Ticket.objects.get(pk=id)
        Review.objects.filter(ticket=ticket).delete()
        ticket.delete()

    return redirect('/posts')


def update_review(request):
    form = GetReviewAndTicketIdForm(request.POST)
    ticket = None
    review = None
    form2 = UpdateReviewForm(request.POST)

    if form.is_valid():
        ticket_id = form.cleaned_data.get('ticket_id')
        review_id = form.cleaned_data.get('review_id')
        ticket = Ticket.objects.get(pk=ticket_id)
        review = Review.objects.get(pk=review_id)

    if form2.is_valid():
        review_id = form2.cleaned_data.get('review_id')
        updated_review = Review.objects.get(pk=review_id)
        updated_review.headline = form2.cleaned_data.get('review_title')
        updated_review.rating = form2.cleaned_data.get('rating')
        updated_review.body = form2.cleaned_data.get('comments')
        updated_review.save()
        return redirect('/posts')

    else:
        form2 = UpdateReviewForm({'review_id': review.id, 'review_title': review.headline, 'rating': review.rating, 'comments': review.body})
        return render(request, "update_review.html", {'form': form2, 'ticket': ticket})


def delete_review(request):
    form = GetReviewAndTicketIdForm(request.POST)

    if form.is_valid():
        review_id = form.cleaned_data.get('review_id')
        Review.objects.filter(pk=review_id).delete()

    return redirect('/posts')