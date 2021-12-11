from Slash.types_ import Column, Table, Int, Text
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations



conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
table.create(conn)


Operations(conn).insert(table.get_name(), ("age", "name"), (Int(2), Text("1234")))

Operations(conn).update(
    table.get_name(),
    ("age", "name"),
    (Int(3), Text("333")),
    SQLConditions.where(
        "age", SQLConditions.LE, "3"
    )
)

print(
    Operations(conn).select(
        table.get_name(),
        ("age", "name")
    )
)


