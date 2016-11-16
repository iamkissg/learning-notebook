# File and Directory Access

## glob [src](https://hg.python.org/cpython/file/2.7/Lib/glob.py)

- 加上注释和空行，100 行
- `glob` - `return list(iglob(pathname))`
- `glob1` - 
- `has_magic` - 利用 `magic_check.search(s)` 验证是否带 `*？[]` 等

- 

## fnmatch [src](https://hg.python.org/cpython/file/2.7/Lib/fnmatch.py)

- 加注释和空行，120 行

```python
"""Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)
"""
```
- `fnmatch()` - 预处理 (`os.path.normcase()`) 后，调用了 `fnmatchcase()`
- `fnmatchcase()` - 调用了 `translate()`. 并用到 `_cache`
- `filter()` - 预处理同 `fnmatchcase()`, 最终还是利用的 `re.match()`
- `translate()` - PATTERN 转为 regex
