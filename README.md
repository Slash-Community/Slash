# Зворотній зв'язок
<a href="https://t.me/Slash_Community_bot">Бот для відгуків</a>

# Важливо
ORM буде переходити на Python 3.10

# Нове
  - Новий синтаксис для створення об'єднаних таблиць `UnitedTable`.
    - Раніше: `TablesManager.unite(table1, table2)`
    - Зараз: `table = table1 | table2`, насправді викликається метод `unite` з `TablesManager`, але на мою думку такий синтаксис більш привабливий.
  - Новий синтаксис для додавання компонентів до таблиць (для того, щоб більше не виконувати `Operations(conn)...`, можна додати об'єкт операцій до об'єкту таблиці). Синтаксис: `об'єкт таблиці << об'єкт операцій`. Для того щоб виконати операцію з базою даних, можна звертатися до об'єкту операцій через атрибут `op`. За умовчуванням це None, я це зробив для того, щоб лінтери не сварилися на те, що такого атрибуту немає (так як лінтери сканують код не під час його виконання, то цей атрибут був би недоступний на думку лінтера).

    ```Python
    from Slash.Core.core import Connection, Table, Column
    from Slash.Core.operations_ import Operations
    from Slash.types_ import Int

    conn = Connection(
        "Slash", "postgres", "root", "127.0.0.1", 5432
    )

    table1 = Table("test")
    table1.set_columns(
        Column(Int, "testField")
    )
    conn.create(table1)

    table1 << Operations(conn) # або можна conn.create(table1, Operations)

    table1.op.insert(
        table1,
        [table1.testField],
        [Int(228)]
    )
    ```
    По суті `компоненти` і є нововведенням, вони просто роблять використання деяких речей більш зручним.
  - Новий синтаксис для додавання/видалення полів моделей.
    ```Python
        from Slash.types_ import Column, Table, TableMeta, Int
        from Slash.Core.operations_ import Operations
        from Slash.Core.core import Connection

        conn = Connection(
            "Slash",
            "postgres",
            "root",
            "127.0.0.1",
            5432
        )

        class Test(Table, metaclass=TableMeta):
            field1 = Column(Int, None)

        table = Test("test123")
        table << Operations(conn)

        conn.create(table)

        table + Column(Int, "field2") # створення нової колонки в таблиці, якщо ядро міграцій увімкнено буде здійснено автоматичну міграцію.
    ```
    Всі зміни будуть відбуватися на рівні бази та ORM.<br>
    - `Створення нової колонки: ` об'єкт таблиці + об'єкт колонки<br>
    - `Видалення колонки: ` об'єкт таблиці - об'єкт колонки




# Файли
  - `Slash/types_.py` <p>Базові типи, клас для валідації типів(за правилами)</p>
  - `Slash/Core/core.py` <p>Створення підключення, класи валідації, розширення SQL-запитів</p>
  - `Slash/Core/exeptions_.py` <p>Виключення</p>
  - `Slash/Core/operations_.py` <p>Операції з БД</p>
  - `Slash/Core/migrate.py` <p>Ядро для міграцій</p>
  - `Slash/Core/migration_templates.py` <p>Шаблони для блоків міграції</p>

# Створення підключення
```Python
from Slash.Core.core import Connection

conn = Connection("Slash", "postgres", "root", "127.0.0.1", 5432)
```
  - `"Slash"` - ім'я бази даних<br>
  - `"postgres"` - ім'я користувача<br>
  - `"root"` - пароль<br>
  - `"127.0.0.1"` - хост<br>
  - `5432` - порт<br>

### Доступні параметри
  - dbname - ім'я бд
  - user - ім'я користувача
  - password - пароль
  - host - хост
  - port - порт
  - logger - клас `Logger` (після кожного commit буде інформація стосовно операції)

# Створення своїх правил валідації
```Python
from Slash.types_ import Rules

class MyRules(Rules):
   def __init__(self):
       super().__init__()

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
           "valide_foo" : myRules.valid_bool
       },
       "type_date" : {
           "current" : "{}.{}.{}",
           "valide_foo" : myRules.valid_date
       },
        "type_hidden": {
            "valide_foo": myRules.valid_hidden
        },
        "type_email": {
            "template": "^[a-zA-Z0-9\\-_\\.]*@[a-z\\.]*$",
            "valide_foo": myRules.valid_email
        },
        "type_phone": {
            "template": "\\+[0-9]*",
            "valide_foo": myRules.valid_phone
        },
        "type_ipv4": {
            "template": "[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}.[0-9]{1,3}",
            "valide_foo": myRules.valid_ipv4
        },
        "type_ipv6": {
            "template": "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$",
            "valide_foo": myRules.valid_ipv6
        },
        "type_url": {
            "template": "^https://[0-9a-zA-Z\\./\\-_&=]*$",
            "valide_foo": myRules.valid_url
        }
   }
)
```
  Данні проходять валідацію декількох рівнів.
  - перевірка вхідних даних на валідність(за правилом)
  - перевірка на валідність SQL-запитів

  Якщо данні не проходять один рівень, буде піднято виключення:
  - `SlashBadColumnNameError` - Неправильне ім'я колонки(містить знаки пунктуації) => Перевірка здійснюється в `core.py`
  - `SlashRulesError` - Невідповідність правилам => Перевірка здійснюється в `types_.py`
  - `SlashPatternMismatch` - Невідповідність шаблонному SQL-запиту => Перевірка здійснюється в `core.py`

## Методи
  - `get_rules` - отримання стандартних правил
  - `get_user_rules` - отримання користувацьких правил
  - `new_rules`  - створення нових правил (приймає словник)
  - `Функції валідації`
    - valid_int - перевірка цілого числа
    - valid_text - перевірка тесту
    - valid_bool - перевірка булевих значень
    - valid_date - перевірка формату дати
    - valid_hidden - перевірка захищеного поля
    - valid_email - перевірка формату ел. пошти
    - valid_phone - перевірка формату номеру телефону
    - valid_ipv4 - перевірка формату IPV4
    - valid_ipv6 - перевірка формату IPV6
    - valid_url - перевірка формату url

# Операції

## Створити таблицю
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

&emsp;`Table` приймає один параметр, це ім'я бд. Вона буде створена якщо не існує.
&emsp;`.set_columns()` може приймати необмежену кількість параметрів, а саме `Columns()`.
&emsp;`Columns` клас для задання колонки. Приймає два параметри, а саме: тип, ім'я.

## Створити поля таблиці можна іншим способом:
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
    name = Column(Text, None)
    password = Column(Hidden, None)

    __table__name__ = "test" # якщо вказати це поле, можна не передавати ім'я в конструктор

table = MyTable("testdoc1")

conn.create(table)
```

## Автоматичні міграції
```Python
from Slash.Core.migrate import MigrationCore # потрібно для міграцій
from Slash.Core.core import Connection, Logger
from Slash.types_ import (
    Table, TableMeta, Column,
    Int, Text, Bool, Hidden, Date
)

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)
conn.set_migration_engine(
    MigrationCore(
        os.path.dirname(__file__) + "/migrations",  # шлях до файлу міграції
        True                                        # показ повідомлень від ядра міграції (аналог режиму debug)
    )
)

class Books(Table, metaclass=TableMeta):
    author = Column(Text, None)    
    theme = Column(Text, None)
    pages = Column(Int, None)
    created = Column(Date, None)


books = Books("books")
conn.create(books)
```

## Приклад міграцій
```Json
{
    "version": "0.1.1",
    "count_of_blocks": 1,
    "last_hash": "4daf5d2dc979ad85eeae646d34b09df106680ef57778d6466f532307139df68a30c083f8a8065d9467e278075cc8d174c313c204dde5d5cc4754152130cea0df",
    "blocks": {
        "migration_0": {
            "is_first": true,
            "hash": "4daf5d2dc979ad85eeae646d34b09df106680ef57778d6466f532307139df68a30c083f8a8065d9467e278075cc8d174c313c204dde5d5cc4754152130cea0df",
            "table_count": 1,
            "tables": {
                "books228": [
                    [
                        "author",
                        "TEXT"
                    ],
                    [
                        "theme",
                        "TEXT"
                    ],
                    [
                        "pages",
                        "INT"
                    ],
                    [
                        "created",
                        "DATE"
                    ]
                ]
            }
        }
    }
}
```
&emsp; Структура файлу міграції
 - `version` - нинішня версія бази даних
 - `count_of_blocks` - кількість блоків міграції(фактично показує кількість змін)
 - `last_hash` - хеш останнього блоку міграції
 - `blocks` - складається з блоків міграцій
   - `migration_0` - блок міграції (містить інформацію стосовно таблиць)
     - `is_first` - прапорець який показує початковий блок міграції
     - `hash` - хеш блоку міграції
     - `table_count` - кількість таблиць(моделей)
     - `tables` - словник, ключами якого є ім'я таблиці(моделі), а значеннями сигнатура таблиць(моделей)
       - `books228` - ім'я таблиці(моделі)
         - `["author", "TEXT"]` - сигнатура одного поля містить ім'я поля та його тип

&emsp; Початковою версією БД буде 0.1.0 -> ({main}.{middle}.{min})
 - main - поки не змінюється
 - middle - змінюється при додаванні/видаленні нової таблиці(моделі)
 - min - змінюється при зміні кількості полів в однієї із таблиць (пізніше буде додана зміна версії при зміні типу поля)

:bangbang: Важливо :bangbang:
&emsp; Для того щоб міграції працювали, `зажди` потрібно писати `conn.create(table)`, так як саме останній такий запис буде запускати ядро міграції. Працює це через підрахунок прапорців об'єктів та класів моделей. Якщо їх кількість рівна, ядро працює, якщо ні ядро спить. В майбутньому цей алгоритм буде змінено.



## Вставка даних
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
        # і так далі
    }
)


conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
conn.create(table)

operations = Operations(conn)

operations.insert(
    table,
    (table.age, table.name),
    (Int(1000), Text("Name2")),
    rules=myRules
)
operations.insert(
    table,
    (table.age, table.name),
    (Int(1000), Text("Name2"))
) # SlashRulesError
```

&emsp;`Operation`, приймає один параметр, це підключення до бд. `Operation(conn).insert` приймає об'єкт таблиці, імена колонок, дані. Також можна задати свої правила валідації, передавши методу `rules=об'єкт правил`


## Оновлення даних
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
    (table.name, ),
    (Text("33"), ),
    SQLConditions.where(
        [table.age, SQLConditions.LE, Int(3)]
    )
)
```
&emsp;`Operation(conn).update` приймає об'єкт таблиці, імена колонок, нові значення. Для того щоб задати умову, потрібно передати `SQLConditions.where`.


## Видалення даних
```Python
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

# видалення з умовою
Operations(conn).delete(
    table, SQLConditions.where(
        [table.age, SQLConditions.LE, Int(100)]
    )
)

# видалення без умов
Operations(conn).delete(table.name)
```
&emsp;`Operation(conn).delete` приймає об'єкт таблиці та умову `SQLConditions.where`.

## Вибірка даних
```Python
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

Operations(conn).select(
    table,
    [table.name],
    condition=SQLConditions.where(
        [table.age, SQLConditions.LE, Int(100)]
    )
)
```
&emsp;`Operation(conn).select` приймає об'єкт таблиці, імена колонок, умову `SQLConditions.where`.


# JOIN запити
```Python
from Slash.types_ import (
    Int, Text,
    Table, Column,
    TablesManager
)
from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations, SQLCnd


conn = Connection(
    "Slash",
    "postgres",
    "root",
    "127.0.0.1",
    5432
)


a = Table("a")
a.set_columns(Column(Int, "age"))

b = Table("b")
b.set_columns(Column(Text, "username"))

conn.create(a)
conn.create(b)

print(
    Operations(conn).inner_join(
        (a, b),
        (a.rowid, a.age, b.username),
        SQLCnd.where([a.rowid, SQLCnd.EQ, b.rowid])
    ).get_data()
)
```
<a href="https://upload.wikimedia.org/wikipedia/commons/9/9d/SQL_Joins.svg">Ось вам посилання щодо видів JOIN запитів</a>
 - `inner_join`
 - `full_join`
 - `full_not_same_join`
 - `left_join`
 - `left_not_r_join`
 - `right_join`
 - `right_not_l_join`




# PyPI
<span><a href="https://pypi.org/project/Slash92/1.5.2/">1.5.2 </a> May 02, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.5.1/">1.5.1 </a> May 01, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.5.0/">1.5.0 </a> Apr 21, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.3.1/">1.3.1 </a> Mar 14, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.3.0/">1.3.0 </a> Mar 13, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.2.0/">1.2.0 </a> Mar 5, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.1.2/">1.1.2 </a> Feb 23, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.1.1/">1.1.1 </a> Feb 15, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/1.1.0/">1.1.0 </a> Feb 15, 2022</span><hr>
<span><a href="https://pypi.org/project/Slash92/0.2.3/">0.2.3</a> Jan 21, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/0.2.1.0/">0.2.1.0</a> Jan 6, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/0.2.0/">0.2.0</a> Jan 4, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.9/">0.1.9</a> Jan 4, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.8/">0.1.8</a> Jan 2, 2022</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.7.0/">0.1.7.0</a> Dec 24, 2021<br>
<span><a href="https://pypi.org/project/Slash92/0.1.6/">0.1.6</a> Dec 21, 2021</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.5/">0.1.5</a> Dec 20, 2021</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.4/">0.1.4</a> Dec 18, 2021</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.3/">0.1.3</a> Dec 17, 2021</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.2/">0.1.2</a> Dec 16, 2021</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.1/">0.1.1</a> Dec 15, 2021</span><br>
<span><a href="https://pypi.org/project/Slash92/0.1.0/">0.1.0</a> Dec 13, 2021</span>

# Зібрати .whl
    python setup.py bdist_wheel

# Установка через .whl
    pip install Slash92-1.3.0-py3-none-any.whl

# Установка через setup.py
    python setup.py install

# Установка через pip
    pip install Slash92

# Зібрати WinJsonConverter
<div id="WinJsonConverter"></div>
&emsp;Для початку скопіюйте ORM `git clone https://github.com/m-o-d-e-r/Slash.git`
  &emsp;<s>Якщо у вас ще не з'явився синій екран</s> знайдіть файл `setup_for_cython.py`, він знадобиться для створення  нашої динамічної бібліотеки. Потім, за допомогою <s>древньої</s> команди, запустіть компіляцію `utils_for_rules.pyx`(цей фал тусується в `Slash/utilities/`, потрібно щоб він був в одній директорії з `setup_for_cython.py` або змінити шлях в `setup_for_cython.py`). В `Slash/utilities/` знаходиться: вихідний код `WinJsonConverter` і вже зібрана його версія, це значить, що ви можете використовувати цей клас без попередньої компіляції.
  python setup_for_cython.py build_ext --inplace

  &emsp;<s>Якщо з вашого пк нічого не вилізло</s> можете сміло переміщувати файл в .pyd в `Slash/utilities/`.<br><br><br>
  <b>!!!Важливо!!!</b><br>
  
|  Можна  |       Не можна       |
| ------- | ------------------ |
| Додавати щось нове   | Змінювати назву файлу |
| Гладити кота під час створення ліби(+2 до удачі) | Пити томатний сік |

&emsp;Якщо виникли якісь трудності під час компіляції пишіть <a href="https://t.me/M_O_D_E_R">сюди</a>.

