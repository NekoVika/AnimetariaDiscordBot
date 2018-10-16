import unittest
import animebot.chess.main as main
import animebot.chess.pieces as pieces
import animebot.chess.helper as helper


class TestGame(unittest.TestCase):

    def test_game_init(self):
        g = main.ChessGame()

        self.assertIsInstance(g.field, main.ChessField)
        self.assertIsInstance(g.player1, main.ChessPlayer)
        self.assertIsInstance(g.player2, main.ChessPlayer)
        self.assertEqual(g.current_player, g.player1)

    def test_game_change_player(self):
        g = main.ChessGame()
        g.change_player()
        self.assertEqual(g.current_player, g.player2)

    def test_game_validate_move_true(self):
        g = main.ChessGame()
        self.assertTrue(g.validate_spelling(('a3', 'a5')))
        self.assertTrue(g.validate_spelling(('b4', 'b6')))
        self.assertTrue(g.validate_spelling(('c7', 'h6')))
        self.assertTrue(g.validate_spelling(('f4', 'a3')))

    def test_game_validate_move_false(self):
        g = main.ChessGame()
        self.assertFalse(g.validate_spelling(('a3', 't5')))
        self.assertFalse(g.validate_spelling(('b4', 'r6')))
        self.assertFalse(g.validate_spelling(('f4', 'f0')))
        self.assertFalse(g.validate_spelling(('f4', 'f9')))
        self.assertFalse(g.validate_spelling('asdasdasd'))
        self.assertFalse(g.validate_spelling('f1f2'))


class TestPieces(unittest.TestCase):
    field = None
    game = None

    def setUp(self):
        self.field = main.ChessField()
        self.game = main.ChessGame(self.field)

    def tearDown(self):
        self.field = None
        self.game = None

    def test_pawn_move_forward_freely(self):
        field = self.game.field
        field.init_piece('a1', self.game.player1, pieces.ChessPawn)
        pawn = self.game.field.get_by_id('a1').piece
        res = self.game.make_move(('a1', 'a2'))
        self.assertEqual(res['code'], 0)
        self.assertEqual(self.game.field.get_by_id('a2').piece, pawn)


class TestHelperPoint(unittest.TestCase):

    def test_helper_point_init_empty(self):
        p = helper.Point()
        self.assertEqual(p.x, 0)
        self.assertEqual(p.y, 0)

    def test_helper_point_init_number(self):
        p = helper.Point(3)
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 3)

    def test_helper_point_init_two_numbers(self):
        p = helper.Point(3, 5)
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 5)

    def test_helper_point_bool_true(self):
        p = helper.Point(3, 5)
        self.assertTrue(p)
        p = helper.Point(0, 0)
        self.assertTrue(p)
        p = helper.Point(7, 5)
        self.assertTrue(p)

    def test_helper_point_bool_false(self):
        p = helper.Point(-3, 1)
        self.assertFalse(p)
        p = helper.Point(4, 14)
        self.assertFalse(p)
        p = helper.Point(9, 1)
        self.assertFalse(p)

    def test_helper_point_add(self):
        p1 = helper.Point(4, 1)
        p2 = helper.Point(2, 3)
        ps = p1 + p2
        self.assertEqual(ps.x, 6)
        self.assertEqual(ps.y, 4)

    def test_helper_point_mul(self):
        p1 = helper.Point(4, 1)
        p2 = helper.Point(2, 3)
        ps = p1 * p2
        self.assertEqual(ps.x, 8)
        self.assertEqual(ps.y, 3)

    def test_helper_point_eq_false(self):
        p1 = helper.Point(4, 1)
        p2 = helper.Point(2, 3)
        self.assertFalse(p1 == p2)

    def test_helper_point_eq_true(self):
        p1 = helper.Point(4, 3)
        p2 = helper.Point(4, 3)
        self.assertTrue(p1 == p2)

