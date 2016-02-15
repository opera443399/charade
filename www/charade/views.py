# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-15
# @ pc
###################################

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
import time

from .models import Vocabulary, GameTemporaryTable, GameScoreBoard


# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse('charade:game_ready'))


def game_ready(request):
    """"ready to go."""
    return render(request, 'charade/ready.html')


def game_set(request):
    """
        crate new board in GameScoreBoard(gsb).
        generate GameTemporaryTable(gtt).
    """
    try:
        amount = int(request.POST['amount'])
    except (KeyError, ValueError):
        #msgs = "[ERROR] Set the number before you can play."
        #print msgs
        return HttpResponseRedirect(reverse('charade:game_ready'))
    else:
        GameTemporaryTable.objects.all().delete()
        random_word_list = Vocabulary.objects.order_by('?')[:amount]
        new_board = GameScoreBoard.objects.create(amount=amount)
        gsb = GameScoreBoard.objects.get(pk=new_board.id)
        for w in random_word_list:
            gsb.gametemporarytable_set.create(en=w.en, zh=w.zh, exp=w.exp, vid=w.id)

        return HttpResponseRedirect(reverse('charade:game_play', args=(new_board.id,)))


def game_play(request, board_id):
    """
        fetch unused word one at a time.
        update scores info in GameScoreBoard(gsb) when game over.
    """
    gsb = get_object_or_404(GameScoreBoard, pk=board_id)
    unused_word_list = gsb.gametemporarytable_set.exclude(used=1).order_by('?')[:1]
    if unused_word_list:
        context = {'word_list': unused_word_list}
    else:
        sum_scores = 0
        used_word_list = gsb.gametemporarytable_set.filter(used=1)
        for w in used_word_list:
            sum_scores += w.scores
        gsb.scores = sum_scores
        gsb.dt_end = timezone.now()
        gsb.save()
        msgs = 'team: {0}, number of words: {1}, scores: {2}'.format(board_id, gsb.amount, sum_scores)
        context = {'msgs': msgs,
                   'used_word_list': used_word_list,
                    }
    return render(request, 'charade/play.html', context)


def game_score(request, wid):
    """
        score the word.
        fetch next word from GameTemporaryTable(gtt).
    """
    gtt = get_object_or_404(GameTemporaryTable, pk=wid)
    try:
        s = int(request.POST['scores'])
    except (KeyError):
        # Redisplay the form.
        tmp_word_list = [gtt]
        return render(request, 'charade/play.html', {
            'word_list': tmp_word_list,
            'msgs': "You didn't select a choice.",
        })
    else:
        gtt.scores = s
        gtt.used = 1
        gtt.save()
        return HttpResponseRedirect(reverse('charade:game_play', args=(gtt.board_id,)))
    

@login_required
def game_board(request):
    """
        show the scores board.
        login is required.
    """
    game_score_board = GameScoreBoard.objects.order_by('-dt_start')
    ## pagenation: show 5 rows per page
    paginator = Paginator(game_score_board, 5)
    page = request.GET.get('page')
    try:
        board = paginator.page(page)
    except PageNotAnInteger:
        board = paginator.page(1)
    except EmptyPage:
        board = paginator.page(paginator.num_pages)
    context = {'board': board}

    return render(request, 'charade/board.html', context)


class Explanation(generic.DetailView):
    """Word Explanation"""
    model = Vocabulary
    template_name = 'charade/explanation.html'


################################################### test use only.


def show_time(request):
    """test ajax"""
    now = time.strftime('%H:%M:%S')
    return JsonResponse({'now': now}) 


@cache_page(60 * 15)
def show_about(request):
    """test cache"""
    return render(request, 'charade/about.html')
    

def show_meta(request):
    """test use only"""
    metas = request.META.items()
    metas.sort()
    print 'test meta: {0}'.format(metas)
    html = []
    for k,v in metas:
        html.append('<tr><td>{0}</td><td>{1}</td></tr>'.format(k,v))
    content = '<table>{0}</table>'.format('\n'.join(html))
    return HttpResponse(content)
