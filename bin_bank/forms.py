from xml.dom import ValidationErr
from django import forms
from django.forms import ModelForm
from bin_bank.models import MyUser, Transaction
from django.core.exceptions import ValidationError

class FindTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'branchName'
        ]

    def clean_branchName(self):  
        branchName = self.cleaned_data['branchName']
        new = Transaction.objects.filter(branchName = branchName)  
        if new.count()==0:
            raise ValidationError("Cabang tidak terdaftar")  
        return branchName  

    # def clean_amountKg(self):  
    #     amountKg = self.cleaned_data['amountKg']
    #     if amountKg==0 or amountKg == None:
    #         raise ValidationError("Tidak bisa nol")  
    #     return amountKg


    
    

class FeedbackForm(forms.Form):
    feedback = forms.CharField(label="Comment", required=True, max_length=100,
                               widget=forms.Textarea(attrs={'type': 'text', 'placeholder': 'Write your feedback'}))


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationErr("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AddTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amountKg',
            'branchName'
        ]