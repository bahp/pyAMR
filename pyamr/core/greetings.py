# Libraries


class Greetings:

    def greet(self, name):
        print("Greetings {0}".format(name))


class Hello(Greetings):

    def greet(self, name):
        print("Hello {0}!".format(name))


class Morning(Greetings):

    def greet(self, name):
        print("Morning {0}!".format(name))
