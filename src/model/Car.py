from attr import dataclass


@dataclass
class Car:
    '''Class for keeping track of an car.'''
    manufacturer: str
    model: str
    ref: str
    rok: str
    rodzaj_paliwa: str
    przebieg: str
    cena: str
    link: str

    def __str__(self):
        return f"{self.manufacturer} {self.model} ref: {self.ref}\nrok: {self.rok}, rodzaj paliwa: {self.rodzaj_paliwa}, przebieg: {self.przebieg}, cena: {self.cena}\n\n{self.link}"
