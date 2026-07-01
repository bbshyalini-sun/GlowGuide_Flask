GET_SKIN_TYPES = """
SELECT *
FROM skin_type
ORDER BY skin_type_name;
"""

GET_SKIN_ISSUES = """
SELECT *
FROM skin_issue
ORDER BY issue_name;
"""

COUNT_PRODUCTS = """
SELECT COUNT(*) AS total
FROM product;
"""

COUNT_CATEGORIES = """
SELECT COUNT(*) AS total
FROM category;
"""

COUNT_SKIN_TYPES = """
SELECT COUNT(*) AS total
FROM skin_type;
"""

COUNT_SKIN_ISSUES = """
SELECT COUNT(*) AS total
FROM skin_issue;
"""