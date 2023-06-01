from unittest import TestCase
from app import app
from flask import session


class FlaskTests(TestCase):

    def setUp(self):
        """test conditions to set up before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def tearDown(self):
        """reinitialize states following every test"""

        with self.client.session_transaction() as sess:
            sess.clear()

    def test_app_launch(self):
        """make sure static and dynamic HTML are displaying correctly from session on load"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_plays'))

            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'<p>Score:', res.data)
            self.assertIn(b'Seconds Remaining:', res.data)

    def test_word_verification(self):
        """Make sure word verification and response are functional"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "Z", "D", "L", "A"], 
                                 ["A", "K", "M", "P", "F"], 
                                 ["C", "D", "E", "P", "L"], 
                                 ["G", "O", "N", "U", "R"], 
                                 ["F", "H", "B", "K", "S"]]
        
        res = self.client.get('/verify-word?word=mac')
        self.assertEqual(res.json['result'], 'ok')

        res = self.client.get('/verify-word?word=great')
        self.assertEqual(res.json['result'], 'not-on-board')

        res = self.client.get('/verify-word?word=sdslk')
        self.assertEqual(res.json['result'], 'not-word')

    def test_stats_update(self):
        """Make sure updated stats are fetched from session and displayed correctly"""

        with self.client.session_transaction() as sess:
            sess['highscore'] = 9
            sess['num_plays'] = 5
            
        res = self.client.get('/')
        expected_html = b'<p>High Score: <b>9</b> in 5 plays</p>'
        self.assertIn(expected_html, res.data)