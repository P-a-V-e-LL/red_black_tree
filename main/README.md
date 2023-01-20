# Red Black tree. 


Реализация алгоритма написана на Python 3.

> Девушка: Нарисуй дерево.
> Программист: (рисует бинарное дерево)
> Девушка: Нет, другое.
> Программист: Я и красно-черное дерево могу нарисовать.

# Свойства алгоритма
КЧД наследует все свойства от обычного бинарного дерева + :
  - Каждый узел окрашен либо в красный, либо в черный цвет (в структуре данных узла появляется дополнительное поле – бит цвета).
  - Корень окрашен в черный цвет.
  - Листья(так называемые NULL-узлы) окрашены в черный цвет.
  - Каждый красный узел должен иметь два черных дочерних узла. Нужно отметить, что у черного узла могут быть черные дочерние узлы. Красные узлы в качестве дочерних могут иметь только черные.
  -  Пути от узла к его листьям должны содержать одинаковое количество черных узлов(это черная высота).