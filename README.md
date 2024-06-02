learning parsing, for my blog post soon to be published at

https://blog.johnamata.com/articles/2024/06/02/brief-parser.html

parses this

```
let x = 5;
if (x > 3) {
    x = x + 1;
}
```

tokens are hardcoded

```tokens = [
    Token('KEYWORD', 'if'),
    Token('DELIMITER', '('),
    Token('IDENTIFIER', 'x'),
    Token('OPERATOR', '>'),
    Token('NUMBER', '3'),
    Token('DELIMITER', ')'),
    Token('DELIMITER', '{'),
    Token('IDENTIFIER', 'x'),
    Token('OPERATOR', '='),
    Token('IDENTIFIER', 'x'),
    Token('OPERATOR', '+'),
    Token('NUMBER', '1'),
    Token('DELIMITER', ';'),
    Token('DELIMITER', '}')
]
```

prints this AST

```
Block {
    statements: [
    LetStatement {
        identifier:         Identifier { name: x },
        value:         Number { value: 5 }
    },
    IfStatement {
        condition:         BinaryExpression {
            left:             Identifier { name: x },
            operator: >,
            right:             Number { value: 3 }
        },
        body:         Block {
            statements: [
            Assignment {
                identifier:                 Identifier { name: x },
                value:                 BinaryExpression {
                    left:                     Identifier { name: x },
                    operator: +,
                    right:                     Number { value: 1 }
                }
            }
            ]
        }
    }
    ]
}

```

recursive

```
parse_program
  └── parse_statement (let x = 5;)
        └── parse_let_statement
              └── parse_identifier
              └── parse_expression
                    └── parse_term
                          └── parse_number
  └── parse_statement (if (x > 3) { x = x + 1; })
        └── parse_if_statement
              └── parse_condition (parse_expression)
                    └── parse_expression
                          └── parse_term
                                └── parse_identifier
                          └── parse_term
                                └── parse_number
              └── parse_block
                    └── parse_statement (x = x + 1;)
                          └── parse_assignment
                                └── parse_identifier
                                └── parse_expression
                                      └── parse_term
                                            └── parse_identifier
                                      └── parse_term
                                            └── parse_number

```
