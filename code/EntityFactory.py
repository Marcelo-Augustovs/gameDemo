from code.Background import Background
from code.Const import WIN_WIDTH


class EntityFactory:
    
    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        match entity_name:
            case 'menu_inicial':
                list_menu_inicial = []
                for i in range(5):
                    list_menu_inicial.append(Background(f'menu_inicial{i}', position))
                    list_menu_inicial.append(Background(f'menu_inicial{i}', (WIN_WIDTH, 0)))
                return list_menu_inicial