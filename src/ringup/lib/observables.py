"""Utility classes for the observer pattern"""
class ObservableMixin:
    def __init__(self):
        self._observers = list()

    def _changed(self):
        self.notifyObservers()

    def registerObserver(self, observer):
        self._observers.append(observer)

    def removeObserver(self, observer):
        self.remove(observer)

    def notifyObservers(self):
        for observer in self._observers:
            observer.update()

class ObserverMixin:
    def update(self):
        self.load()
