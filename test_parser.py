import unittest
import datetime

from main import Parser


class TestParser(unittest.TestCase):
    def subject(self):
        with open("tests/2019-10-24.html") as f:
            html_doc = f.read()
        return Parser(html_doc)

    def test_date(self):
        self.assertEquals(datetime.date(2019, 10, 22), self.subject().date())

    def test_transilien(self):
        expected = [
            ["transilien", "global", 81.2],
            ["transilien", "A", 86.6],
            ["transilien", "B", 80.1],
            ["transilien", "C", 80.1],
            ["transilien", "D", 66.0],
            ["transilien", "E", 90.9],
            ["transilien", "H", 89.2],
            ["transilien", "J", 83.2],
            ["transilien", "K", 92.9],
            ["transilien", "L", 94.6],
            ["transilien", "N", 75.1],
            ["transilien", "P", 85.9],
            ["transilien", "R", 83.5],
            ["transilien", "U", 81.9],
            ["transilien", "T4", None],
            ["transilien", "T11", 86.7],
        ]

        self.assertEquals(expected, self.subject().transilien())

    def test_ter(self):
        expected = [
            ["ter", "global", 88.6],
            ["ter", "Grand Est", 92.2],
            ["ter", "Nouvelle-Aquitaine", 93.3],
            ["ter", "Auvergne-Rhône-Alpes", 86.0],
            ["ter", "Bourgogne-Franche-Comté", 90.2],
            ["ter", "Bretagne", 92.4],
            ["ter", "Centre-Val de Loire", 84.8],
            ["ter", "Occitanie", 77.3],
            ["ter", "Hauts-de-France", 88.0],
            ["ter", "Normandie", 94.6],
            ["ter", "Pays de la Loire", 88.1],
            ["ter", "Provence-Alpes-Côte d'Azur", 84.6],
        ]

        self.assertEquals(expected, self.subject().ter())

    def test_tgv(self):
        expected = [
            ["tgv", "global", 78.6],
            ["tgv", "nord", 88.9],
            ["tgv", "est", 85.1],
            ["tgv", "atlantique", 69.6],
            ["tgv", "sudest", 79.5],
            ["tgv", "ouigo", 76.9],
            ["tgv", "europe", 83.6],
        ]

        self.assertEquals(expected, self.subject().tgv())

    def test_intercites(self):
        expected = [
            ["intercites", "global", 68.4],
            ["intercites", "Paris-Limoges-Toulouse", 55.0],
            ["intercites", "Paris-Clermont", 75.0],
            ["intercites", "Bordeaux-Marseille", 13.3],
            ["intercites", "Nantes-Bordeaux", 100.0],
            ["intercites", "Nantes-Lyon", None],
            ["intercites", "Toulouse-Bayonne", 50.0],
            ["intercites", "Clermont-Béziers", 100.0],
            ["intercites", "Paris-Caen-Cherbourg Trouville/Deauville", 70.6],
            ["intercites", "Paris-Rouen-Le Havre", 83.0],
            ["intercites", "Paris-Granville", 60.0],
            ["intercites", "Caen-Le Mans-Tours", 75.0],
            ["intercites", "Paris-Toulouse-Latour De Carol/Cerbere/Rodez", 100.0],
            ["intercites", "Paris-Briançon", None],
        ]

        self.assertEquals(expected, self.subject().intercites())

    def test_to_list(self):
        expected = [
            [datetime.date(2019, 10, 22), "transilien", "B", 80.1],
            [datetime.date(2019, 10, 22), "ter", "Occitanie", 77.3],
            [datetime.date(2019, 10, 22), "intercites", "global", 68.4],
            [datetime.date(2019, 10, 22), "tgv", "nord", 88.9],
        ]

        self.assertEquals(16 + 12 + 7 + 14, len(self.subject().to_list()))

        for line in expected:
            self.assertIn(line, self.subject().to_list())
