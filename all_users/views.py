from django.shortcuts import render

# Create your views here.

#show the home page
def index(request):
	return render(request, 'all_users/index.html')
