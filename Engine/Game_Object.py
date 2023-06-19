from Components import Game_Component

class Game_Object:
    
    def __init__(self) -> None:
        self._components = []
    
    def add_component(self, component :Game_Component) -> None:
        self._components.append(component)
    
    def update(self, delta_time :float):
        self.update_components()
    
    def update_components(self):
        for comp in self._components:
            comp.update()