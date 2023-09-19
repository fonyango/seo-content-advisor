from rest_framework.response import Response
from rest_framework import status
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import textForm
from django.shortcuts import render
from .blog_text import KeywordExplorer


@csrf_exempt
def home(request):

    return render(request, 'templates/content/home.html')


@csrf_exempt
def get_keywords(request):
    """
    returns 10 single keywords
    """
    try:
        if request.method=='POST':
            form = textForm(request.POST)
            
            if form.is_valid():
                text_input = form.cleaned_data['text_input']
           
            explorer = KeywordExplorer(text_input,10)
            keywords = explorer.extract_single_keywords()

            keywords = keywords.to_dict('records')

            context = {
                "keywords":keywords,
                "form": form 
            }

            form = textForm()

            return render(request, 'templates/content/keywords.html', context)
        
        else:
            form = textForm()
            context = {'form': form}
            return render(request, 'templates/content/keywords.html', context)

    except Exception as e:
        print(e)
        return Response({
                            "Success": False, 
                            "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                            "Message":"An error was encountered during execution"
                        })
    
@csrf_exempt
def get_bigrams(request):
    """
    returns 10 two-tail keywords
    """
    try:
        if request.method=='POST':
            form = textForm(request.POST)
            
            if form.is_valid():
                text_input = form.cleaned_data['text_input']
            
            num_keywords = 10
            explorer = KeywordExplorer(text_input, num_keywords)
            bigrams = explorer.extract_two_tail_keywords()
            bigrams = bigrams.head(num_keywords)

            bigrams = bigrams.to_dict('records')

            context = {
                "bigrams":bigrams,
                "form": form 
            }
        
            form = textForm()

            return render(request, 'templates/content/bigrams.html', context)
        
        else:
            form = textForm()
            context = {'form': form}
            return render(request, 'templates/content/bigrams.html', context)

    except Exception as e:
        print(e)
        return Response({
                            "Success": False, 
                            "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                            "Message":"An error was encountered during execution"
                        })