import datetime
import re

from bs4 import BeautifulSoup


class Parser(object):
    def __init__(self, html):
        super(Parser, self).__init__()
        self.content = BeautifulSoup(html, "html.parser")

    def to_list(self):
        res = []
        for method in ["transilien", "ter", "tgv", "intercites"]:
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
            raise ValueError(value)
        value = matches[0].replace(",", ".")
        return float(value)

    def extract_item(self, item, mode, title_attr):
        name = item.attrs[title_attr]
        if name == "global" or name == "":
            name = "global"
        return [mode, name, self.clean_percentage(item.text)]

    def filter_results(self, mode, tag, title_attr):
        return [
            self.extract_item(item, mode, title_attr)
            for item in self.content.find_all(tag, attrs={"data-activite": mode})
        ]

    def tgv(self):
        return self.filter_results("tgv", tag="span", title_attr="data-id")

    def transilien(self):
        return self.filter_results("transilien", tag="span", title_attr="data-id")

    def ter(self):
        ter_global = self.filter_results("ter", "span", "data-id")
        return ter_global + self.filter_results(
            "ter", tag="g", title_attr="data-original-title"
        )

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
        if len(values) != len(lines):
            raise ValueError(lines, values)
        return list(map(list, zip(["intercites"] * len(lines), lines, values)))
