INSERT INTO CONSULTAS (
    NAME,
    INDICATOR,
    DATE_QUERY,
    VALUE,
    SOURCE
) VALUES (
    'DEMO',
    'UF',
    TO_DATE('2025-12-25','YYYY-MM-DD'),
    37500,
    'mindicador.cl'
);

COMMIT;
