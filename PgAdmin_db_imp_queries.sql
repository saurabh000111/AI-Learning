SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'documents'
ORDER BY ordinal_position;

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'documents';

-- verify for the foregien key
SELECT
    conname,
    pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'documents'::regclass;
