from django.shortcuts import render
from django.http import HttpResponse
import wikipedia
import wikipediaapi
import json

from django.template.loader import render_to_string
import weasyprint
from pprint import pprint

def search(request):
    """
    View for wiki search listing using search box.
    """
    search_found = True # Wiki Page Search
    result = None
    query = None
    if request.GET:
        query = str(request.GET.get('query', ''))
        try:
            wiki_wiki = wikipediaapi.Wikipedia(
                    language='en',
                    extract_format=wikipediaapi.ExtractFormat.HTML
            )
            result = wiki_wiki.page(query)

            if not result.exists():
                search_found = False
                result = search_suggestion(query)
        except:
            result = None

    return render(request,
            'wikiapp/home.html',
            {'result': result,
            'search_found': search_found,
            'query': query,
            })

def autocomplete(request):
    """
    Auto suggest powered by wikipedia.
    """
    if request.is_ajax():
        q = request.GET.get('search', '')
        try:
            results = wikipedia.search(q)
        except:
            results = None
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def pdf_download(request):
    """
    Downloading Wikipedia Article as PDF.
    """
    query = str(request.POST.get('query', ''))
    result = str(request.POST.get('result', ''))
    result_title = str(request.POST.get('result_title', ''))
    result_url = str(request.POST.get('result_url', ''))

    html = render_to_string('wikiapp/pdf.html', 
                            {'result': result,
                            'result_url': result_url,
                            'result_title': result_title,
                            'request':request})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
                "{}.pdf"'.format(query)
    weasyprint.HTML(string=html).write_pdf(response)
    return response
    # return HttpResponse("hi akhil")

def search_suggestion(query):
    result = wikipedia.search(query)
    return result
    