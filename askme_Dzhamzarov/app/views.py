import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.

questions = []
for i in range(1,131):
  questions.append({
    'title': 'Title ' + str(i),
    'id': i,
    'text': 'text for ' + str(i),
    'tags': [
        {
            'text': f'tag{(i%10)}',
            'id': 'tag' + str((i%10))
        },
        {
            'text': f'tag{(i%10)+1}',
            'id': 'tag' + str((i%10)+1)
        }
    ]
  })
tags = []
for q in range(0, 10):
  tags.append({
      'id': 'tag' + str(q),
      'text': 'tag' + str(q)
  })

def get_questions_by_tag(list1, tag_id):
    result = []
    for quest in list1:
        if quest['tags'] != 0:
            for tag in quest['tags']:
                if tag['id'] == tag_id:
                    result.append(quest)
                    break
    return result

def paginate(object_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    try:
        if page_num is None:
            page_num = 1
        paginator = Paginator(object_list, per_page=per_page)
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

def index(request):
    page = paginate(questions, request, 20)
    return render(
        request, template_name='index.html',
        context={'questions': page.object_list, 'page_obj': page, 'tags': tags}
    )

def hot(request):
    hot_questions = copy.deepcopy(questions)
    hot_questions.reverse()
    page = paginate(hot_questions, request, 20)
    return render(
        request, template_name='hot_questions.html',
        context={'questions': page.object_list, 'page_obj': page, 'tags': tags}
    )

def question(request, question_id):
    requestions = []
    for j in range(1, 121):
        requestions.append({
            'text': 'text for ' + str(question_id) + " " + str(j)
        })
    page = paginate(requestions, request, 30)
    one_question = questions[question_id-1]
    return render(
        request, template_name='one_question.html',
        context={'item': one_question, 'requestions' : page.object_list, 'page_obj': page, 'tags': tags}
    )

def ask(request):
    return render(request, template_name='ask.html')

def signup(request):
    return render(request, template_name='signup.html')

def login(request):
    return render(request, template_name='login.html')

def settings(request):
    return render(request, template_name='settings.html')

def tags(request, tag_id):
    tag_list = get_questions_by_tag(questions, tag_id)
    page = paginate(tag_list, request, 20)
    return render(
        request, template_name='tags.html',
        context={'questions': page.object_list, 'page_obj': page, 'tag_id': tag_id}
    )

