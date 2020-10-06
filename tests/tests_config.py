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
VALID_TFSTATE_CONTENT_NO_RESOURCES = {
  'version': 4,
  'terraform_version': "0.12.18",
  'serial': 153,
  'lineage': "xxxxxx-xxxx-xxx-xxxx-xxxxxx",
  'outputs': {
    'test_output': {
      'value': 'test',
      'type': 'string'
    }
  },
  'resources': []
}
VALID_TFSTATE_CONTENT_WITH_RESOURCES = {
  'version': 4,
  'terraform_version': "0.12.18",
  'serial': 153,
  'lineage': "xxxxxx-xxxx-xxx-xxxx-xxxxxx",
  'outputs': {
    'test_output': {
      'value': 'test',
      'type': 'string'
    }
  },
  'resources': [
    {
      'module': 'module.test',
      'mode': 'data',
      'type': 'aws_caller_identity',
      'name': 'current_user',
      'provider': 'provider.aws',
      'instances': [
        {
          'schema_version': 0,
          'attributes': {
            'account_id': '123456789011',
            'arn': 'arn:aws:sts::123456789011:assumed-role/test/test_user_email',
            'id': '2020-02-20 22:10:40.720934 +0000 UTC',
            'user_id': 'XXXXXXXXXXXXX:test_user_email'
          }
        }
      ]
    },
    {
      'mode': 'managed',
      'type': 'aws_dynamodb_table',
      'name': 'dynamodb-terraform-state-lock',
      'provider': 'provider.aws',
      'instances': []
    }
  ]
}
NON_VALID_TFSTATE_CONTENT = {
  'version': 4,
  'terraform_version': "0.12.18",
  'serial': 153,
  'lineage': "xxxxxx-xxxx-xxx-xxxx-xxxxxx",
  'outputs': {
    'test_output': {
      'value': 'test',
      'type': 'string'
    }
  }
}
VALID_MODULE_RESOURCE = {
  'module': 'module.test',
  'mode': 'data',
  'type': 'aws_caller_identity',
  'name': 'current_user',
  'provider': 'provider.aws',
  'instances': []
}
VALID_NON_MODULE_RESOURCE = {
  'mode': 'managed',
  'type': 'aws_dynamodb_table',
  'name': 'dynamodb-terraform-state-lock',
  'provider': 'provider.aws',
  'instances': []
}
NON_VALID_RESOURCE = {
  'mode': 'managed',
  'name': 'dynamodb-terraform-state-lock',
  'provider': 'provider.aws',
  'instances': []
}
