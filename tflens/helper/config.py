MARKDOWN_PRINT_TABLE_OUTPUT = '''
|   provider   |        type         | mode |     name     | module |
|--------------|---------------------|------|--------------|--------|
| provider.aws | aws_caller_identity | data | current_user |  test  |
'''
DEFAULT_PRINT_TABLE_OUTPUT = '''
+--------------+---------------------+------+--------------+--------+
|   provider   |        type         | mode |     name     | module |
+--------------+---------------------+------+--------------+--------+
| provider.aws | aws_caller_identity | data | current_user |  test  |
+--------------+---------------------+------+--------------+--------+
'''
FILE_HTML_OUTPUT = '''
<table>
<thead>
<tr>
<th>provider</th>
<th>type</th>
<th>mode</th>
<th>name</th>
<th>module</th>
</tr>
</thead>
<tbody>
<tr>
<td>provider.aws</td>
<td>aws_caller_identity</td>
<td>data</td>
<td>current_user</td>
<td>test</td>
</tr>
</tbody>
</table>
'''