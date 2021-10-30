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


def registration(request):
    form = UserRegisterForm(request.POST)
    errors = []
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        password_confirmation = form.cleaned_data.get('password_confirmation')

        if password == password_confirmation:

            if User.objects.filter(username=username).exists():
                errors.append("Un utilisateur avec le même nom existe déjà")
                return render(request, "registration.html", {'form': form, 'errors': errors})
            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                login(request, new_user)
                return redirect("/flux")

        else:
            errors.append("Le mot de passe et sa confirmation ne sont pas les mêmes")
            return render(request, "registration.html", {'form': form, 'errors': errors})

    else:
        return render(request, "registration.html", {'form': form})


def signin(request):
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
                return redirect('/signin')

        else:
            errors.append("Nom d'utilisateur ou mot de passe incorrect")
            return render(request, "signin.html", {'form': form, 'errors': errors})

    elif request.user.is_authenticated:
        return redirect('/flux')
    else:
        return render(request, 'signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/signin')


def unfollow(request):
    if request.user.is_authenticated:
        form = UserUnfollowForm(request.POST)
        messages = []
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            user = UserFollows.objects.get(pk=user_id)
            messages.append("Vous ne suivez plus " + str(user.followed_user))
            user.delete()
            return subscriptions(request, messages)
    else:
        return redirect('/signin')


def follow(request):
    if request.user.is_authenticated:
        form = UserFollowForm(request.POST)
        messages = []
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists() and request.user.username != username:
                followed_user = User.objects.get(username=username)
                try:
                    UserFollows.objects.create(user=request.user, followed_user=followed_user)
                    messages.append("Vous suivez maintenant " + str(followed_user.username))
                except IntegrityError:
                    messages.append("Vous suivez déjà " + str(followed_user.username))
                return subscriptions(request, messages)
            elif request.user.username == username:
                messages.append("Vous ne pouvez pas vous suivre vous-même")
                return subscriptions(request, messages)
            else:
                messages.append("L'utilisateur que vous essayez de suivre n'existe pas")
                return subscriptions(request, messages)

        return redirect('/subscriptions')
    else:
        return redirect('/signin')


def subscriptions(request, messages=None):
    if request.user.is_authenticated:
        users = UserFollows.objects.all()
        my_subscriptions = []
        my_subscribers = []

        for u in users:
            if u.user.id == request.user.id:
                my_subscriptions.append(u)
            elif u.followed_user.id == request.user.id:
                my_subscribers.append(u)

        return render(request, "subscriptions.html",
                      {'my_subscriptions': my_subscriptions, 'my_subscribers': my_subscribers,
                       'messages': messages})
    else:
        return redirect('/signin')


def create_ticket(request):
    if request.user.is_authenticated:
        form = CreateTicketForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            new_ticket = Ticket.objects.create(title=title, description=description, user=request.user)
            new_ticket.save()
            return redirect('/flux')

        else:
            return render(request, "create_ticket.html", {'form': form})
    else:
        return redirect('/signin')


def create_review(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('/signin')


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
                    t.is_having_a_review = True
                    r.is_having_a_review = True

        for r in review:
            my_reviews.append(r)

        for t in ticket:
            my_tickets.append(t)

        users = UserFollows.objects.filter(user=request.user)

        for u in users:
            review = Review.objects.filter(user=u.followed_user.id)
            ticket = Ticket.objects.filter(user=u.followed_user.id)

            for mr in my_reviews:
                for r in review:
                    if mr.ticket.id == r.ticket.id and mr.ticket.user.id == request.user.id \
                            and mr.user.id == request.user.id:
                        r.is_having_a_review = True

            for t in ticket:
                for mr in my_reviews:
                    if t.id == mr.ticket.id and t.user.id == u.followed_user.id \
                            and mr.user.id == request.user.id:
                        t.is_having_a_review = True
                        mr.is_having_a_review = True

            for mr in my_reviews:
                for r in review:
                    if mr.ticket.id == r.ticket.id and mr.ticket.user.id == u.followed_user.id \
                            and mr.user.id == request.user.id:
                        r.is_having_a_review = True

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
        return redirect('/signin')


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
        return redirect('/signin')


def add_review(request):
    if request.user.is_authenticated:
        first_form = GetIdForm(request.POST)
        second_form = AddReviewForm(request.POST)
        ticket = None

        if first_form.is_valid():
            id = first_form.cleaned_data.get('id')
            ticket = Ticket.objects.get(pk=id)

        if second_form.is_valid():
            id = second_form.cleaned_data.get('ticket_id')
            ticket = Ticket.objects.get(pk=id)
            new_ticket = ticket
            review_title = second_form.cleaned_data.get('review_title')
            rating = second_form.cleaned_data.get('rating')
            comments = second_form.cleaned_data.get('comments')
            new_review = Review.objects.create(ticket=new_ticket, rating=rating, headline=review_title, body=comments,
                                               user=request.user)
            new_review.save()
            return redirect('/flux')

        else:
            return render(request, "add_review.html", {'form': second_form, 'ticket': ticket})
    else:
        return redirect('/signin')


def update_ticket(request):
    if request.user.is_authenticated:
        first_form = GetIdForm(request.POST)
        second_form = UpdateTicketForm(request.POST)
        ticket = None

        if first_form.is_valid():
            id = first_form.cleaned_data.get('id')
            ticket = Ticket.objects.get(pk=id)

        if second_form.is_valid():
            ticket_id = second_form.cleaned_data.get('ticket_id')
            updated_ticket = Ticket.objects.get(pk=ticket_id)
            updated_ticket.title = second_form.cleaned_data.get('title')
            updated_ticket.description = second_form.cleaned_data.get('description')
            updated_ticket.save()
            return redirect('/posts')

        else:
            second_form = UpdateTicketForm({'title': ticket.title, 'description': ticket.description})
            return render(request, "update_ticket.html", {'form': second_form, 'ticket': ticket})
    else:
        return redirect('/signin')


def delete_ticket(request):
    if request.user.is_authenticated:
        form = GetIdForm(request.POST)

        if form.is_valid():
            id = form.cleaned_data.get('id')
            ticket = Ticket.objects.get(pk=id)
            Review.objects.filter(ticket=ticket).delete()
            ticket.delete()

        return redirect('/posts')
    else:
        return redirect('/signin')


def update_review(request):
    if request.user.is_authenticated:
        first_form = GetReviewAndTicketIdForm(request.POST)
        second_form = UpdateReviewForm(request.POST)
        ticket = None
        review = None

        if first_form.is_valid():
            ticket_id = first_form.cleaned_data.get('ticket_id')
            review_id = first_form.cleaned_data.get('review_id')
            ticket = Ticket.objects.get(pk=ticket_id)
            review = Review.objects.get(pk=review_id)

        if second_form.is_valid():
            review_id = second_form.cleaned_data.get('review_id')
            updated_review = Review.objects.get(pk=review_id)
            updated_review.headline = second_form.cleaned_data.get('review_title')
            updated_review.rating = second_form.cleaned_data.get('rating')
            updated_review.body = second_form.cleaned_data.get('comments')
            updated_review.save()
            return redirect('/posts')

        else:
            second_form = UpdateReviewForm(
                {'review_id': review.id, 'review_title': review.headline, 'rating': review.rating,
                 'comments': review.body})
            return render(request, "update_review.html", {'form': second_form, 'ticket': ticket})
    else:
        return redirect('/signin')


def delete_review(request):
    if request.user.is_authenticated:
        form = GetReviewAndTicketIdForm(request.POST)

        if form.is_valid():
            review_id = form.cleaned_data.get('review_id')
            Review.objects.filter(pk=review_id).delete()

        return redirect('/posts')
    else:
        return redirect('/signin')
