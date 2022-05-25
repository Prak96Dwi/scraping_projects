""" core/views.py """
from bs4 import BeautifulSoup
import requests

# API URLs
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import render, redirect
from core.serializer import ContentTextSerializer


def index(request):
    """
    This is the main which renders a form
    with heading 'Enter Title' in which one input box we can enter famous personality
    name and second input box is to enter wikepedia url
    After submit form new page having information of a person
    whose name you have input in this form.

    """ 
    if request.method == 'POST':
        data = request.POST.get('data')

        if data:
            pages = requests.get(f"https://www.wikipedia.org/wiki/{data}")
            if pages.status_code == status.HTTP_200_OK:
                return redirect('data-detail', name=data)
            key = "This data is not available in Wikipedia"
            return render(request, 'core/index.html', {'errors': key})
    return render(request, 'core/index.html', {})


def search_data(request, name=None):
    """Search data function

    This function receives name of the topic in which we have to search
    and fetch data. This function will renders a page having information of a
    particular person which we have entered in the previous page form.

    Arguments :
    1. name : str (default=None)
        Name of person or object which we have entered in the previours form

    """
    if name:
        # This will returns particular wikepedia url page data
        page = requests.get(f"https://www.wikipedia.org/wiki/{name}")
    # Creating BeautifulSoup object by passing page.content and getting in
    # html parser
    soup = BeautifulSoup(page.content, 'html.parser')
    # Asigning title of wikepedia title
    title = soup.title.text

    # Looping the images of beautifulsoup object
    for img in soup.find_all('img'):
        if img['width'] >= '220':  # If img width is in specified width
            image = img['src']
            break # when one image width will get loop will break

    paragraph_data = ''
    # Looping the paragraph of a beautifulsoup object
    for para in soup.find_all('p'):
        # If the paragraph contains the specified length of text
        if len(para.get_text()) >= 200:
            paragraph_data = para.get_text() # Assigns paragraph data
            break

    unordered_index_list = [content for content in list(soup.find_all('ul')[3]) if content != '\n']
    index_data_list = []
    # Looping the ordered list from unordered list
    for unordered_list in unordered_index_list:
        for anchor_list in unordered_list.find_all('a'):
            mylist = anchor_list.find_all('span')
            index_data_list.append({
                'num' : mylist[0].get_text(),
                'detail' : mylist[1].get_text(),
                'detail2' : mylist[1].get_text().replace(' ', '_')
            })

    if paragraph_data is not None: # If paragraph data is None
        context = {
            'title': title,
            'image': image,
            'data': paragraph_data,
            'content': index_data_list,
            'name': name
        }
    else:
        context = {
            'title' : title,
            'image' : image
        }
    return render(request, 'core/content.html', context)


class ContentLinkTextAPIView(APIView):
    """
    This APIView display content on the right hand side of the
    page asynchronously. Get request is called to display data
    on page.

    """
    def get(self, request): # pylint: disable=no-self-use
        """
        This method is called when user click on anchor tag of
        index content list.

        """
        # Retreives data for request.GET
        data = request.GET
        # Getting serialized from the request data
        serializer = ContentTextSerializer(data=data)
        if serializer.is_valid(raise_exception=True): # If serializer is valid
            name = data.get('name')
            detail = data.get('detail')
            detail2 = data.get('detail2')

        page = requests.get(f"https://www.wikipedia.org/wiki/{name}")
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id=detail2)
        content_list = [detail2, detail]
        heading = title.parent
        paragraph = heading.next_sibling
        while paragraph.name != 'h2':
            content_list.append(paragraph.get_text())
            paragraph = paragraph.next_sibling

        for _ in range(content_list.count('\n')):
            content_list.remove('\n')

        return Response(content_list, status = status.HTTP_200_OK)
