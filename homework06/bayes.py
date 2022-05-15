import typing as tp
from collections import defaultdict
from math import log
from statistics import mean


class NaiveBayesClassifier:
    def __init__(self, a: float = 1e-5) -> None:
        self.d = 0
        self.words_number: tp.Dict[str, int] = defaultdict(int)
        self.classify_w: tp.Dict[tp.Tuple[str, str], int] = defaultdict(int)
        self.class1: dict[str, float] = defaultdict(int)  # type: ignore
        self.a = a

    def fit(self, x: tp.List[str], y: tp.List[str]) -> None:
        """Fit Naive Bayes classifier according to titles, labels."""

        for x_el, y_el in zip(x, y):  # проход через х и у
            self.class1[y_el] += 1
            for slovo in x_el.split():
                self.words_number[slovo] += 1
                self.classify_w[slovo, y_el] += 1

        for cl in self.class1:
            self.class1[cl] /= len(x)

        self.d = len(self.words_number)

    def logar(self, cls: str, slovo: str) -> float:
        """Calculate log of probability of P(Wi|C)"""
        return log(
            (self.classify_w[slovo, cls] + self.a) / (self.words_number[slovo] + self.a * self.d)
        )

    def class_probability(self, cls: str, feature: str) -> float:
        """Calculate log of probability"""
        return log(self.class1[cls]) + sum(self.logar(cls, w) for w in feature.split())

    def predict(self, feature: str) -> str:
        """Perform classification for one feature."""
        assert len(self.class1) > 0
        return str(max(self.class1.keys(), key=lambda c: self.class_probability(c, feature)))

    def get_predictions(self, X: tp.List[str]) -> tp.List[str]:
        """Perform classification on an array of test vectors X."""
        return [self.predict(feature) for feature in X]

    def score(self, X: tp.List[str], y: tp.List[str]) -> float:  # средняя точность
        """Returns the mean accuracy on the given test data and labels."""
        predicted = self.get_predictions(X)
        return mean(pred == actual for pred, actual in zip(predicted, y))
