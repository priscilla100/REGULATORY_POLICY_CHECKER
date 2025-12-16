
module MenhirBasics = struct
  
  exception Error
  
  let _eRR =
    fun _s ->
      raise Error
  
  type token = 
    | YESTERDAY
    | XOR
    | VERSION
    | UNTIL
    | TYPE_DECL_START
    | TYPE_DECL_ENDS
    | TYPE
    | TRUE
    | STRING of (
# 10 "src/parser.mly"
       (string)
# 23 "src/parser.ml"
  )
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
    | INT of (
# 7 "src/parser.mly"
       (int)
# 44 "src/parser.ml"
  )
    | IMPLIES
    | IFF
    | ID of (
# 9 "src/parser.mly"
       (string)
# 51 "src/parser.ml"
  )
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
    | CONST of (
# 8 "src/parser.mly"
       (string)
# 67 "src/parser.ml"
  )
    | COMMA
    | AT_LBRACKET
    | AND
    | ALWAYS
  
end

include MenhirBasics

# 3 "src/parser.mly"
   
    open Ast

# 82 "src/parser.ml"

type ('s, 'r) _menhir_state = 
  | MenhirState013 : ('s _menhir_cell0_option_regulation_metadata_, _menhir_box_main) _menhir_state
    (** State 013.
        Stack shape : option(regulation_metadata).
        Start symbol: main. *)

  | MenhirState015 : (('s, _menhir_box_main) _menhir_cell1_TYPE _menhir_cell0_ID, _menhir_box_main) _menhir_state
    (** State 015.
        Stack shape : TYPE ID.
        Start symbol: main. *)

  | MenhirState021 : ('s _menhir_cell0_option_regulation_metadata_ _menhir_cell0_option_type_declaration_section_, _menhir_box_main) _menhir_state
    (** State 021.
        Stack shape : option(regulation_metadata) option(type_declaration_section).
        Start symbol: main. *)

  | MenhirState022 : (('s, _menhir_box_main) _menhir_cell1_YESTERDAY, _menhir_box_main) _menhir_state
    (** State 022.
        Stack shape : YESTERDAY.
        Start symbol: main. *)

  | MenhirState029 : ((('s, _menhir_box_main) _menhir_cell1_YESTERDAY, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 029.
        Stack shape : YESTERDAY option(timebound).
        Start symbol: main. *)

  | MenhirState032 : (('s, _menhir_box_main) _menhir_cell1_ONCE, _menhir_box_main) _menhir_state
    (** State 032.
        Stack shape : ONCE.
        Start symbol: main. *)

  | MenhirState033 : ((('s, _menhir_box_main) _menhir_cell1_ONCE, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 033.
        Stack shape : ONCE option(timebound).
        Start symbol: main. *)

  | MenhirState034 : (('s, _menhir_box_main) _menhir_cell1_NOT, _menhir_box_main) _menhir_state
    (** State 034.
        Stack shape : NOT.
        Start symbol: main. *)

  | MenhirState035 : (('s, _menhir_box_main) _menhir_cell1_NEXT, _menhir_box_main) _menhir_state
    (** State 035.
        Stack shape : NEXT.
        Start symbol: main. *)

  | MenhirState036 : ((('s, _menhir_box_main) _menhir_cell1_NEXT, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 036.
        Stack shape : NEXT option(timebound).
        Start symbol: main. *)

  | MenhirState037 : (('s, _menhir_box_main) _menhir_cell1_LPAREN, _menhir_box_main) _menhir_state
    (** State 037.
        Stack shape : LPAREN.
        Start symbol: main. *)

  | MenhirState040 : (('s, _menhir_box_main) _menhir_cell1_ID, _menhir_box_main) _menhir_state
    (** State 040.
        Stack shape : ID.
        Start symbol: main. *)

  | MenhirState042 : (('s, _menhir_box_main) _menhir_cell1_ID, _menhir_box_main) _menhir_state
    (** State 042.
        Stack shape : ID.
        Start symbol: main. *)

  | MenhirState045 : (('s, _menhir_box_main) _menhir_cell1_term, _menhir_box_main) _menhir_state
    (** State 045.
        Stack shape : term.
        Start symbol: main. *)

  | MenhirState052 : (('s, _menhir_box_main) _menhir_cell1_HISTORICALLY, _menhir_box_main) _menhir_state
    (** State 052.
        Stack shape : HISTORICALLY.
        Start symbol: main. *)

  | MenhirState053 : ((('s, _menhir_box_main) _menhir_cell1_HISTORICALLY, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 053.
        Stack shape : HISTORICALLY option(timebound).
        Start symbol: main. *)

  | MenhirState054 : (('s, _menhir_box_main) _menhir_cell1_FORALL, _menhir_box_main) _menhir_state
    (** State 054.
        Stack shape : FORALL.
        Start symbol: main. *)

  | MenhirState056 : (('s, _menhir_box_main) _menhir_cell1_ID, _menhir_box_main) _menhir_state
    (** State 056.
        Stack shape : ID.
        Start symbol: main. *)

  | MenhirState059 : ((('s, _menhir_box_main) _menhir_cell1_FORALL, _menhir_box_main) _menhir_cell1_separated_nonempty_list_COMMA_ID_, _menhir_box_main) _menhir_state
    (** State 059.
        Stack shape : FORALL separated_nonempty_list(COMMA,ID).
        Start symbol: main. *)

  | MenhirState061 : (('s, _menhir_box_main) _menhir_cell1_EXISTS, _menhir_box_main) _menhir_state
    (** State 061.
        Stack shape : EXISTS.
        Start symbol: main. *)

  | MenhirState063 : ((('s, _menhir_box_main) _menhir_cell1_EXISTS, _menhir_box_main) _menhir_cell1_separated_nonempty_list_COMMA_ID_, _menhir_box_main) _menhir_state
    (** State 063.
        Stack shape : EXISTS separated_nonempty_list(COMMA,ID).
        Start symbol: main. *)

  | MenhirState064 : (('s, _menhir_box_main) _menhir_cell1_EVENTUALLY, _menhir_box_main) _menhir_state
    (** State 064.
        Stack shape : EVENTUALLY.
        Start symbol: main. *)

  | MenhirState065 : ((('s, _menhir_box_main) _menhir_cell1_EVENTUALLY, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 065.
        Stack shape : EVENTUALLY option(timebound).
        Start symbol: main. *)

  | MenhirState066 : (('s, _menhir_box_main) _menhir_cell1_ALWAYS, _menhir_box_main) _menhir_state
    (** State 066.
        Stack shape : ALWAYS.
        Start symbol: main. *)

  | MenhirState067 : ((('s, _menhir_box_main) _menhir_cell1_ALWAYS, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 067.
        Stack shape : ALWAYS option(timebound).
        Start symbol: main. *)

  | MenhirState069 : (('s, _menhir_box_main) _menhir_cell1_term, _menhir_box_main) _menhir_state
    (** State 069.
        Stack shape : term.
        Start symbol: main. *)

  | MenhirState071 : (('s, _menhir_box_main) _menhir_cell1_term, _menhir_box_main) _menhir_state
    (** State 071.
        Stack shape : term.
        Start symbol: main. *)

  | MenhirState073 : (('s, _menhir_box_main) _menhir_cell1_term, _menhir_box_main) _menhir_state
    (** State 073.
        Stack shape : term.
        Start symbol: main. *)

  | MenhirState075 : (('s, _menhir_box_main) _menhir_cell1_term, _menhir_box_main) _menhir_state
    (** State 075.
        Stack shape : term.
        Start symbol: main. *)

  | MenhirState077 : (('s, _menhir_box_main) _menhir_cell1_term, _menhir_box_main) _menhir_state
    (** State 077.
        Stack shape : term.
        Start symbol: main. *)

  | MenhirState079 : (('s, _menhir_box_main) _menhir_cell1_term, _menhir_box_main) _menhir_state
    (** State 079.
        Stack shape : term.
        Start symbol: main. *)

  | MenhirState086 : (('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_state
    (** State 086.
        Stack shape : formula.
        Start symbol: main. *)

  | MenhirState088 : (('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_state
    (** State 088.
        Stack shape : formula.
        Start symbol: main. *)

  | MenhirState090 : (('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_state
    (** State 090.
        Stack shape : formula.
        Start symbol: main. *)

  | MenhirState091 : ((('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 091.
        Stack shape : formula option(timebound).
        Start symbol: main. *)

  | MenhirState093 : (('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_state
    (** State 093.
        Stack shape : formula.
        Start symbol: main. *)

  | MenhirState094 : ((('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_cell1_option_timebound_, _menhir_box_main) _menhir_state
    (** State 094.
        Stack shape : formula option(timebound).
        Start symbol: main. *)

  | MenhirState096 : (('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_state
    (** State 096.
        Stack shape : formula.
        Start symbol: main. *)

  | MenhirState098 : (('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_state
    (** State 098.
        Stack shape : formula.
        Start symbol: main. *)

  | MenhirState100 : (('s, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_state
    (** State 100.
        Stack shape : formula.
        Start symbol: main. *)

  | MenhirState112 : (('s, _menhir_box_main) _menhir_cell1_AT_LBRACKET _menhir_cell0_STRING, _menhir_box_main) _menhir_state
    (** State 112.
        Stack shape : AT_LBRACKET STRING.
        Start symbol: main. *)

  | MenhirState118 : (('s, _menhir_box_main) _menhir_cell1_annotated_formula, _menhir_box_main) _menhir_state
    (** State 118.
        Stack shape : annotated_formula.
        Start symbol: main. *)


and ('s, 'r) _menhir_cell1_annotated_formula = 
  | MenhirCell1_annotated_formula of 's * ('s, 'r) _menhir_state * (Ast.formula)

and ('s, 'r) _menhir_cell1_formula = 
  | MenhirCell1_formula of 's * ('s, 'r) _menhir_state * (Ast.formula)

and 's _menhir_cell0_option_regulation_metadata_ = 
  | MenhirCell0_option_regulation_metadata_ of 's * (Ast.regulation_metadata option)

and ('s, 'r) _menhir_cell1_option_timebound_ = 
  | MenhirCell1_option_timebound_ of 's * ('s, 'r) _menhir_state * ((int * int) option)

and 's _menhir_cell0_option_type_declaration_section_ = 
  | MenhirCell0_option_type_declaration_section_ of 's * (string list option)

and 's _menhir_cell0_option_version_clause_ = 
  | MenhirCell0_option_version_clause_ of 's * (string option)

and ('s, 'r) _menhir_cell1_separated_nonempty_list_COMMA_ID_ = 
  | MenhirCell1_separated_nonempty_list_COMMA_ID_ of 's * ('s, 'r) _menhir_state * (string list)

and ('s, 'r) _menhir_cell1_term = 
  | MenhirCell1_term of 's * ('s, 'r) _menhir_state * (Ast.term)

and ('s, 'r) _menhir_cell1_ALWAYS = 
  | MenhirCell1_ALWAYS of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_AT_LBRACKET = 
  | MenhirCell1_AT_LBRACKET of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_EVENTUALLY = 
  | MenhirCell1_EVENTUALLY of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_EXISTS = 
  | MenhirCell1_EXISTS of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_FORALL = 
  | MenhirCell1_FORALL of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_HISTORICALLY = 
  | MenhirCell1_HISTORICALLY of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_ID = 
  | MenhirCell1_ID of 's * ('s, 'r) _menhir_state * (
# 9 "src/parser.mly"
       (string)
# 342 "src/parser.ml"
)

and 's _menhir_cell0_ID = 
  | MenhirCell0_ID of 's * (
# 9 "src/parser.mly"
       (string)
# 349 "src/parser.ml"
)

and ('s, 'r) _menhir_cell1_LPAREN = 
  | MenhirCell1_LPAREN of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_NEXT = 
  | MenhirCell1_NEXT of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_NOT = 
  | MenhirCell1_NOT of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_ONCE = 
  | MenhirCell1_ONCE of 's * ('s, 'r) _menhir_state

and 's _menhir_cell0_STRING = 
  | MenhirCell0_STRING of 's * (
# 10 "src/parser.mly"
       (string)
# 368 "src/parser.ml"
)

and ('s, 'r) _menhir_cell1_TYPE = 
  | MenhirCell1_TYPE of 's * ('s, 'r) _menhir_state

and ('s, 'r) _menhir_cell1_YESTERDAY = 
  | MenhirCell1_YESTERDAY of 's * ('s, 'r) _menhir_state

and _menhir_box_main = 
  | MenhirBox_main of (Ast.policy_file) [@@unboxed]

let _menhir_action_01 =
  fun cite f ->
    (
# 77 "src/parser.mly"
        ( Annotated(f, cite) )
# 385 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_02 =
  fun f ->
    (
# 79 "src/parser.mly"
        ( f )
# 393 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_03 =
  fun name xs ->
    let args = 
# 241 "<standard.mly>"
    ( xs )
# 401 "src/parser.ml"
     in
    (
# 122 "src/parser.mly"
        ( Predicate(name, args) )
# 406 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_04 =
  fun name ->
    (
# 124 "src/parser.mly"
        ( Predicate(name, []) )
# 414 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_05 =
  fun d ->
    (
# 57 "src/parser.mly"
                                 ( d )
# 422 "src/parser.ml"
     : (string))

let _menhir_action_06 =
  fun _1 ->
    (
# 82 "src/parser.mly"
                     ( _1 )
# 430 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_07 =
  fun f1 f2 ->
    (
# 83 "src/parser.mly"
                                      ( BinLogicalOp(And, f1, f2) )
# 438 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_08 =
  fun f1 f2 ->
    (
# 84 "src/parser.mly"
                                     ( BinLogicalOp(Or, f1, f2) )
# 446 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_09 =
  fun f1 f2 ->
    (
# 85 "src/parser.mly"
                                      ( BinLogicalOp(Iff, f1, f2) )
# 454 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_10 =
  fun f1 f2 ->
    (
# 86 "src/parser.mly"
                                          ( BinLogicalOp(Implies, f1, f2) )
# 462 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_11 =
  fun f1 f2 ->
    (
# 87 "src/parser.mly"
                                      ( BinLogicalOp(Xor, f1, f2) )
# 470 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_12 =
  fun b f1 f2 ->
    (
# 88 "src/parser.mly"
                                                        ( BinTemporalOp(Until, f1, f2, b) )
# 478 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_13 =
  fun b f1 f2 ->
    (
# 89 "src/parser.mly"
                                                        ( BinTemporalOp(Since, f1, f2, b) )
# 486 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_14 =
  fun () ->
    (
# 216 "<standard.mly>"
    ( [] )
# 494 "src/parser.ml"
     : (Ast.formula list))

let _menhir_action_15 =
  fun x xs ->
    let x = 
# 196 "<standard.mly>"
    ( x )
# 502 "src/parser.ml"
     in
    (
# 219 "<standard.mly>"
    ( x :: xs )
# 507 "src/parser.ml"
     : (Ast.formula list))

let _menhir_action_16 =
  fun () ->
    (
# 145 "<standard.mly>"
    ( [] )
# 515 "src/parser.ml"
     : (Ast.term list))

let _menhir_action_17 =
  fun x ->
    (
# 148 "<standard.mly>"
    ( x )
# 523 "src/parser.ml"
     : (Ast.term list))

let _menhir_action_18 =
  fun metadata policy_section type_section ->
    (
# 43 "src/parser.mly"
      ( { metadata = metadata;
          type_decls = (match type_section with None -> [] | Some t -> t);
          policies = policy_section } )
# 533 "src/parser.ml"
     : (Ast.policy_file))

let _menhir_action_19 =
  fun () ->
    (
# 111 "<standard.mly>"
    ( None )
# 541 "src/parser.ml"
     : (string option))

let _menhir_action_20 =
  fun x ->
    (
# 114 "<standard.mly>"
    ( Some x )
# 549 "src/parser.ml"
     : (string option))

let _menhir_action_21 =
  fun () ->
    (
# 111 "<standard.mly>"
    ( None )
# 557 "src/parser.ml"
     : (Ast.regulation_metadata option))

let _menhir_action_22 =
  fun x ->
    (
# 114 "<standard.mly>"
    ( Some x )
# 565 "src/parser.ml"
     : (Ast.regulation_metadata option))

let _menhir_action_23 =
  fun () ->
    (
# 111 "<standard.mly>"
    ( None )
# 573 "src/parser.ml"
     : ((int * int) option))

let _menhir_action_24 =
  fun x ->
    (
# 114 "<standard.mly>"
    ( Some x )
# 581 "src/parser.ml"
     : ((int * int) option))

let _menhir_action_25 =
  fun () ->
    (
# 111 "<standard.mly>"
    ( None )
# 589 "src/parser.ml"
     : (string list option))

let _menhir_action_26 =
  fun x ->
    (
# 114 "<standard.mly>"
    ( Some x )
# 597 "src/parser.ml"
     : (string list option))

let _menhir_action_27 =
  fun () ->
    (
# 111 "<standard.mly>"
    ( None )
# 605 "src/parser.ml"
     : (string option))

let _menhir_action_28 =
  fun x ->
    (
# 114 "<standard.mly>"
    ( Some x )
# 613 "src/parser.ml"
     : (string option))

let _menhir_action_29 =
  fun formulas ->
    (
# 73 "src/parser.mly"
      ( formulas )
# 621 "src/parser.ml"
     : (Ast.formula list))

let _menhir_action_30 =
  fun date name ver ->
    (
# 51 "src/parser.mly"
      ( { name = name; version = ver; effective_date = date } )
# 629 "src/parser.ml"
     : (Ast.regulation_metadata))

let _menhir_action_31 =
  fun x ->
    (
# 250 "<standard.mly>"
    ( [ x ] )
# 637 "src/parser.ml"
     : (string list))

let _menhir_action_32 =
  fun x xs ->
    (
# 253 "<standard.mly>"
    ( x :: xs )
# 645 "src/parser.ml"
     : (string list))

let _menhir_action_33 =
  fun x ->
    (
# 250 "<standard.mly>"
    ( [ x ] )
# 653 "src/parser.ml"
     : (Ast.term list))

let _menhir_action_34 =
  fun x xs ->
    (
# 253 "<standard.mly>"
    ( x :: xs )
# 661 "src/parser.ml"
     : (Ast.term list))

let _menhir_action_35 =
  fun () ->
    (
# 92 "src/parser.mly"
           ( True )
# 669 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_36 =
  fun () ->
    (
# 93 "src/parser.mly"
            ( False )
# 677 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_37 =
  fun f ->
    (
# 94 "src/parser.mly"
                              ( Not f )
# 685 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_38 =
  fun b f ->
    (
# 95 "src/parser.mly"
                                                 ( UnTemporalOp(Always, f, b) )
# 693 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_39 =
  fun b f ->
    (
# 96 "src/parser.mly"
                                                     ( UnTemporalOp(Eventually, f, b) )
# 701 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_40 =
  fun b f ->
    (
# 97 "src/parser.mly"
                                               ( UnTemporalOp(Next, f, b) )
# 709 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_41 =
  fun b f ->
    (
# 98 "src/parser.mly"
                                                       ( UnTemporalOp(Historically, f, b) )
# 717 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_42 =
  fun b f ->
    (
# 99 "src/parser.mly"
                                               ( UnTemporalOp(Once, f, b) )
# 725 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_43 =
  fun b f ->
    (
# 100 "src/parser.mly"
                                                    ( UnTemporalOp(Yesterday, f, b) )
# 733 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_44 =
  fun f ->
    (
# 101 "src/parser.mly"
                                  ( f )
# 741 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_45 =
  fun f vars ->
    (
# 103 "src/parser.mly"
        ( Quantified(Forall vars, f) )
# 749 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_46 =
  fun f vars ->
    (
# 105 "src/parser.mly"
        ( Quantified(Exists vars, f) )
# 757 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_47 =
  fun t1 t2 ->
    (
# 107 "src/parser.mly"
        ( Predicate("=", [t1; t2]) )
# 765 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_48 =
  fun t1 t2 ->
    (
# 109 "src/parser.mly"
        ( Predicate("!=", [t1; t2]) )
# 773 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_49 =
  fun t1 t2 ->
    (
# 111 "src/parser.mly"
        ( Predicate("<", [t1; t2]) )
# 781 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_50 =
  fun t1 t2 ->
    (
# 113 "src/parser.mly"
        ( Predicate("<=", [t1; t2]) )
# 789 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_51 =
  fun t1 t2 ->
    (
# 115 "src/parser.mly"
        ( Predicate(">", [t1; t2]) )
# 797 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_52 =
  fun t1 t2 ->
    (
# 117 "src/parser.mly"
        ( Predicate(">=", [t1; t2]) )
# 805 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_53 =
  fun a ->
    (
# 118 "src/parser.mly"
                         ( a )
# 813 "src/parser.ml"
     : (Ast.formula))

let _menhir_action_54 =
  fun x ->
    (
# 127 "src/parser.mly"
             ( Var x )
# 821 "src/parser.ml"
     : (Ast.term))

let _menhir_action_55 =
  fun c ->
    (
# 128 "src/parser.mly"
                ( Const c )
# 829 "src/parser.ml"
     : (Ast.term))

let _menhir_action_56 =
  fun n ->
    (
# 129 "src/parser.mly"
              ( Const (string_of_int n) )
# 837 "src/parser.ml"
     : (Ast.term))

let _menhir_action_57 =
  fun s ->
    (
# 130 "src/parser.mly"
                 ( Const s )
# 845 "src/parser.ml"
     : (Ast.term))

let _menhir_action_58 =
  fun x xs ->
    let args = 
# 241 "<standard.mly>"
    ( xs )
# 853 "src/parser.ml"
     in
    (
# 132 "src/parser.mly"
        ( Func(x, args) )
# 858 "src/parser.ml"
     : (Ast.term))

let _menhir_action_59 =
  fun t1 t2 ->
    (
# 134 "src/parser.mly"
                                                    ( (t1, t2) )
# 866 "src/parser.ml"
     : (int * int))

let _menhir_action_60 =
  fun types ->
    (
# 63 "src/parser.mly"
      ( types )
# 874 "src/parser.ml"
     : (string list))

let _menhir_action_61 =
  fun () ->
    (
# 66 "src/parser.mly"
      ( [] )
# 882 "src/parser.ml"
     : (string list))

let _menhir_action_62 =
  fun name rest ->
    (
# 67 "src/parser.mly"
                                        ( name :: rest )
# 890 "src/parser.ml"
     : (string list))

let _menhir_action_63 =
  fun v ->
    (
# 54 "src/parser.mly"
                          ( v )
# 898 "src/parser.ml"
     : (string))

let _menhir_print_token : token -> string =
  fun _tok ->
    match _tok with
    | ALWAYS ->
        "ALWAYS"
    | AND ->
        "AND"
    | AT_LBRACKET ->
        "AT_LBRACKET"
    | COMMA ->
        "COMMA"
    | CONST _ ->
        "CONST"
    | DOT ->
        "DOT"
    | EFFECTIVE_DATE ->
        "EFFECTIVE_DATE"
    | EOF ->
        "EOF"
    | EQUALS ->
        "EQUALS"
    | EVENTUALLY ->
        "EVENTUALLY"
    | EXISTS ->
        "EXISTS"
    | FALSE ->
        "FALSE"
    | FORALL ->
        "FORALL"
    | GREATER ->
        "GREATER"
    | GREATEREQ ->
        "GREATEREQ"
    | HISTORICALLY ->
        "HISTORICALLY"
    | ID _ ->
        "ID"
    | IFF ->
        "IFF"
    | IMPLIES ->
        "IMPLIES"
    | INT _ ->
        "INT"
    | LBRACKET ->
        "LBRACKET"
    | LESS ->
        "LESS"
    | LESSEQ ->
        "LESSEQ"
    | LPAREN ->
        "LPAREN"
    | NEXT ->
        "NEXT"
    | NOT ->
        "NOT"
    | NOTEQUALS ->
        "NOTEQUALS"
    | ONCE ->
        "ONCE"
    | OR ->
        "OR"
    | POLICY_END ->
        "POLICY_END"
    | POLICY_START ->
        "POLICY_START"
    | RBRACKET ->
        "RBRACKET"
    | REGULATION ->
        "REGULATION"
    | RPAREN ->
        "RPAREN"
    | SEMICOLON ->
        "SEMICOLON"
    | SINCE ->
        "SINCE"
    | STRING _ ->
        "STRING"
    | TRUE ->
        "TRUE"
    | TYPE ->
        "TYPE"
    | TYPE_DECL_ENDS ->
        "TYPE_DECL_ENDS"
    | TYPE_DECL_START ->
        "TYPE_DECL_START"
    | UNTIL ->
        "UNTIL"
    | VERSION ->
        "VERSION"
    | XOR ->
        "XOR"
    | YESTERDAY ->
        "YESTERDAY"

let _menhir_fail : unit -> 'a =
  fun () ->
    Printf.eprintf "Internal failure -- please contact the parser generator's developers.\n%!";
    assert false

include struct
  
  [@@@ocaml.warning "-4-37"]
  
  let _menhir_run_114 : type  ttv_stack. ttv_stack _menhir_cell0_option_regulation_metadata_ _menhir_cell0_option_type_declaration_section_ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let formulas = _v in
      let _v = _menhir_action_29 formulas in
      match (_tok : MenhirBasics.token) with
      | EOF ->
          let MenhirCell0_option_type_declaration_section_ (_menhir_stack, type_section) = _menhir_stack in
          let MenhirCell0_option_regulation_metadata_ (_menhir_stack, metadata) = _menhir_stack in
          let policy_section = _v in
          let _v = _menhir_action_18 metadata policy_section type_section in
          MenhirBox_main _v
      | _ ->
          _eRR ()
  
  let rec _menhir_run_119 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_annotated_formula -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let MenhirCell1_annotated_formula (_menhir_stack, _menhir_s, x) = _menhir_stack in
      let xs = _v in
      let _v = _menhir_action_15 x xs in
      _menhir_goto_list_terminated_annotated_formula_SEMICOLON__ _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
  
  and _menhir_goto_list_terminated_annotated_formula_SEMICOLON__ : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      match _menhir_s with
      | MenhirState118 ->
          _menhir_run_119 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | MenhirState021 ->
          _menhir_run_114 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | _ ->
          _menhir_fail ()
  
  let rec _menhir_run_022 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_YESTERDAY (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState022
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_029 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState022 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_023 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | INT _v ->
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | COMMA ->
              let _tok = _menhir_lexer _menhir_lexbuf in
              (match (_tok : MenhirBasics.token) with
              | INT _v_0 ->
                  let _tok = _menhir_lexer _menhir_lexbuf in
                  (match (_tok : MenhirBasics.token) with
                  | RBRACKET ->
                      let _tok = _menhir_lexer _menhir_lexbuf in
                      let (t2, t1) = (_v_0, _v) in
                      let _v = _menhir_action_59 t1 t2 in
                      let x = _v in
                      let _v = _menhir_action_24 x in
                      _menhir_goto_option_timebound_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
                  | _ ->
                      _eRR ())
              | _ ->
                  _eRR ())
          | _ ->
              _eRR ())
      | _ ->
          _eRR ()
  
  and _menhir_goto_option_timebound_ : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match _menhir_s with
      | MenhirState093 ->
          _menhir_run_094 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState090 ->
          _menhir_run_091 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState066 ->
          _menhir_run_067 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState064 ->
          _menhir_run_065 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState052 ->
          _menhir_run_053 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState035 ->
          _menhir_run_036 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState032 ->
          _menhir_run_033 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState022 ->
          _menhir_run_029 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _menhir_fail ()
  
  and _menhir_run_094 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_formula as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState094
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState094
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState094
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState094
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState094
      | _ ->
          _eRR ()
  
  and _menhir_run_030 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let _v = _menhir_action_35 () in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_goto_simple_formula : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match _menhir_s with
      | MenhirState029 ->
          _menhir_run_109 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState033 ->
          _menhir_run_108 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState034 ->
          _menhir_run_107 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState036 ->
          _menhir_run_106 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState053 ->
          _menhir_run_103 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState118 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState021 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState112 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState037 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState059 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState100 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState098 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState096 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState094 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState091 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState088 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState086 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState063 ->
          _menhir_run_084 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState065 ->
          _menhir_run_083 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState067 ->
          _menhir_run_081 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | _ ->
          _menhir_fail ()
  
  and _menhir_run_109 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_YESTERDAY, _menhir_box_main) _menhir_cell1_option_timebound_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
      let MenhirCell1_YESTERDAY (_menhir_stack, _menhir_s) = _menhir_stack in
      let f = _v in
      let _v = _menhir_action_43 b f in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_108 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_ONCE, _menhir_box_main) _menhir_cell1_option_timebound_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
      let MenhirCell1_ONCE (_menhir_stack, _menhir_s) = _menhir_stack in
      let f = _v in
      let _v = _menhir_action_42 b f in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_107 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_NOT -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_NOT (_menhir_stack, _menhir_s) = _menhir_stack in
      let f = _v in
      let _v = _menhir_action_37 f in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_106 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_NEXT, _menhir_box_main) _menhir_cell1_option_timebound_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
      let MenhirCell1_NEXT (_menhir_stack, _menhir_s) = _menhir_stack in
      let f = _v in
      let _v = _menhir_action_40 b f in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_103 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_HISTORICALLY, _menhir_box_main) _menhir_cell1_option_timebound_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
      let MenhirCell1_HISTORICALLY (_menhir_stack, _menhir_s) = _menhir_stack in
      let f = _v in
      let _v = _menhir_action_41 b f in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_084 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _1 = _v in
      let _v = _menhir_action_06 _1 in
      _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_goto_formula : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match _menhir_s with
      | MenhirState118 ->
          _menhir_run_116 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState021 ->
          _menhir_run_116 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState112 ->
          _menhir_run_113 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState037 ->
          _menhir_run_104 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState059 ->
          _menhir_run_102 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState100 ->
          _menhir_run_101 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState098 ->
          _menhir_run_099 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState096 ->
          _menhir_run_097 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState094 ->
          _menhir_run_095 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState091 ->
          _menhir_run_092 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState088 ->
          _menhir_run_089 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState086 ->
          _menhir_run_087 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState063 ->
          _menhir_run_085 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _menhir_fail ()
  
  and _menhir_run_116 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IMPLIES ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_098 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_100 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SEMICOLON ->
          let f = _v in
          let _v = _menhir_action_02 f in
          _menhir_goto_annotated_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_086 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _menhir_s = MenhirState086 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_031 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let s = _v in
      let _v = _menhir_action_57 s in
      _menhir_goto_term _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_goto_term : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match _menhir_s with
      | MenhirState079 ->
          _menhir_run_080 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState077 ->
          _menhir_run_078 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState075 ->
          _menhir_run_076 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState073 ->
          _menhir_run_074 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState071 ->
          _menhir_run_072 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState069 ->
          _menhir_run_070 _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | MenhirState118 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState021 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState112 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState029 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState033 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState034 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState036 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState037 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState053 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState059 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState100 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState098 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState096 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState094 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState091 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState088 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState086 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState063 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState065 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState067 ->
          _menhir_run_068 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState040 ->
          _menhir_run_044 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState045 ->
          _menhir_run_044 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | MenhirState042 ->
          _menhir_run_044 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _menhir_fail ()
  
  and _menhir_run_080 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_term -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_term (_menhir_stack, _menhir_s, t1) = _menhir_stack in
      let t2 = _v in
      let _v = _menhir_action_47 t1 t2 in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_078 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_term -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_term (_menhir_stack, _menhir_s, t1) = _menhir_stack in
      let t2 = _v in
      let _v = _menhir_action_51 t1 t2 in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_076 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_term -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_term (_menhir_stack, _menhir_s, t1) = _menhir_stack in
      let t2 = _v in
      let _v = _menhir_action_52 t1 t2 in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_074 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_term -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_term (_menhir_stack, _menhir_s, t1) = _menhir_stack in
      let t2 = _v in
      let _v = _menhir_action_49 t1 t2 in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_072 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_term -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_term (_menhir_stack, _menhir_s, t1) = _menhir_stack in
      let t2 = _v in
      let _v = _menhir_action_50 t1 t2 in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_070 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_term -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_term (_menhir_stack, _menhir_s, t1) = _menhir_stack in
      let t2 = _v in
      let _v = _menhir_action_48 t1 t2 in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_068 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_term (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | NOTEQUALS ->
          let _menhir_s = MenhirState069 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | INT _v ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | ID _v ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | CONST _v ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | LESSEQ ->
          let _menhir_s = MenhirState071 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | INT _v ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | ID _v ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | CONST _v ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | LESS ->
          let _menhir_s = MenhirState073 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | INT _v ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | ID _v ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | CONST _v ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | GREATEREQ ->
          let _menhir_s = MenhirState075 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | INT _v ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | ID _v ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | CONST _v ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | GREATER ->
          let _menhir_s = MenhirState077 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | INT _v ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | ID _v ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | CONST _v ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | EQUALS ->
          let _menhir_s = MenhirState079 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | INT _v ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | ID _v ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | CONST _v ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | _ ->
          _eRR ()
  
  and _menhir_run_038 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let n = _v in
      let _v = _menhir_action_56 n in
      _menhir_goto_term _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_041 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LPAREN ->
          let _menhir_stack = MenhirCell1_ID (_menhir_stack, _menhir_s, _v) in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v_0 ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState042
          | INT _v_1 ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState042
          | ID _v_2 ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState042
          | CONST _v_3 ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState042
          | RPAREN ->
              let _v_4 = _menhir_action_16 () in
              _menhir_run_048 _menhir_stack _menhir_lexbuf _menhir_lexer _v_4
          | _ ->
              _eRR ())
      | AND | COMMA | IFF | IMPLIES | OR | RPAREN | SEMICOLON | SINCE | UNTIL | XOR ->
          let x = _v in
          let _v = _menhir_action_54 x in
          _menhir_goto_term _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_043 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let c = _v in
      let _v = _menhir_action_55 c in
      _menhir_goto_term _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_048 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_ID -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let MenhirCell1_ID (_menhir_stack, _menhir_s, x) = _menhir_stack in
      let xs = _v in
      let _v = _menhir_action_58 x xs in
      _menhir_goto_term _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_044 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | COMMA ->
          let _menhir_stack = MenhirCell1_term (_menhir_stack, _menhir_s, _v) in
          let _menhir_s = MenhirState045 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | INT _v ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | ID _v ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | CONST _v ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | RPAREN ->
          let x = _v in
          let _v = _menhir_action_33 x in
          _menhir_goto_separated_nonempty_list_COMMA_term_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_goto_separated_nonempty_list_COMMA_term_ : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      match _menhir_s with
      | MenhirState040 ->
          _menhir_run_047 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | MenhirState042 ->
          _menhir_run_047 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | MenhirState045 ->
          _menhir_run_046 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | _ ->
          _menhir_fail ()
  
  and _menhir_run_047 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_ID as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let x = _v in
      let _v = _menhir_action_17 x in
      _menhir_goto_loption_separated_nonempty_list_COMMA_term__ _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
  
  and _menhir_goto_loption_separated_nonempty_list_COMMA_term__ : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_ID as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      match _menhir_s with
      | MenhirState040 ->
          _menhir_run_050 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | MenhirState042 ->
          _menhir_run_048 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | _ ->
          _menhir_fail ()
  
  and _menhir_run_050 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_ID -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | AND | IFF | IMPLIES | OR | RPAREN | SEMICOLON | SINCE | UNTIL | XOR ->
          let MenhirCell1_ID (_menhir_stack, _menhir_s, name) = _menhir_stack in
          let xs = _v in
          let _v = _menhir_action_03 name xs in
          _menhir_goto_atomic_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | EQUALS | GREATER | GREATEREQ | LESS | LESSEQ | NOTEQUALS ->
          let MenhirCell1_ID (_menhir_stack, _menhir_s, x) = _menhir_stack in
          let xs = _v in
          let _v = _menhir_action_58 x xs in
          _menhir_goto_term _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_goto_atomic_formula : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let a = _v in
      let _v = _menhir_action_53 a in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_046 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_term -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let MenhirCell1_term (_menhir_stack, _menhir_s, x) = _menhir_stack in
      let xs = _v in
      let _v = _menhir_action_34 x xs in
      _menhir_goto_separated_nonempty_list_COMMA_term_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
  
  and _menhir_run_032 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_ONCE (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState032
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_033 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState032 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_033 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_ONCE as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState033
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState033
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState033
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState033
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState033
      | _ ->
          _eRR ()
  
  and _menhir_run_034 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_NOT (_menhir_stack, _menhir_s) in
      let _menhir_s = MenhirState034 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_035 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_NEXT (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState035
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_036 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState035 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_036 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_NEXT as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState036
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState036
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState036
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState036
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState036
      | _ ->
          _eRR ()
  
  and _menhir_run_037 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_LPAREN (_menhir_stack, _menhir_s) in
      let _menhir_s = MenhirState037 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_039 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LPAREN ->
          let _menhir_stack = MenhirCell1_ID (_menhir_stack, _menhir_s, _v) in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v_0 ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState040
          | INT _v_1 ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState040
          | ID _v_2 ->
              _menhir_run_041 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState040
          | CONST _v_3 ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState040
          | RPAREN ->
              let _v_4 = _menhir_action_16 () in
              _menhir_run_050 _menhir_stack _menhir_lexbuf _menhir_lexer _v_4
          | _ ->
              _eRR ())
      | AND | IFF | IMPLIES | OR | RPAREN | SEMICOLON | SINCE | UNTIL | XOR ->
          let name = _v in
          let _v = _menhir_action_04 name in
          _menhir_goto_atomic_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | EQUALS | GREATER | GREATEREQ | LESS | LESSEQ | NOTEQUALS ->
          let x = _v in
          let _v = _menhir_action_54 x in
          _menhir_goto_term _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_052 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_HISTORICALLY (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState052
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_053 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState052 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_053 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_HISTORICALLY as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState053
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState053
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState053
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState053
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState053
      | _ ->
          _eRR ()
  
  and _menhir_run_054 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_FORALL (_menhir_stack, _menhir_s) in
      let _menhir_s = MenhirState054 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | ID _v ->
          _menhir_run_055 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_055 : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | COMMA ->
          let _menhir_stack = MenhirCell1_ID (_menhir_stack, _menhir_s, _v) in
          let _menhir_s = MenhirState056 in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | ID _v ->
              _menhir_run_055 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
          | _ ->
              _eRR ())
      | DOT ->
          let x = _v in
          let _v = _menhir_action_31 x in
          _menhir_goto_separated_nonempty_list_COMMA_ID_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_goto_separated_nonempty_list_COMMA_ID_ : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      match _menhir_s with
      | MenhirState061 ->
          _menhir_run_062 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | MenhirState054 ->
          _menhir_run_058 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | MenhirState056 ->
          _menhir_run_057 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | _ ->
          _menhir_fail ()
  
  and _menhir_run_062 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_EXISTS as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _menhir_stack = MenhirCell1_separated_nonempty_list_COMMA_ID_ (_menhir_stack, _menhir_s, _v) in
      let _menhir_s = MenhirState063 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_060 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let _v = _menhir_action_36 () in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_061 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_EXISTS (_menhir_stack, _menhir_s) in
      let _menhir_s = MenhirState061 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | ID _v ->
          _menhir_run_055 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_064 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_EVENTUALLY (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState064
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_065 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState064 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_065 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_EVENTUALLY as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState065
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState065
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState065
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState065
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState065
      | _ ->
          _eRR ()
  
  and _menhir_run_066 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_ALWAYS (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState066
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_067 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState066 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_067 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_ALWAYS as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState067
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState067
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState067
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState067
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState067
      | _ ->
          _eRR ()
  
  and _menhir_run_058 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_FORALL as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _menhir_stack = MenhirCell1_separated_nonempty_list_COMMA_ID_ (_menhir_stack, _menhir_s, _v) in
      let _menhir_s = MenhirState059 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_057 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_ID -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let MenhirCell1_ID (_menhir_stack, _menhir_s, x) = _menhir_stack in
      let xs = _v in
      let _v = _menhir_action_32 x xs in
      _menhir_goto_separated_nonempty_list_COMMA_ID_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
  
  and _menhir_run_090 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState090
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_091 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState090 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_091 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_formula as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState091
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState091
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState091
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState091
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState091
      | _ ->
          _eRR ()
  
  and _menhir_run_093 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | LBRACKET ->
          _menhir_run_023 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState093
      | ALWAYS | CONST _ | EVENTUALLY | EXISTS | FALSE | FORALL | HISTORICALLY | ID _ | INT _ | LPAREN | NEXT | NOT | ONCE | STRING _ | TRUE | YESTERDAY ->
          let _v = _menhir_action_23 () in
          _menhir_run_094 _menhir_stack _menhir_lexbuf _menhir_lexer _v MenhirState093 _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_096 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _menhir_s = MenhirState096 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_098 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _menhir_s = MenhirState098 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_100 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _menhir_s = MenhirState100 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_088 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _menhir_s = MenhirState088 in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | STRING _v ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | INT _v ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ID _v ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | CONST _v ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_goto_annotated_formula : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      let _menhir_stack = MenhirCell1_annotated_formula (_menhir_stack, _menhir_s, _v) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState118
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState118
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState118
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState118
      | AT_LBRACKET ->
          _menhir_run_110 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState118
      | POLICY_END ->
          let _v_4 = _menhir_action_14 () in
          _menhir_run_119 _menhir_stack _menhir_lexbuf _menhir_lexer _v_4
      | _ ->
          _eRR ()
  
  and _menhir_run_110 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_AT_LBRACKET (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | STRING _v ->
          let _menhir_stack = MenhirCell0_STRING (_menhir_stack, _v) in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | RBRACKET ->
              let _menhir_s = MenhirState112 in
              let _tok = _menhir_lexer _menhir_lexbuf in
              (match (_tok : MenhirBasics.token) with
              | YESTERDAY ->
                  _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | TRUE ->
                  _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | STRING _v ->
                  _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
              | ONCE ->
                  _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | NOT ->
                  _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | NEXT ->
                  _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | LPAREN ->
                  _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | INT _v ->
                  _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
              | ID _v ->
                  _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
              | HISTORICALLY ->
                  _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | FORALL ->
                  _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | FALSE ->
                  _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | EXISTS ->
                  _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | EVENTUALLY ->
                  _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | CONST _v ->
                  _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
              | ALWAYS ->
                  _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s
              | _ ->
                  _eRR ())
          | _ ->
              _eRR ())
      | _ ->
          _eRR ()
  
  and _menhir_run_113 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_AT_LBRACKET _menhir_cell0_STRING as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IMPLIES ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_098 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_100 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SEMICOLON ->
          let MenhirCell0_STRING (_menhir_stack, cite) = _menhir_stack in
          let MenhirCell1_AT_LBRACKET (_menhir_stack, _menhir_s) = _menhir_stack in
          let f = _v in
          let _v = _menhir_action_01 cite f in
          _menhir_goto_annotated_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
      | _ ->
          _eRR ()
  
  and _menhir_run_104 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_LPAREN as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | RPAREN ->
          let _tok = _menhir_lexer _menhir_lexbuf in
          let MenhirCell1_LPAREN (_menhir_stack, _menhir_s) = _menhir_stack in
          let f = _v in
          let _v = _menhir_action_44 f in
          _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IMPLIES ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_098 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_100 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | _ ->
          _eRR ()
  
  and _menhir_run_102 : type  ttv_stack. (((ttv_stack, _menhir_box_main) _menhir_cell1_FORALL, _menhir_box_main) _menhir_cell1_separated_nonempty_list_COMMA_ID_ as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IMPLIES ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_098 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_100 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | RPAREN | SEMICOLON ->
          let MenhirCell1_separated_nonempty_list_COMMA_ID_ (_menhir_stack, _, vars) = _menhir_stack in
          let MenhirCell1_FORALL (_menhir_stack, _menhir_s) = _menhir_stack in
          let f = _v in
          let _v = _menhir_action_45 f vars in
          _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_101 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_formula as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IMPLIES ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_098 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_100 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | RPAREN | SEMICOLON ->
          let MenhirCell1_formula (_menhir_stack, _menhir_s, f1) = _menhir_stack in
          let f2 = _v in
          let _v = _menhir_action_09 f1 f2 in
          _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_099 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_formula as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IMPLIES ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_098 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF | RPAREN | SEMICOLON ->
          let MenhirCell1_formula (_menhir_stack, _menhir_s, f1) = _menhir_stack in
          let f2 = _v in
          let _v = _menhir_action_10 f1 f2 in
          _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_097 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_formula as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF | IMPLIES | OR | RPAREN | SEMICOLON | SINCE | UNTIL | XOR ->
          let MenhirCell1_formula (_menhir_stack, _menhir_s, f1) = _menhir_stack in
          let f2 = _v in
          let _v = _menhir_action_08 f1 f2 in
          _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_095 : type  ttv_stack. (((ttv_stack, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_cell1_option_timebound_ as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF | IMPLIES | RPAREN | SEMICOLON ->
          let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
          let MenhirCell1_formula (_menhir_stack, _menhir_s, f1) = _menhir_stack in
          let f2 = _v in
          let _v = _menhir_action_13 b f1 f2 in
          _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_092 : type  ttv_stack. (((ttv_stack, _menhir_box_main) _menhir_cell1_formula, _menhir_box_main) _menhir_cell1_option_timebound_ as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF | IMPLIES | RPAREN | SEMICOLON ->
          let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
          let MenhirCell1_formula (_menhir_stack, _menhir_s, f1) = _menhir_stack in
          let f2 = _v in
          let _v = _menhir_action_12 b f1 f2 in
          _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_089 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_formula -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_formula (_menhir_stack, _menhir_s, f1) = _menhir_stack in
      let f2 = _v in
      let _v = _menhir_action_07 f1 f2 in
      _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_087 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_formula as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF | IMPLIES | OR | RPAREN | SEMICOLON | SINCE | UNTIL | XOR ->
          let MenhirCell1_formula (_menhir_stack, _menhir_s, f1) = _menhir_stack in
          let f2 = _v in
          let _v = _menhir_action_11 f1 f2 in
          _menhir_goto_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_085 : type  ttv_stack. (((ttv_stack, _menhir_box_main) _menhir_cell1_EXISTS, _menhir_box_main) _menhir_cell1_separated_nonempty_list_COMMA_ID_ as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      match (_tok : MenhirBasics.token) with
      | XOR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_086 _menhir_stack _menhir_lexbuf _menhir_lexer
      | UNTIL ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_090 _menhir_stack _menhir_lexbuf _menhir_lexer
      | SINCE ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_093 _menhir_stack _menhir_lexbuf _menhir_lexer
      | OR ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_096 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IMPLIES ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_098 _menhir_stack _menhir_lexbuf _menhir_lexer
      | IFF ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_100 _menhir_stack _menhir_lexbuf _menhir_lexer
      | AND ->
          let _menhir_stack = MenhirCell1_formula (_menhir_stack, _menhir_s, _v) in
          _menhir_run_088 _menhir_stack _menhir_lexbuf _menhir_lexer
      | RPAREN | SEMICOLON ->
          let MenhirCell1_separated_nonempty_list_COMMA_ID_ (_menhir_stack, _, vars) = _menhir_stack in
          let MenhirCell1_EXISTS (_menhir_stack, _menhir_s) = _menhir_stack in
          let f = _v in
          let _v = _menhir_action_46 f vars in
          _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
      | _ ->
          _eRR ()
  
  and _menhir_run_083 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_EVENTUALLY, _menhir_box_main) _menhir_cell1_option_timebound_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
      let MenhirCell1_EVENTUALLY (_menhir_stack, _menhir_s) = _menhir_stack in
      let f = _v in
      let _v = _menhir_action_39 b f in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_081 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_ALWAYS, _menhir_box_main) _menhir_cell1_option_timebound_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell1_option_timebound_ (_menhir_stack, _, b) = _menhir_stack in
      let MenhirCell1_ALWAYS (_menhir_stack, _menhir_s) = _menhir_stack in
      let f = _v in
      let _v = _menhir_action_38 b f in
      _menhir_goto_simple_formula _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok
  
  and _menhir_run_029 : type  ttv_stack. ((ttv_stack, _menhir_box_main) _menhir_cell1_YESTERDAY as 'stack) -> _ -> _ -> _ -> ('stack, _menhir_box_main) _menhir_state -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s _tok ->
      let _menhir_stack = MenhirCell1_option_timebound_ (_menhir_stack, _menhir_s, _v) in
      match (_tok : MenhirBasics.token) with
      | YESTERDAY ->
          _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | TRUE ->
          _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | STRING _v_0 ->
          _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState029
      | ONCE ->
          _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | NOT ->
          _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | NEXT ->
          _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | LPAREN ->
          _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | INT _v_1 ->
          _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState029
      | ID _v_2 ->
          _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState029
      | HISTORICALLY ->
          _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | FORALL ->
          _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | FALSE ->
          _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | EXISTS ->
          _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | EVENTUALLY ->
          _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | CONST _v_3 ->
          _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState029
      | ALWAYS ->
          _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState029
      | _ ->
          _eRR ()
  
  let _menhir_goto_option_type_declaration_section_ : type  ttv_stack. ttv_stack _menhir_cell0_option_regulation_metadata_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let _menhir_stack = MenhirCell0_option_type_declaration_section_ (_menhir_stack, _v) in
      match (_tok : MenhirBasics.token) with
      | POLICY_START ->
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | YESTERDAY ->
              _menhir_run_022 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | TRUE ->
              _menhir_run_030 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | STRING _v_0 ->
              _menhir_run_031 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0 MenhirState021
          | ONCE ->
              _menhir_run_032 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | NOT ->
              _menhir_run_034 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | NEXT ->
              _menhir_run_035 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | LPAREN ->
              _menhir_run_037 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | INT _v_1 ->
              _menhir_run_038 _menhir_stack _menhir_lexbuf _menhir_lexer _v_1 MenhirState021
          | ID _v_2 ->
              _menhir_run_039 _menhir_stack _menhir_lexbuf _menhir_lexer _v_2 MenhirState021
          | HISTORICALLY ->
              _menhir_run_052 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | FORALL ->
              _menhir_run_054 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | FALSE ->
              _menhir_run_060 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | EXISTS ->
              _menhir_run_061 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | EVENTUALLY ->
              _menhir_run_064 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | CONST _v_3 ->
              _menhir_run_043 _menhir_stack _menhir_lexbuf _menhir_lexer _v_3 MenhirState021
          | AT_LBRACKET ->
              _menhir_run_110 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | ALWAYS ->
              _menhir_run_066 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState021
          | POLICY_END ->
              let _v_4 = _menhir_action_14 () in
              _menhir_run_114 _menhir_stack _menhir_lexbuf _menhir_lexer _v_4
          | _ ->
              _eRR ())
      | _ ->
          _eRR ()
  
  let _menhir_run_017 : type  ttv_stack. ttv_stack _menhir_cell0_option_regulation_metadata_ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      let types = _v in
      let _v = _menhir_action_60 types in
      let x = _v in
      let _v = _menhir_action_26 x in
      _menhir_goto_option_type_declaration_section_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
  
  let rec _menhir_run_016 : type  ttv_stack. (ttv_stack, _menhir_box_main) _menhir_cell1_TYPE _menhir_cell0_ID -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v ->
      let MenhirCell0_ID (_menhir_stack, name) = _menhir_stack in
      let MenhirCell1_TYPE (_menhir_stack, _menhir_s) = _menhir_stack in
      let rest = _v in
      let _v = _menhir_action_62 name rest in
      _menhir_goto_type_list _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s
  
  and _menhir_goto_type_list : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _menhir_s ->
      match _menhir_s with
      | MenhirState013 ->
          _menhir_run_017 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | MenhirState015 ->
          _menhir_run_016 _menhir_stack _menhir_lexbuf _menhir_lexer _v
      | _ ->
          _menhir_fail ()
  
  let rec _menhir_run_014 : type  ttv_stack. ttv_stack -> _ -> _ -> (ttv_stack, _menhir_box_main) _menhir_state -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _menhir_s ->
      let _menhir_stack = MenhirCell1_TYPE (_menhir_stack, _menhir_s) in
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | ID _v ->
          let _menhir_stack = MenhirCell0_ID (_menhir_stack, _v) in
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | TYPE ->
              _menhir_run_014 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState015
          | TYPE_DECL_ENDS ->
              let _v_0 = _menhir_action_61 () in
              _menhir_run_016 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0
          | _ ->
              _eRR ())
      | _ ->
          _eRR ()
  
  let _menhir_goto_option_regulation_metadata_ : type  ttv_stack. ttv_stack -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let _menhir_stack = MenhirCell0_option_regulation_metadata_ (_menhir_stack, _v) in
      match (_tok : MenhirBasics.token) with
      | TYPE_DECL_START ->
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | TYPE ->
              _menhir_run_014 _menhir_stack _menhir_lexbuf _menhir_lexer MenhirState013
          | TYPE_DECL_ENDS ->
              let _v_0 = _menhir_action_61 () in
              _menhir_run_017 _menhir_stack _menhir_lexbuf _menhir_lexer _v_0
          | _ ->
              _eRR ())
      | POLICY_START ->
          let _v = _menhir_action_25 () in
          _menhir_goto_option_type_declaration_section_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | _ ->
          _eRR ()
  
  let _menhir_goto_option_effective_date_clause_ : type  ttv_stack. ttv_stack _menhir_cell0_ID _menhir_cell0_option_version_clause_ -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let MenhirCell0_option_version_clause_ (_menhir_stack, ver) = _menhir_stack in
      let MenhirCell0_ID (_menhir_stack, name) = _menhir_stack in
      let date = _v in
      let _v = _menhir_action_30 date name ver in
      let x = _v in
      let _v = _menhir_action_22 x in
      _menhir_goto_option_regulation_metadata_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
  
  let _menhir_goto_option_version_clause_ : type  ttv_stack. ttv_stack _menhir_cell0_ID -> _ -> _ -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok ->
      let _menhir_stack = MenhirCell0_option_version_clause_ (_menhir_stack, _v) in
      match (_tok : MenhirBasics.token) with
      | EFFECTIVE_DATE ->
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | STRING _v_0 ->
              let _tok = _menhir_lexer _menhir_lexbuf in
              let d = _v_0 in
              let _v = _menhir_action_05 d in
              let x = _v in
              let _v = _menhir_action_20 x in
              _menhir_goto_option_effective_date_clause_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
          | _ ->
              _eRR ())
      | POLICY_START | TYPE_DECL_START ->
          let _v = _menhir_action_19 () in
          _menhir_goto_option_effective_date_clause_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | _ ->
          _eRR ()
  
  let _menhir_run_000 : type  ttv_stack. ttv_stack -> _ -> _ -> _menhir_box_main =
    fun _menhir_stack _menhir_lexbuf _menhir_lexer ->
      let _tok = _menhir_lexer _menhir_lexbuf in
      match (_tok : MenhirBasics.token) with
      | REGULATION ->
          let _tok = _menhir_lexer _menhir_lexbuf in
          (match (_tok : MenhirBasics.token) with
          | ID _v ->
              let _menhir_stack = MenhirCell0_ID (_menhir_stack, _v) in
              let _tok = _menhir_lexer _menhir_lexbuf in
              (match (_tok : MenhirBasics.token) with
              | VERSION ->
                  let _tok = _menhir_lexer _menhir_lexbuf in
                  (match (_tok : MenhirBasics.token) with
                  | STRING _v_0 ->
                      let _tok = _menhir_lexer _menhir_lexbuf in
                      let v = _v_0 in
                      let _v = _menhir_action_63 v in
                      let x = _v in
                      let _v = _menhir_action_28 x in
                      _menhir_goto_option_version_clause_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
                  | _ ->
                      _eRR ())
              | EFFECTIVE_DATE | POLICY_START | TYPE_DECL_START ->
                  let _v = _menhir_action_27 () in
                  _menhir_goto_option_version_clause_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
              | _ ->
                  _eRR ())
          | _ ->
              _eRR ())
      | POLICY_START | TYPE_DECL_START ->
          let _v = _menhir_action_21 () in
          _menhir_goto_option_regulation_metadata_ _menhir_stack _menhir_lexbuf _menhir_lexer _v _tok
      | _ ->
          _eRR ()
  
end

let main =
  fun _menhir_lexer _menhir_lexbuf ->
    let _menhir_stack = () in
    let MenhirBox_main v = _menhir_run_000 _menhir_stack _menhir_lexbuf _menhir_lexer in
    v
