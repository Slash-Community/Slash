# Канал
<p>
    &emsp;Свежая информация по поводу моих проектов будет доступна на этом <a href="https://t.me/logbook_17">канале</a>.
</p>

# Новое
  - with для Connection, Operations(будет удобно, возможно)
  - теперь нужно передавать колонку для того чтобы задать условие для запроов (проверка типов колонок и входных данных)

```Python
from Slash.types_ import Table, Column, Text
from Slash.Core.core import Connection, SQLCnd


table = Table("testtableforcondition")
table.set_columns(Column(Text, "some_c"))

with Connection("Slash", "postgres", "root", "127.0.0.1", 5432) as conn:
    conn.create(table)

    print(SQLCnd.where([table.some_c, SQLCnd.EQ, Text("1")]))

```
<br>

```Python
from Slash.Core.operations_ import Operations
from Slash.types_ import Table, Column, Text
from Slash.Core.core import Connection


table = Table("some_table")
table.set_columns(Column(Text, "textcolumn"))

with Connection("Slash", "postgres", "root", "127.0.0.1", 5432) as conn:
    conn.create(table)

    with Operations(conn) as op:
        op.insert(table, ("textcolumn"), (Text("hello")))
        print(op.select(table, ("textcolumn")).get_data())

```


# Файлы
  - `Slash/types_.py` <p>Базовые типы, класс для валидации типов(за правилами)</p>
  - `Slash/Core/core.py` <p>Создание подключения, классы валидации, расширение SQL-запросов</p>
  - `Slash/Core/exeptions_.py` <p>Исключения</p>
  - `Slash/Core/operations_.py` <p>Операции с БД</p>

# Создание подключения
```Python
from Slash.Core.core import Connection

conn = Connection("Slash", "postgres", "root", "127.0.0.1", 5432)
```
  - `"Slash"` - имя базы данных<br>
  - `"postgres"` - имя пользователя<br>
  - `"root"` - пароль<br>
  - `"127.0.0.1"` - хост<br>
  - `5432` - порт<br>

### Доспупные параметры
  - dbname - имя бд
  - user - имя пользователя
  - password - пароль
  - host - хост
  - port - порт
  - logger - класс `Logger` (после каждого коммита будет инфо о статусе операции)

# Создать свои правили валидации
 ```Python
from Slash.types_ import Rules

class MyRules(Rules):
   def __init__(self):
       super().__init__()

# нормально работает валидация для строки и числа, всё остальное будет позже
myRules = MyRules()
myRules.new_rules(
   {
       "type_int"  : {
           "min" : 0,
           "max" : 1000,
           "valide_foo" : myRules.valid_int
       },
       "type_text" : {
           "length" : 100,
           "valide_foo" : myRules.valid_text
       },
       "type_bool" : {
           "symbols" : [True, False],
           "valide_foo" : myRules.valid_bool
       },
       "type_date" : {
           "current" : "{}.{}.{}",
           "valide_foo" : myRules.valid_date
       }
   }
)
 ```
  Данные проходят валидацию нескольких уровней.
  - проверка на валидность входных строк
  - проверка данных(за правилом) на валидность
  - проверка на валидность SQL-запроса

  Если данные не проходят один уровень, будет поднято исключения:
  - `SlashBadColumnNameError` - Неправильное имя колонки(содержание знаков пунктуации) => Проверка осуществляется в `core.py`
  - `SlashRulesError` - Несоответствие правилам => Проверка осуществляется в `types_.py`
  - `SlashPatternMismatch` - Несоответствие шаблонному SQL-запросов => Проверка осуществляется в `core.py`

## Методы
  - `get_rules` - получение правил по умочанию
  - `get_user_rules` - получение новых правил
  - `new_rules`  - создание новых правил (принимает словарь)
  - `Функции валидации`
    - valid_bool - проверка белевых значений
    - valid_date - проверка вормата даты
    - valid_hidden - проверка защищенного поля
    - valid_int - проверка целого числа
    - valid_text - проверка текста

# Операции

## Создать таблицу
```Python
from Slash.types_ import (
    Column, Table, Int, Text,
    Hidden, Date, Bool
)
from Slash.Core.core import Connection, Logger

log = Logger(__name__, __file__, redirect_error=True)

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432,
    logger=log
)

table = Table("testdoc1")
table.set_columns(
    Column(Date, "born"),
    Column(Bool, "man"),
    Column(Int, "age"),
    Column(Text, "name"),
    Column(Hidden, "password")
)

conn.create(table)
```

&emsp;`Table` принимает один параметр, это имя бд. Она будет создана если не существует.

&emsp;`.set_columns()` может принимать любое кол-во параметров, а именно `Columns()`

&emsp;`Columns` это класс для определения колонки. Принимает два параметра, а именно: тип, имя.

### Определить поля таблицы можно другим способом:
```Python
from Slash.types_ import (
    Column, Table, Int, Text,
    Hidden, Date, Bool, TableMeta
)
from Slash.Core.core import Connection, Logger

log = Logger(__name__, __file__, redirect_error=True)

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432,
    logger=log
)


class MyTable(Table, metaclass=TableMeta):
    born = Column(Date, None)
    man = Column(Bool, None)
    age = Column(Int, None)
    mame = Column(Text, None)
    password = Column(Hidden, None)

table = MyTable("testdoc1")

conn.create(table)
```



## Вставка данных
```Python
from Slash.types_ import Column, Table, Int, Text, Rules
from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations


class MyRules(Rules):
    def __init__(self):
        super().__init__()

myRules = MyRules()
myRules.new_rules(
    {
        "type_int"  : {
            "min" : 0,
            "max" : 2000,
            "valide_foo" : myRules.valid_int
        },
        "type_text" : {
            "length" : 100,
            "valide_foo" : myRules.valid_text
        },
        "type_bool" : {
            "symbols" : [True, False],
            "valide_foo" : myRules.valid_bool
        },
        "type_date" : {
            "current" : "{}.{}.{}",
            "valide_foo" : myRules.valid_date
        }
    }
)


conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
conn.create(table)

operations = Operations(conn)

operations.insert(table, ("age", "name"), (Int(1000), Text("Name2")), rules=myRules)
# или (но базовые правила сильно ограничены)
operations.insert(table, ("age", "name"), (Int(1000), Text("Name2"))) # SlashRulesError
```

&emsp;`Operation`, принимает один параметр и это подключение к бд. `Operation(conn).insert` принимает объект таблицы, имена колонок, данные. Также можно задать свои правила для валидации, передав методу `rules=объект правил`


## Обновление данных
```Python
from Slash.types_ import AutoField, Column, Table, Int, Text
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
conn.create(table)

Operations(conn).update(
    table,
    ("name", ),
    (Text("33"), ),
    SQLConditions.where(
        "age", SQLConditions.LE, "3"
    )
)
```
&emsp;`Operation(conn).update` принимает объект таблицы, имена колонок, новые значения. Для того чтобы задать условие, надо передать `SQLConditions.where`.


## Удаление данных
```Python
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

# удаление с условием
Operations(conn).delete(
    table, SQLConditions.where(
        "age", SQLConditions.LE, 100
    )
)

# удаление без условий
Operations(conn).delete(table.name)
```
&emsp;`Operation(conn).delet` принимает объект таблицы, и условие `SQLConditions.where`.

## Выборка данных
```Python
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

# выборка даннных за условем из сортировкой
print(
    Operations(conn).select(
        table,
        ("age", "name"),
        SQLConditions.where(
            "age", SQLConditions.EQ, 3,
            SQLConditions.order_by("age", desc="desc")   
        )
    )
)
```
&emsp;`Operation(conn).select` принимает объект таблицы, имена колонок, условие `SQLConditions.where`.

# PyPI
<a href="https://pypi.org/project/Slash92/1.1.1/">1.1.1 (alpha)</a><br>
<a href="https://pypi.org/project/Slash92/1.1.0/">1.1.0 (alpha)</a><hr>
<a href="https://pypi.org/project/Slash92/0.2.3/">0.2.3</a><br>
<a href="https://pypi.org/project/Slash92/0.2.1.0/">0.2.1.0</a><br>
<a href="https://pypi.org/project/Slash92/0.2.0/">0.2.0</a><br>
<a href="https://pypi.org/project/Slash92/0.1.9/">0.1.9</a><br>
<a href="https://pypi.org/project/Slash92/0.1.8/">0.1.8</a><br>
<a href="https://pypi.org/project/Slash92/0.1.7.0/">0.1.7.0</a><br>
<a href="https://pypi.org/project/Slash92/0.1.6/">0.1.6</a><br>
<a href="https://pypi.org/project/Slash92/0.1.5/">0.1.5</a><br>
<a href="https://pypi.org/project/Slash92/0.1.4/">0.1.4</a><br>
<a href="https://pypi.org/project/Slash92/0.1.3/">0.1.3</a><br>
<a href="https://pypi.org/project/Slash92/0.1.2/">0.1.2</a><br>
<a href="https://pypi.org/project/Slash92/0.1.1/">0.1.1</a><br>
<a href="https://pypi.org/project/Slash92/0.1.0/">0.1.0</a>

# Собрать .whl
    python setup.py bdist_wheel

# Установка через .whl
    pip install Slash92-1.1.1-py3-none-any.whl

# Установка через setup.py
    python setup.py install

# Собрать WinJsonConverter
<div id="WinJsonConverter"></div>
&emsp;Для начала cкопируйте исходник ORM
    
    git clone https://github.com/m-o-d-e-r/Slash.git
  &emsp;<s>Если вас у вас не появился синий экран</s> найдите файл `setup_for_cython.py`, он понадобится для сборки нашей динамической либы.
  Потом с помощью <s>древней</s> команды запустите компиляцию `utils_for_rules.pyx`(этот файл тусит в `Slash/utilities/`, надо чтобы он был в одной папке с `setup_for_cython.py` или изменить путь в `setup_for_cython.py`). В `Slash/utilities/` находится: исходник `WinJsonConverter` и уже скомпилирования его версия, это значит что вы можете не собирать этот модуль заново.

    python setup_for_cython.py build_ext --inplace

  &emsp;<s>Если с вашего монитора ничего не вылезло</s> можете смело перемещать файл с расширением .pyd в `Slash/utilities/`.<br><br><br>
  <b>!!!Важно!!!</b><br>
  
|  Можно  |       Нельзя       |
| ------- | ------------------ |
| Добавлять что-то новое   | Менять имя файла   |
| Гладить кота при сборке(+2 к удаче) | Пить томатный сок  |

&emsp;Если есть какие-то трудности в сборке пишите <a href="https://t.me/M_O_D_E_R">сюда</a>.


  <b>!!!Не сильно важно, но к сути!!!</b><br>
  `Windows` - .pyd<br>
  `Linux` - .so<br>
&emsp;Под каждую ось свое расширение, но питон всё понимает. + вы не будете импортировать эту либу напрямую, хотя конечно это возможно.


