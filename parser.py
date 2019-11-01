import datetime
import re

from bs4 import BeautifulSoup


class Parser(object):
    MODES = ["transilien", "ter", "tgv", "intercites"]

    def __init__(self, html):
        super(Parser, self).__init__()
        self.content = BeautifulSoup(html, "html.parser")

    def to_list(self):
        res = []
        for method in self.MODES:
            data = getattr(self, method)()
            res.extend([[self.date()] + e for e in data])
        return res

    def incidents(self):
        res = []
        for method in [f"{m}_incidents" for m in self.MODES]:
            data = getattr(self, method)()
            res.extend([[self.date()] + e for e in data])
        return res

    def date(self):
        title = self.content.title.text[-10:]
        return datetime.datetime.strptime(title, "%Y/%m/%d").date()

    def clean_percentage(self, value):
        matches = re.findall(r"(\d+(?:\.|,)*\d*)", value)
        if len(matches) == 0:
            return None
        if len(matches) > 1:
            raise ValueError(f"Multiple matches for {value}")
        value = matches[0].replace(",", ".")
        return float(value)

    def find_reason(self, value):
        percentage = self.clean_percentage(value)
        if percentage is None:
            return value
        return None

    def extract_item(self, item, mode, title_attr):
        name = item.attrs[title_attr]
        if name == "global" or name == "":
            name = "global"
        return [
            mode,
            name,
            self.clean_percentage(item.text),
            self.find_reason(item.text),
        ]

    def filter_results(self, mode, tag, title_attr):
        return [
            self.extract_item(item, mode, title_attr)
            for item in self.content.find_all(tag, attrs={"data-activite": mode})
        ]

    def find_incident(self, line, mode):
        if mode in ["transilien", "tgv"]:
            el = self.content.find(
                "div", class_="fait-du-jour", attrs={"data-id": line}
            )
        elif mode in ["ter", "intercites"]:
            el = self.content.find("span", class_="fait-du-jour-titre", string=line)
            if el is not None:
                el = el.parent
        else:
            raise ValueError(f"Unknow type {mode}")
        if el is None:
            return None
        ul = el.find("ul")
        if ul is not None:
            return [li.text.strip() for li in ul.findAll("li")]
        return [el.find("p").text.strip()]

    def find_incidents(self, mode):
        lines = [e[1] for e in getattr(self, mode)()]
        lines.remove("global")
        return [[mode, line, self.find_incident(line, mode)] for line in lines]

    def transilien_incidents(self):
        return self.find_incidents("transilien")

    def tgv_incidents(self):
        return self.find_incidents("tgv")

    def ter_incidents(self):
        return self.find_incidents("ter")

    def intercites_incidents(self):
        return self.find_incidents("intercites")

    def tgv(self):
        return self.filter_results("tgv", tag="span", title_attr="data-id")

    def transilien(self):
        return self.filter_results("transilien", tag="span", title_attr="data-id")

    def ter(self):
        ter_global = self.filter_results("ter", "span", "data-id")
        return ter_global + self.filter_results("ter", tag="g", title_attr="title")

    def intercites(self):
        lines = ["global"] + [
            item.get_text()
            for item in self.content.find_all(attrs={"class": ["legende-relation"]})
        ]
        values = [
            self.clean_percentage(item.get_text())
            for item in self.content.find_all(
                "span", attrs={"data-activite": "intercites"}
            )
        ]
        reasons = [
            self.find_reason(item.get_text())
            for item in self.content.find_all(
                "span", attrs={"data-activite": "intercites"}
            )
        ]
        if len(values) != len(lines) or len(reasons) != len(values):
            raise ValueError(
                f"Lists have different sizes: {str(values)}, {str(lines)}, {str(reasons)}"
            )
        return list(map(list, zip(["intercites"] * len(lines), lines, values, reasons)))
