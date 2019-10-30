import unittest
import datetime

from parser import Parser


class TestParser(unittest.TestCase):
    def subject(self):
        with open("tests/2019-10-24.html") as f:
            html_doc = f.read()
        return Parser(html_doc)

    def test_date(self):
        self.assertEquals(datetime.date(2019, 10, 22), self.subject().date())

    def test_transilien(self):
        expected = [
            ["transilien", "global", 81.2, None],
            ["transilien", "A", 86.6, None],
            ["transilien", "B", 80.1, None],
            ["transilien", "C", 80.1, None],
            ["transilien", "D", 66.0, None],
            ["transilien", "E", 90.9, None],
            ["transilien", "H", 89.2, None],
            ["transilien", "J", 83.2, None],
            ["transilien", "K", 92.9, None],
            ["transilien", "L", 94.6, None],
            ["transilien", "N", 75.1, None],
            ["transilien", "P", 85.9, None],
            ["transilien", "R", 83.5, None],
            ["transilien", "U", 81.9, None],
            ["transilien", "T4", None, "TRAVAUX"],
            ["transilien", "T11", 86.7, None],
        ]

        self.assertEquals(expected, self.subject().transilien())

    def test_ter(self):
        expected = [
            ["ter", "global", 88.6, None],
            ["ter", "Grand Est", 92.2, None],
            ["ter", "Nouvelle-Aquitaine", 93.3, None],
            ["ter", "Auvergne-Rhône-Alpes", 86.0, None],
            ["ter", "Bourgogne-Franche-Comté", 90.2, None],
            ["ter", "Bretagne", 92.4, None],
            ["ter", "Centre-Val de Loire", 84.8, None],
            ["ter", "Occitanie", 77.3, None],
            ["ter", "Hauts-de-France", 88.0, None],
            ["ter", "Normandie", 94.6, None],
            ["ter", "Pays de la Loire", 88.1, None],
            ["ter", "Provence-Alpes-Côte d'Azur", 84.6, None],
        ]

        self.assertEquals(expected, self.subject().ter())

    def test_tgv(self):
        expected = [
            ["tgv", "global", 78.6, None],
            ["tgv", "nord", 88.9, None],
            ["tgv", "est", 85.1, None],
            ["tgv", "atlantique", 69.6, None],
            ["tgv", "sudest", 79.5, None],
            ["tgv", "ouigo", 76.9, None],
            ["tgv", "europe", 83.6, None],
        ]

        self.assertEquals(expected, self.subject().tgv())

    def test_intercites(self):
        expected = [
            ["intercites", "global", 68.4, None],
            ["intercites", "Paris-Limoges-Toulouse", 55.0, None],
            ["intercites", "Paris-Clermont", 75.0, None],
            ["intercites", "Bordeaux-Marseille", 13.3, None],
            ["intercites", "Nantes-Bordeaux", 100.0, None],
            ["intercites", "Nantes-Lyon", None, "Grève sans préavis"],
            ["intercites", "Toulouse-Bayonne", 50.0, None],
            ["intercites", "Clermont-Béziers", 100.0, None],
            ["intercites", "Paris-Caen-Cherbourg Trouville/Deauville", 70.6, None],
            ["intercites", "Paris-Rouen-Le Havre", 83.0, None],
            ["intercites", "Paris-Granville", 60.0, None],
            ["intercites", "Caen-Le Mans-Tours", 75.0, None],
            ["intercites", "Paris-Toulouse-Latour De Carol/Cerbere/Rodez", 100.0, None],
            ["intercites", "Paris-Briançon", None, "Travaux sur la ligne"],
        ]

        self.assertEquals(expected, self.subject().intercites())

    def test_to_list(self):
        expected = [
            [datetime.date(2019, 10, 22), "transilien", "B", 80.1, None],
            [datetime.date(2019, 10, 22), "ter", "Occitanie", 77.3, None],
            [datetime.date(2019, 10, 22), "intercites", "global", 68.4, None],
            [datetime.date(2019, 10, 22), "tgv", "nord", 88.9, None],
        ]

        self.assertEquals(16 + 12 + 7 + 14, len(self.subject().to_list()))

        for line in expected:
            self.assertIn(line, self.subject().to_list())
