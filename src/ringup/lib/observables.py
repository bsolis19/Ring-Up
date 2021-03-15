"""Utility classes for the observer pattern"""
class ObservableMixin:
    def __init__(self):
        self.observers = list()

    def changed(self):
        self.notifyObservers()

    def registerObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update()

class ObserverMixin:
    def update(self):
        self.load()
