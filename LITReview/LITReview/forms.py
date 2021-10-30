from django import forms


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True)
    username.widget.attrs['class'] = 'form-control'
    username.widget.attrs['placeholder'] = 'Nom d\'utilisateur'
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password.widget.attrs['class'] = 'form-control'
    password.widget.attrs['placeholder'] = 'Mot de passe'
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_confirmation.widget.attrs['class'] = 'form-control'
    password_confirmation.widget.attrs['placeholder'] = 'Confirmation du mot de passe'


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    username.widget.attrs['class'] = 'form-control'
    username.widget.attrs['placeholder'] = 'Nom d\'utilisateur'
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password.widget.attrs['class'] = 'form-control'
    password.widget.attrs['placeholder'] = 'Mot de passe'


class UserUnfollowForm(forms.Form):
    user_id = forms.CharField(required=True)


class UserFollowForm(forms.Form):
    username = forms.CharField(required=True)


class CreateTicketForm(forms.Form):
    title = forms.CharField(required=True)
    title.widget.attrs['class'] = 'form-control'
    title.widget.attrs['placeholder'] = 'Titre'
    description = forms.CharField(widget=forms.Textarea, required=True)
    description.widget.attrs['class'] = 'form-control'
    description.widget.attrs['placeholder'] = 'Description'


class CreateReviewForm(forms.Form):
    ticket_title = forms.CharField(required=True)
    ticket_title.widget.attrs['class'] = 'form-control'
    ticket_title.widget.attrs['placeholder'] = 'Titre'
    description = forms.CharField(widget=forms.Textarea, required=True)
    description.widget.attrs['class'] = 'form-control'
    description.widget.attrs['placeholder'] = 'Description'
    review_title = forms.CharField(required=True)
    review_title.widget.attrs['class'] = 'form-control'
    review_title.widget.attrs['placeholder'] = 'Titre'
    choices = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5')]
    rating = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    comments = forms.CharField(widget=forms.Textarea, required=True)
    comments.widget.attrs['class'] = 'form-control'
    comments.widget.attrs['placeholder'] = 'Commentaire'


class GetIdForm(forms.Form):
    id = forms.CharField(required=True)


class AddReviewForm(forms.Form):
    ticket_id = forms.CharField(required=True)
    review_title = forms.CharField(required=True)
    review_title.widget.attrs['class'] = 'form-control'
    review_title.widget.attrs['placeholder'] = 'Titre'
    choices = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5')]
    rating = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    comments = forms.CharField(widget=forms.Textarea, required=True)
    comments.widget.attrs['class'] = 'form-control'
    comments.widget.attrs['placeholder'] = 'Commentaire'


class GetReviewAndTicketIdForm(forms.Form):
    ticket_id = forms.CharField(required=True)
    review_id = forms.CharField(required=True)


class UpdateTicketForm(forms.Form):
    ticket_id = forms.CharField(required=True)
    title = forms.CharField(required=True)
    title.widget.attrs['class'] = 'form-control'
    title.widget.attrs['placeholder'] = 'Titre'
    description = forms.CharField(widget=forms.Textarea, required=True)
    description.widget.attrs['class'] = 'form-control'
    description.widget.attrs['placeholder'] = 'Description'


class UpdateReviewForm(forms.Form):
    review_id = forms.CharField(required=True)
    review_title = forms.CharField(required=True)
    review_title.widget.attrs['class'] = 'form-control'
    review_title.widget.attrs['placeholder'] = 'Titre'
    choices = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5')]
    rating = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    comments = forms.CharField(widget=forms.Textarea, required=True)
    comments.widget.attrs['class'] = 'form-control'
    comments.widget.attrs['placeholder'] = 'Commentaire'
