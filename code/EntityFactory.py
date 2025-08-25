from code.Background import Background


class EntityFactory:
    
    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        match entity_name:
            case 'menu_inicial':
                list_menu_inicial = []
                for i in range(5):
                    list_menu_inicial.append(Background(f'menu_inicial{i}', (0,0)))
                return list_menu_inicial