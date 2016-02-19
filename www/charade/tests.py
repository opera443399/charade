# -*- coding: utf-8 -*-
###################################
# @ Django 1.9.1
# @ 2016-02-16
# @ pc
###################################

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

import datetime
from .models import Vocabulary

# Create your tests here.

########################################################### test models
class VocabularyMethodTests(TestCase):
    def test_was_added_recently_with_future_word(self):
        """
        was_added_recently() should return False for word added in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_word = Vocabulary(dt=time)
        self.assertEqual(future_word.was_added_recently(), False)

    def test_was_added_recently_with_old_word(self):
        """
        was_added_recently() should return False for word added in the future.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_word = Vocabulary(dt=time)
        self.assertEqual(old_word.was_added_recently(), False)

    def test_was_added_recently_with_recent_word(self):
        """
        was_added_recently() should return False for word added in the future.
        """
        time = timezone.now() - datetime.timedelta(hours=5)
        recent_word = Vocabulary(dt=time)
        self.assertEqual(recent_word.was_added_recently(), True)



########################################################### test views
def create_word(en):
    """
    create a word
    """
    han = "中文 {0}".format(en)
    return Vocabulary.objects.create(en=en, zh=han, exp=han)

class VocabularyViewTests(TestCase):
    def test_index_view(self):
        """
        index --01
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_game_ready_view_default(self):
        """
        game_ready --01
        """
        response = self.client.get(reverse('charade:game_ready'))     
        self.assertEqual(response.status_code, 200)

    def test_game_set_view_word_number_not_set(self):
        """
        game_set --01
        """    
        response = self.client.get(reverse('charade:game_set'))
        self.assertEqual(response.status_code, 302)

    def test_game_set_view_word_number_set(self):
        """
        game_set --02
        """   
        num_of_words = 3
        response = self.client.post(reverse('charade:game_set'), 
                                    {'amount': num_of_words,})
        self.assertEqual(response.status_code, 302)

    def test_game_play_view_board_id_not_exist(self):
        """
        game_play --01
        """    
        board_id = 10
        response = self.client.get(reverse('charade:game_play', args=(board_id,)))
        self.assertEqual(response.status_code, 404)

    def test_game_play_view_board_id_exist(self):
        """
        game_play --02
        """    
        create_word('a')
        create_word('b')
        create_word('c')
        num_of_words = 3
        self.client.post(reverse('charade:game_set'), {'amount': num_of_words,})
        board_id = 1
        response = self.client.get(reverse('charade:game_play', args=(board_id,)))
        self.assertContains(response, "points", status_code=200)

    def test_game_score_view_word_id_not_exist(self):
        """
        game_score --01
        """
        word_id = 101    
        scores = 2
        response = self.client.post(reverse('charade:game_score', args=(word_id,)),
                                            {'scores': scores,})
        self.assertEqual(response.status_code, 404)

    def test_game_score_view_word_id_exist(self):
        """
        game_score --02
        """
        create_word('a')
        create_word('b')
        create_word('c')
        num_of_words = 3
        self.client.post(reverse('charade:game_set'), {'amount': num_of_words,})
        word_id = 2
        scores = 2
        response = self.client.post(reverse('charade:game_score', args=(word_id,)),
                                            {'scores': scores,})
        self.assertEqual(response.status_code, 302)

    def test_game_board_view_user_not_login(self):
        """
        game_board --01
        """    
        response = self.client.get(reverse('charade:game_board'), follow=True)
        self.assertContains(response, "Authantication System", status_code=200)

    def test_explanation_view_word_id_not_exist(self):
        """
        explanation --01
        """    
        word_id = 101    
        response = self.client.get(reverse('charade:explanation', args=(word_id,)))
        self.assertEqual(response.status_code, 404)

    def test_explanation_view_word_id_exist(self):
        """
        explanation --02
        """
        create_word('a')
        num_of_words = 1
        self.client.post(reverse('charade:game_set'), {'amount': num_of_words,})
        word_id = 1
        response = self.client.get(reverse('charade:explanation', args=(word_id,)))
        self.assertContains(response, "Explanation", status_code=200)


########################################################### test details

