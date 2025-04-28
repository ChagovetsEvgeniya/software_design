import graphviz
from graphviz import Digraph

def create_interaction_diagram():
    # Створення об'єкта діаграми
    diagram = Digraph(comment='Interaction Diagram')

    # Додавання учасників
    diagram.node('T', 'Trader')
    diagram.node('TS', 'Trading System')
    diagram.node('O', 'Order')
    diagram.node('SE', 'Stock Exchange')
    diagram.node('M', 'Module')

    # Додавання взаємодій між учасниками
    diagram.edge('T', 'TS', 'ЗапитПозики (сума, умови)')
    diagram.edge('TS', 'O', 'СтворитиБорг (сума, відсотки)')
    diagram.edge('O', 'SE', 'РезервуватиКошти()')
    diagram.edge('SE', 'T', 'НадатиПозиченіКошти()')
    diagram.edge('T', 'M', 'ПовернутиБорг (сума, відсотки)')
    diagram.edge('M', 'SE', 'ЗакритиБорг()')
    diagram.edge('SE', 'O', 'ОновитиСтатусБоргу()')

    # Виведення діаграми
    diagram.render('interaction_diagram', format='png', view=True)

def create_collaboration_diagram():
    # Створення об'єкта діаграми
    diagram = Digraph(comment='Collaboration Diagram')

    # Додавання учасників
    diagram.node('T', 'Trader')
    diagram.node('TS', 'Trading System')
    diagram.node('O', 'Order')
    diagram.node('SE', 'Stock Exchange')
    diagram.node('M', 'Module')

    # Додавання взаємодій
    diagram.edge('T', 'TS', 'ЗапитПозики (сума, умови)')
    diagram.edge('TS', 'O', 'СтворитиБорг (сума, відсотки)')
    diagram.edge('O', 'SE', 'РезервуватиКошти()')
    diagram.edge('SE', 'T', 'НадатиПозиченіКошти()')
    diagram.edge('T', 'M', 'ПовернутиБорг (сума, відсотки)')
    diagram.edge('M', 'SE', 'ЗакритиБорг()')
    diagram.edge('SE', 'O', 'ОновитиСтатусБоргу()')

    # Виведення діаграми
    diagram.render('collaboration_diagram', format='png', view=True)

# Виклик функцій для створення діаграм
create_interaction_diagram()
create_collaboration_diagram()