def get_relations_query(table_name):
    return "SELECT " \
           "OBJECT_NAME (FKEYS.REFERENCED_OBJECT_ID) REFERENCED_TABLE_NAME, " \
           "COL_NAME(FKEYS.PARENT_OBJECT_ID, FKEYS.PARENT_COLUMN_ID) REFERENCING_COLUMN_NAME, " \
           "COL_NAME(FKEYS.REFERENCED_OBJECT_ID, FKEYS.REFERENCED_COLUMN_ID) REFERENCED_COLUMN_NAME " \
           "FROM SYS.FOREIGN_KEY_COLUMNS AS FKEYS " \
           f"WHERE OBJECT_NAME(FKEYS.PARENT_OBJECT_ID) = '{table_name}'"


def get_primary_keys_query(table_name):
    return "SELECT " \
           "COL_NAME(INDEX_COLUMNS.OBJECT_ID, INDEX_COLUMNS.COLUMN_ID) AS COLUMN_NAME " \
           "FROM SYS.INDEXES AS INDEXES " \
           "INNER JOIN SYS.INDEX_COLUMNS AS INDEX_COLUMNS " \
           "ON INDEXES.OBJECT_ID = INDEX_COLUMNS.OBJECT_ID AND INDEXES.INDEX_ID = INDEX_COLUMNS.INDEX_ID " \
           f"WHERE INDEXES.IS_PRIMARY_KEY = 1 AND OBJECT_NAME(INDEX_COLUMNS.OBJECT_ID) = '{table_name}'"
