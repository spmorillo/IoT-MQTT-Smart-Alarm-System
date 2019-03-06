from state import State

# Start of our states
class Apagado(State):
    """
    Estado apagado definicion de transiciones
    """

    def on_event(self, event):
        if event == 'Encendido':
            return Encendido()

        return self


class Encendido(State):
    """
    Estado encendido definicion de transiciones
    """

    def on_event(self, event):
        if event == 'Apagado':
            return Apagado()
        elif event == 'Activado':
            return Activado()

        return self

class Activado(State):
    """
    Estado encendido definicion de transiciones 
    """

    def on_event(self, event):
        if event == 'Apagado':
            return Apagado()

        return self


# End of our states.