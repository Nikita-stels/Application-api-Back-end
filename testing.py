import unittest
from core_logic import Estimation, Board, Card
from app_in_bd import delete_card, delete_board, is_card, is_board, report
from flask import request
       
class TestEstimation(unittest.TestCase):

    def setUp(self):
        self.widget = Estimation(5, 'h')


    def test_math_num(self):
        self.assertEqual(self.widget.num, 5)
    
    def test_math_pars(self):
        self.assertEqual(self.widget.pars(), '5h')

    def test_math_pars_day(self):
        widget = Estimation(20, 'h')
        self.assertEqual(widget.pars(), '2d4h')

    def test_math_creat_day(self):
        widget = Estimation(5, 'd')
        self.assertEqual(widget.num, 40)

    def test_math_creat_pars_day(self):
        widget = Estimation(5, 'd')
        self.assertEqual(widget.pars(), '1w')

    def test_math_creat_week(self):
        widget = Estimation(5, 'w')
        self.assertEqual(widget.num, 200)

    def test_math_creat_pars_week(self):
        widget = Estimation(5, 'w')
        self.assertEqual(widget.pars(), '1m1w')

    def test_math_creat_month(self):
        widget = Estimation(5, 'm')
        self.assertEqual(widget.num, 800)

    def test_math_creat_pars_month(self):
        widget = Estimation(5, 'm')
        self.assertEqual(widget.pars(), '5m')
    

    def test_add_is_obj(self):
        widget1 = Estimation(2, 'h')
        widget2 = Estimation(2, 'h')
        widget3 = widget1 + widget2
        self.assertIsInstance(widget3, Estimation)

    def test_add_h(self):
        widget1 = Estimation(2, 'h')
        widget2 = Estimation(2, 'h')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '4h')
    
    def test_add_d(self):
        widget1 = Estimation(7, 'h')
        widget2 = Estimation(1, 'h')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '1d')

    def test_add_d_h(self):
        widget1 = Estimation(9, 'h')
        widget2 = Estimation(1, 'h')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '1d2h')
    
    def test_add_d_d(self):
        widget1 = Estimation(4, 'd')
        widget2 = Estimation(1, 'd')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '1w')
    
    def test_add_w_d(self):
        widget1 = Estimation(2, 'w')
        widget2 = Estimation(2, 'd')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '2w2d')
    
    def test_add_w_w(self):
        widget1 = Estimation(4, 'w')
        widget2 = Estimation(1, 'w')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '1m1w')
    
    def test_add_m_d(self):
        widget1 = Estimation(2, 'm')
        widget2 = Estimation(5, 'd')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '2m1w')

    def test_add_interesting(self):
        widget1 = Estimation(256, 'h')
        widget2 = Estimation(16, 'd')
        widget3 = widget1 + widget2
        self.assertEqual(widget3.pars(), '2m1w3d')


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.widget = Board('Bob', 'Доска Дизайнера 2', ['ToDo', 'InProgress', 'Done'])

    def test_atr_pars(self):
        self.assertAlmostEqual(self.widget.columns, 'ToDo,InProgress,Done')
    
    def test_create_from_dict(self):

        data = {
                "user_name": "Bob",
                "title": "Доска Дизайнера 2",
                "columns": [
                             "ToDo",
                             "InProgress",
                             "Done"
                ] }
        self.assertIsInstance(self.widget.create_from_dict(data), Board)

    def test_save_in_BD(self):
        self.assertEqual(self.widget.save_in_bd(), 'INSERT 0 1')

class TestCard(unittest.TestCase):
    def setUp(self):
        self.widget = Card('Bob', 'Painter',
                            'Доска Дизайнера 2', 'ToDo', 
                            'Необходимо развернуть базу данных PostgreSQL', 'Jeck', '8h', '1586613110.325977')

    def test_atr_pars(self):
        data = {
                "user_name": "Bob",
                "title": "Painter",
                "board": "Доска Дизайнера 2",
                "status": "ToDo",
                "description": "Необходимо развернуть базу данных PostgreSQL",
                "times": "1586613110.334104",
                "assignee": "Jon",
                "estimation": "8h"
                }
        self.assertIsInstance(Card.create_from_dict(data), Card)
    
    def test_save_in_BD(self):
        self.assertEqual(self.widget.save_in_bd(), 'INSERT 0 1')
    

class Test_func_app_in_bd(unittest.TestCase):

    def test_delete_card(self):
        widget = delete_card('Painter', 'Доска Дизайнера 2')
        self.assertEqual(widget, 'DELETE 1')

    def test_delete_board(self):
        widget = delete_board('Доска Дизайнера 2', 'Bob')
        self.assertEqual(widget, 'DELETE 1')

    def test_is_board(self):
        """ func is_board reverse """
        widget = is_board('Доска Дворника')
        self.assertFalse(widget)

    def test_is_card(self):
        """ func is_card reverse """
        widget = is_card('Кукуха','Доска Дизайнера')
        self.assertFalse(widget)

    def test_report(self):
        data = {
            "board": "Доска Дворника",
            "column": "Пойти",
            "assignee": "Karl"
            }
        widget = report(data)
        if widget:
            self.assertIsInstance(widget, list)


# from test_client import *

# class FlaskrTestCase(unittest.TestCase):
    
#     def setUp(self):
#         server.app.testing = True
#         self.app = server.app.test_client()
    
#     def test_info(self):
#         result = self.app.get('/api/v1/info')
#         self.assertEqual(result.data, b'This is api gives access to the task management application')

    # def tes_get_boards_list(self):
    #     result = self.app.get('/api/v1/board/list')
    #     print(result)
    #     self.assertEqual(result.data, b'qwe' )
 

    
if __name__ == '__main__':
    unittest.main()
