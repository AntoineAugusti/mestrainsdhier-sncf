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

    def test_transilien_incidents(self):
        expected = [
            [
                "transilien",
                "A",
                [
                    "Panne d'un engin de travaux à Noisiel.",
                    "Panne de signalisation à Vincennes.",
                    "Malaise voyageur à Châtelet.",
                    "Présence de personne sur les voies à Auber.",
                ],
            ],
            ["transilien", "B", ["Grève sans préavis"]],
            [
                "transilien",
                "C",
                [
                    "Présence d'une personne sur les voies entre Porchefontaine et Viroflay Rive Gauche.",
                    "Panne de signalisation à Issy Val de Seine.",
                ],
            ],
            [
                "transilien",
                "D",
                [
                    "Panne de signalisation à St Denis.",
                    "Bagage abandonné dans un train à Pierrefitte.",
                    "Panne d'un aiguillage à Corbeil.",
                ],
            ],
            [
                "transilien",
                "E",
                [
                    "Panne d'un aiguillage à Vaires.",
                    "Malaise voyageur dans un train à Pantin.",
                ],
            ],
            [
                "transilien",
                "H",
                [
                    "Panne d'un train à Champ de Courses d'Enghien.",
                    "Panne de signalisation à Ermont Eaubonne.",
                ],
            ],
            [
                "transilien",
                "J",
                [
                    "Panne de signalisation à La Frette Montigny.",
                    "Signal d'alarme sans motif dans un train à Argenteuil.",
                ],
            ],
            ["transilien", "K", ["Malaise voyageur dans un train à Dammartin."]],
            ["transilien", "L", None],
            [
                "transilien",
                "N",
                [
                    "Présence d'une personne dans les voies entre Porchefontaine et Viroflay Rive Gauche."
                ],
            ],
            [
                "transilien",
                "P",
                [
                    "Prolongation des travaux à Nangis suite à la panne d'un train de travaux.",
                    "Malaise voyageur à Pantin.",
                ],
            ],
            [
                "transilien",
                "R",
                [
                    "Panne d'un aiguillage à Corbeil.",
                    "Prolongation des travaux à Montargis suite à la panne d'un train de travaux.",
                    "Attente du passage d'un train TER à Motereau.",
                ],
            ],
            [
                "transilien",
                "U",
                [
                    "Présence d'une personne sur les voies entre Porchefontaine et Viroflay Rive Gauche."
                ],
            ],
            ["transilien", "T4", ["Travaux jusqu'au lundi 3 novembre."]],
            [
                "transilien",
                "T11",
                ["Absence de conducteur et indisponibilité de rame."],
            ],
        ]

        self.assertEquals(expected, self.subject().transilien_incidents())

    def test_tgv_incidents(self):
        self.maxDiff = None
        expected = [
            ["tgv", "nord", None],
            ["tgv", "est", ["Colis suspect à Paris-Est (2 TGV impactés)."]],
            [
                "tgv",
                "atlantique",
                ["Incident caténaire à Courtalain (49 TGV impactés)."],
            ],
            [
                "tgv",
                "sudest",
                [
                    "Panne de signalisation au Châtelet (11 TGV impactés).",
                    "Dérangement d'installation à Montpellier (7 trains).",
                    "Accident de personne à Vic-Mireval (7 TGV impactés).",
                    "Foudre tombée sur les installations électriques à Marseille (6 TGV impactés).",
                ],
            ],
            [
                "tgv",
                "ouigo",
                [
                    "Incident caténaire à Rouvray (4 OUIGO impactés).",
                    "Panne de signalisation au Châtelet (4 OUIGO impactés).",
                ],
            ],
            [
                "tgv",
                "europe",
                [
                    "Panne de signalisation au Châtelet (2 TGV impactés).",
                    "Accident de personne à Vic-Mireval (7 TGV impactés).",
                    "Foudre tombée sur les installations électriques à Marseille (6 TGV impactés).",
                ],
            ],
        ]

        self.assertEquals(expected, self.subject().tgv_incidents())

    def test_ter_incidents(self):
        self.maxDiff = None
        expected = [
            ["ter", "Grand Est", None],
            ["ter", "Nouvelle-Aquitaine", None],
            [
                "ter",
                "Auvergne-Rhône-Alpes",
                [
                    "Ralentissements suite à des travaux à Lentilly-Charpenay (26 TER "
                    "impactés).",
                    "Perte de la télécommande d'un poste suite à un problème sur le câble "
                    "télécom entre St-Romain-en-Gier et Givors (22 trains impactes)",
                ],
            ],
            [
                "ter",
                "Bourgogne-Franche-Comté",
                [
                    "Restitution tardive de travaux à Montargis (10 TER impactés).",
                    "Panne de signalisation à Paris-sud-Est (6 TER impactés).",
                ],
            ],
            ["ter", "Bretagne", ["Panne d'un train à Pontchaillou (13 TER impactés)."]],
            [
                "ter",
                "Centre-Val de Loire",
                [
                    "Ralentissement des trains suite à un brouillard épais en plaine de Beauce "
                    "(9 TER impactés).",
                    "Incident caténaire à Rouvray (5 TER impactés).",
                ],
            ],
            [
                "ter",
                "Occitanie",
                [
                    "Accident de personne à Frontignan (18 TER impactés).",
                    "Ralentissements suite à des travaux à Montpellier-St-Roch (10 TER "
                    "impactés).",
                ],
            ],
            [
                "ter",
                "Hauts-de-France",
                [
                    "Panne d'un train à Paris-Nord (21 TER impactés).",
                    "Forte affluence de voyageurs en gare de Longueau (8 TER impactés).",
                ],
            ],
            ["ter", "Normandie", None],
            ["ter", "Pays de la Loire", None],
            [
                "ter",
                "Provence-Alpes-Côte d'Azur",
                [
                    "Ralentissements suite à des travaux à Bandol (36 TER impactés).",
                    "Incident caténaire à Abeille suite aux intempéries (28 TER impactés).",
                ],
            ],
        ]

        self.assertEquals(expected, self.subject().ter_incidents())

    def test_intercites_incidents(self):
        self.maxDiff = None
        expected = [
            [
                "intercites",
                "Paris-Limoges-Toulouse",
                [
                    "Panne d'un train à Paris-Austerlitz.",
                    "Heurt de chèvres entre La Souterraine et Argenton sur Creuse.",
                    "Panne d'un aiguillage à Toury.",
                ],
            ],
            [
                "intercites",
                "Paris-Clermont",
                ["Travaux sur la voie restitués tardivement entre Montargis et Cosne."],
            ],
            [
                "intercites",
                "Bordeaux-Marseille",
                [
                    "Accident de personne à Vic-Mireval.",
                    "Foudre tombée sur les installations électriques à Marseille.",
                ],
            ],
            ["intercites", "Nantes-Bordeaux", None],
            ["intercites", "Nantes-Lyon", ["Grève sans préavis : aucune circulation."]],
            [
                "intercites",
                "Toulouse-Bayonne",
                ["Panne sur un train de marchandises à Montréjeau."],
            ],
            ["intercites", "Clermont-Béziers", None],
            [
                "intercites",
                "Paris-Caen-Cherbourg Trouville/Deauville",
                ["Mises à disposition retardées de matériels à Paris St Lazare."],
            ],
            ["intercites", "Paris-Rouen-Le Havre", None],
            [
                "intercites",
                "Paris-Granville",
                ["Panne sur un passage à niveau près d'Argentan."],
            ],
            [
                "intercites",
                "Caen-Le Mans-Tours",
                [
                    "Arrêts supplémentaires commerciaux accordés suite à la poursuite de la "
                    "grève sans préavis sur la région Pays de Loire."
                ],
            ],
            ["intercites", "Paris-Toulouse-Latour De Carol/Cerbere/Rodez", None],
            [
                "intercites",
                "Paris-Briançon",
                ["Travaux de modernisation des voies : aucune circulation."],
            ],
        ]
        self.assertEquals(expected, self.subject().intercites_incidents())

    def test_incidents(self):
        incidents = self.subject().incidents()
        self.assertEquals(16 + 12 + 7 + 14 - 4, len(incidents))

        tests = [
            [
                datetime.date(2019, 10, 22),
                "transilien",
                "H",
                [
                    "Panne d'un train à Champ de Courses d'Enghien.",
                    "Panne de signalisation à Ermont Eaubonne.",
                ],
            ],
            [
                datetime.date(2019, 10, 22),
                "tgv",
                "est",
                ["Colis suspect à Paris-Est (2 TGV impactés)."],
            ],
            [datetime.date(2019, 10, 22), "ter", "Grand Est", None],
            [datetime.date(2019, 10, 22), "intercites", "Clermont-Béziers", None],
        ]
        for test in tests:
            self.assertIn(test, incidents)
