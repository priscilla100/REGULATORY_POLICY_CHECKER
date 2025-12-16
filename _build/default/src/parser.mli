
(* The type of tokens. *)

type token = 
  | YESTERDAY
  | XOR
  | VERSION
  | UNTIL
  | TYPE_DECL_START
  | TYPE_DECL_ENDS
  | TYPE
  | TRUE
  | STRING of (string)
  | SINCE
  | SEMICOLON
  | RPAREN
  | REGULATION
  | RBRACKET
  | POLICY_START
  | POLICY_END
  | OR
  | ONCE
  | NOTEQUALS
  | NOT
  | NEXT
  | LPAREN
  | LESSEQ
  | LESS
  | LBRACKET
  | INT of (int)
  | IMPLIES
  | IFF
  | ID of (string)
  | HISTORICALLY
  | GREATEREQ
  | GREATER
  | FORALL
  | FALSE
  | EXISTS
  | EVENTUALLY
  | EQUALS
  | EOF
  | EFFECTIVE_DATE
  | DOT
  | CONST of (string)
  | COMMA
  | AT_LBRACKET
  | AND
  | ALWAYS

(* This exception is raised by the monolithic API functions. *)

exception Error

(* The monolithic API. *)

val main: (Lexing.lexbuf -> token) -> Lexing.lexbuf -> (Ast.policy_file)
