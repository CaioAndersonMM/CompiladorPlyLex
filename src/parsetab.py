
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ALL AND CARDINALIDADE CLASS DISJOINTCLASSES DISJOINTWITH EQUIVALENTTO EXACTLY IDENTIFICADOR_CLASSE IDENTIFICADOR_INDIVIDUO IDENTIFICADOR_PROPRIEDADE INDIVIDUALS LPAREN MAIOR MAIORIGUAL MAX MENOR MENORIGUAL MIN NAMESPACE NOT ONLY OR RPAREN SIMBOLO_ESPECIAL SOME SUBCLASSOF THAT TIPO_DADO VALUEontologia : declaracao_classe\n                 | ontologia declaracao_classedeclaracao_classe : declaracao_classe_definida\n                        | declaracao_classe_primitivadeclaracao_classe_definida : CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO tipo_classe_definida individuals_opcionaldeclaracao_classe_primitiva : CLASS IDENTIFICADOR_CLASSE subclassoff_opcional disjoint_opcional individuals_opcionaltipo_classe_definida : classe_enumerada\n                             | classe_coberta\n                             | classe_aninhadasubclassoff_opcional : SUBCLASSOF sequencia_subclassof\n                             | SUBCLASSOF classe_aninhada\n                             | SUBCLASSOF IDENTIFICADOR_CLASSE\n                             | SUBCLASSOF IDENTIFICADOR_CLASSE SIMBOLO_ESPECIAL sequencia_subclassof\n                             | sequencia_subclassof : sequencia_subclassof SIMBOLO_ESPECIAL conteudo_aninhamento\n                   | conteudo_aninhamento disjoint_opcional : DISJOINTCLASSES identificadores_classe_sequencia\n                             |  classe_enumerada : SIMBOLO_ESPECIAL identificadores_classe_sequencia SIMBOLO_ESPECIALclasse_coberta : identificadores_classe_sequenciaclasse_aninhada : IDENTIFICADOR_CLASSE AND aninhamento\n                        | AND aninhamentoaninhamento : conteudo_aninhamento_com_parenteses\n                   | LPAREN conteudo_aninhamento_com_parenteses OR conteudo_aninhamento_com_parenteses RPAREN\n                   | LPAREN aninhamento RPAREN\n                   | conteudo_aninhamento_com_parenteses AND aninhamentoconteudo_aninhamento_com_parenteses : LPAREN conteudo_aninhamento RPARENconteudo_aninhamento :  IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_pos\n                             | IDENTIFICADOR_PROPRIEDADE MIN CARDINALIDADE conteudo_aninhamento_pos\n                             | IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_com_parentesesconteudo_aninhamento_pos : IDENTIFICADOR_CLASSE\n                                | NAMESPACE TIPO_DADO\n                                | LPAREN identificadores_classe_or RPAREN\n                                | NAMESPACE TIPO_DADO SIMBOLO_ESPECIAL operador_relacional cardinalidade_com_sem_aspas_simples SIMBOLO_ESPECIAL\n    individuals_opcional : INDIVIDUALS identificadores_individuo_sequencia\n                         | \n                         | INDIVIDUALS\n                         | identificadores_individuo_sequencia\n    operador_relacional : MAIOR\n                            | MENOR\n                            | MAIORIGUAL\n                            | MENORIGUALcardinalidade_com_sem_aspas_simples : CARDINALIDADE\n                                | SIMBOLO_ESPECIAL CARDINALIDADE SIMBOLO_ESPECIALidentificadores_classe_sequencia : IDENTIFICADOR_CLASSE\n                                         | identificadores_classe_sequencia SIMBOLO_ESPECIAL IDENTIFICADOR_CLASSEidentificadores_classe_or : IDENTIFICADOR_CLASSE\n                                | identificadores_classe_or OR IDENTIFICADOR_CLASSEidentificadores_individuo_sequencia : IDENTIFICADOR_INDIVIDUO\n                                         | identificadores_individuo_sequencia SIMBOLO_ESPECIAL IDENTIFICADOR_INDIVIDUOrestricao_propriedade : ONLY\n                            | SOME\n                            | VALUE'
    
_lr_action_items = {'CLASS':([0,1,2,3,4,6,7,9,11,12,13,14,15,17,19,21,22,23,24,27,28,29,30,32,34,35,37,38,46,47,49,50,56,57,58,59,60,64,65,67,68,69,72,77,79,90,],[5,5,-1,-3,-4,-2,-14,-18,-45,-36,-7,-8,-9,-20,-36,-10,-11,-12,-16,-5,-37,-38,-49,-45,-22,-23,-6,-17,-21,-35,-19,-46,-15,-13,-28,-30,-31,-50,-26,-25,-27,-32,-29,-33,-24,-34,]),'$end':([1,2,3,4,6,7,9,11,12,13,14,15,17,19,21,22,23,24,27,28,29,30,32,34,35,37,38,46,47,49,50,56,57,58,59,60,64,65,67,68,69,72,77,79,90,],[0,-1,-3,-4,-2,-14,-18,-45,-36,-7,-8,-9,-20,-36,-10,-11,-12,-16,-5,-37,-38,-49,-45,-22,-23,-6,-17,-21,-35,-19,-46,-15,-13,-28,-30,-31,-50,-26,-25,-27,-32,-29,-33,-24,-34,]),'IDENTIFICADOR_CLASSE':([5,8,10,16,20,33,41,43,44,45,49,62,63,73,78,],[7,11,23,32,32,50,60,-51,-52,-53,50,71,60,71,85,]),'EQUIVALENTTO':([7,],[8,]),'SUBCLASSOF':([7,],[10,]),'DISJOINTCLASSES':([7,9,21,22,23,24,34,35,46,56,57,58,59,60,65,67,68,69,72,77,79,90,],[-14,20,-10,-11,-12,-16,-22,-23,-21,-15,-13,-28,-30,-31,-26,-25,-27,-32,-29,-33,-24,-34,]),'INDIVIDUALS':([7,9,11,12,13,14,15,17,19,21,22,23,24,32,34,35,38,46,49,50,56,57,58,59,60,65,67,68,69,72,77,79,90,],[-14,-18,-45,28,-7,-8,-9,-20,28,-10,-11,-12,-16,-45,-22,-23,-17,-21,-19,-46,-15,-13,-28,-30,-31,-26,-25,-27,-32,-29,-33,-24,-34,]),'IDENTIFICADOR_INDIVIDUO':([7,9,11,12,13,14,15,17,19,21,22,23,24,28,32,34,35,38,46,48,49,50,56,57,58,59,60,65,67,68,69,72,77,79,90,],[-14,-18,-45,30,-7,-8,-9,-20,30,-10,-11,-12,-16,30,-45,-22,-23,-17,-21,64,-19,-46,-15,-13,-28,-30,-31,-26,-25,-27,-32,-29,-33,-24,-34,]),'SIMBOLO_ESPECIAL':([8,11,17,21,23,24,29,30,31,32,38,47,50,56,57,58,59,60,64,68,69,72,77,80,81,82,83,84,87,88,89,90,91,],[16,-45,33,39,40,-16,48,-49,49,-45,33,48,-46,-15,39,-28,-30,-31,-50,-27,76,-29,-33,86,-39,-40,-41,-42,90,-43,91,-34,-44,]),'AND':([8,10,11,23,35,53,68,],[18,18,26,26,51,51,-27,]),'IDENTIFICADOR_PROPRIEDADE':([10,36,39,40,52,62,74,],[25,25,25,25,25,25,25,]),'LPAREN':([18,26,36,41,43,44,45,51,52,63,66,],[36,36,52,62,-51,-52,-53,36,52,73,74,]),'MIN':([25,],[42,]),'ONLY':([25,],[43,]),'SOME':([25,],[44,]),'VALUE':([25,],[45,]),'RPAREN':([35,53,54,55,58,59,60,65,67,68,69,70,71,72,75,77,79,85,90,],[-23,-23,67,68,-28,-30,-31,-26,-25,-27,-32,77,-47,-29,79,-33,-24,-48,-34,]),'NAMESPACE':([41,43,44,45,63,],[61,-51,-52,-53,61,]),'CARDINALIDADE':([42,80,81,82,83,84,86,],[63,88,-39,-40,-41,-42,89,]),'OR':([53,68,70,71,85,],[66,-27,78,-47,-48,]),'TIPO_DADO':([61,],[69,]),'MAIOR':([76,],[81,]),'MENOR':([76,],[82,]),'MAIORIGUAL':([76,],[83,]),'MENORIGUAL':([76,],[84,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'ontologia':([0,],[1,]),'declaracao_classe':([0,1,],[2,6,]),'declaracao_classe_definida':([0,1,],[3,3,]),'declaracao_classe_primitiva':([0,1,],[4,4,]),'subclassoff_opcional':([7,],[9,]),'tipo_classe_definida':([8,],[12,]),'classe_enumerada':([8,],[13,]),'classe_coberta':([8,],[14,]),'classe_aninhada':([8,10,],[15,22,]),'identificadores_classe_sequencia':([8,16,20,],[17,31,38,]),'disjoint_opcional':([9,],[19,]),'sequencia_subclassof':([10,40,],[21,57,]),'conteudo_aninhamento':([10,36,39,40,52,62,74,],[24,55,56,24,55,55,55,]),'individuals_opcional':([12,19,],[27,37,]),'identificadores_individuo_sequencia':([12,19,28,],[29,29,47,]),'aninhamento':([18,26,36,51,52,],[34,46,54,65,54,]),'conteudo_aninhamento_com_parenteses':([18,26,36,41,51,52,66,],[35,35,53,59,35,53,75,]),'restricao_propriedade':([25,],[41,]),'conteudo_aninhamento_pos':([41,63,],[58,72,]),'identificadores_classe_or':([62,73,],[70,70,]),'operador_relacional':([76,],[80,]),'cardinalidade_com_sem_aspas_simples':([80,],[87,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> ontologia","S'",1,None,None,None),
  ('ontologia -> declaracao_classe','ontologia',1,'p_ontologia','lexer.py',145),
  ('ontologia -> ontologia declaracao_classe','ontologia',2,'p_ontologia','lexer.py',146),
  ('declaracao_classe -> declaracao_classe_definida','declaracao_classe',1,'p_declaracao_classe','lexer.py',153),
  ('declaracao_classe -> declaracao_classe_primitiva','declaracao_classe',1,'p_declaracao_classe','lexer.py',154),
  ('declaracao_classe_definida -> CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO tipo_classe_definida individuals_opcional','declaracao_classe_definida',5,'p_declaracao_classe_definida','lexer.py',160),
  ('declaracao_classe_primitiva -> CLASS IDENTIFICADOR_CLASSE subclassoff_opcional disjoint_opcional individuals_opcional','declaracao_classe_primitiva',5,'p_declaracao_classe_primitiva','lexer.py',164),
  ('tipo_classe_definida -> classe_enumerada','tipo_classe_definida',1,'p_tipo_classe_definida','lexer.py',175),
  ('tipo_classe_definida -> classe_coberta','tipo_classe_definida',1,'p_tipo_classe_definida','lexer.py',176),
  ('tipo_classe_definida -> classe_aninhada','tipo_classe_definida',1,'p_tipo_classe_definida','lexer.py',177),
  ('subclassoff_opcional -> SUBCLASSOF sequencia_subclassof','subclassoff_opcional',2,'p_subclassoff_opcional','lexer.py',182),
  ('subclassoff_opcional -> SUBCLASSOF classe_aninhada','subclassoff_opcional',2,'p_subclassoff_opcional','lexer.py',183),
  ('subclassoff_opcional -> SUBCLASSOF IDENTIFICADOR_CLASSE','subclassoff_opcional',2,'p_subclassoff_opcional','lexer.py',184),
  ('subclassoff_opcional -> SUBCLASSOF IDENTIFICADOR_CLASSE SIMBOLO_ESPECIAL sequencia_subclassof','subclassoff_opcional',4,'p_subclassoff_opcional','lexer.py',185),
  ('subclassoff_opcional -> <empty>','subclassoff_opcional',0,'p_subclassoff_opcional','lexer.py',186),
  ('sequencia_subclassof -> sequencia_subclassof SIMBOLO_ESPECIAL conteudo_aninhamento','sequencia_subclassof',3,'p_sequencia_subclassof','lexer.py',195),
  ('sequencia_subclassof -> conteudo_aninhamento','sequencia_subclassof',1,'p_sequencia_subclassof','lexer.py',196),
  ('disjoint_opcional -> DISJOINTCLASSES identificadores_classe_sequencia','disjoint_opcional',2,'p_disjoint_opcional','lexer.py',203),
  ('disjoint_opcional -> <empty>','disjoint_opcional',0,'p_disjoint_opcional','lexer.py',204),
  ('classe_enumerada -> SIMBOLO_ESPECIAL identificadores_classe_sequencia SIMBOLO_ESPECIAL','classe_enumerada',3,'p_classe_enumerada','lexer.py',211),
  ('classe_coberta -> identificadores_classe_sequencia','classe_coberta',1,'p_classe_coberta','lexer.py',215),
  ('classe_aninhada -> IDENTIFICADOR_CLASSE AND aninhamento','classe_aninhada',3,'p_classe_aninhada','lexer.py',219),
  ('classe_aninhada -> AND aninhamento','classe_aninhada',2,'p_classe_aninhada','lexer.py',220),
  ('aninhamento -> conteudo_aninhamento_com_parenteses','aninhamento',1,'p_aninhamento','lexer.py',229),
  ('aninhamento -> LPAREN conteudo_aninhamento_com_parenteses OR conteudo_aninhamento_com_parenteses RPAREN','aninhamento',5,'p_aninhamento','lexer.py',230),
  ('aninhamento -> LPAREN aninhamento RPAREN','aninhamento',3,'p_aninhamento','lexer.py',231),
  ('aninhamento -> conteudo_aninhamento_com_parenteses AND aninhamento','aninhamento',3,'p_aninhamento','lexer.py',232),
  ('conteudo_aninhamento_com_parenteses -> LPAREN conteudo_aninhamento RPAREN','conteudo_aninhamento_com_parenteses',3,'p_conteudo_aninhamento_com_parenteses','lexer.py',243),
  ('conteudo_aninhamento -> IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_pos','conteudo_aninhamento',3,'p_conteudo_aninhamento','lexer.py',247),
  ('conteudo_aninhamento -> IDENTIFICADOR_PROPRIEDADE MIN CARDINALIDADE conteudo_aninhamento_pos','conteudo_aninhamento',4,'p_conteudo_aninhamento','lexer.py',248),
  ('conteudo_aninhamento -> IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_com_parenteses','conteudo_aninhamento',3,'p_conteudo_aninhamento','lexer.py',249),
  ('conteudo_aninhamento_pos -> IDENTIFICADOR_CLASSE','conteudo_aninhamento_pos',1,'p_conteudo_aninhamento_pos','lexer.py',257),
  ('conteudo_aninhamento_pos -> NAMESPACE TIPO_DADO','conteudo_aninhamento_pos',2,'p_conteudo_aninhamento_pos','lexer.py',258),
  ('conteudo_aninhamento_pos -> LPAREN identificadores_classe_or RPAREN','conteudo_aninhamento_pos',3,'p_conteudo_aninhamento_pos','lexer.py',259),
  ('conteudo_aninhamento_pos -> NAMESPACE TIPO_DADO SIMBOLO_ESPECIAL operador_relacional cardinalidade_com_sem_aspas_simples SIMBOLO_ESPECIAL','conteudo_aninhamento_pos',6,'p_conteudo_aninhamento_pos','lexer.py',260),
  ('individuals_opcional -> INDIVIDUALS identificadores_individuo_sequencia','individuals_opcional',2,'p_individuals_opcional','lexer.py',272),
  ('individuals_opcional -> <empty>','individuals_opcional',0,'p_individuals_opcional','lexer.py',273),
  ('individuals_opcional -> INDIVIDUALS','individuals_opcional',1,'p_individuals_opcional','lexer.py',274),
  ('individuals_opcional -> identificadores_individuo_sequencia','individuals_opcional',1,'p_individuals_opcional','lexer.py',275),
  ('operador_relacional -> MAIOR','operador_relacional',1,'p_operador_relacional','lexer.py',288),
  ('operador_relacional -> MENOR','operador_relacional',1,'p_operador_relacional','lexer.py',289),
  ('operador_relacional -> MAIORIGUAL','operador_relacional',1,'p_operador_relacional','lexer.py',290),
  ('operador_relacional -> MENORIGUAL','operador_relacional',1,'p_operador_relacional','lexer.py',291),
  ('cardinalidade_com_sem_aspas_simples -> CARDINALIDADE','cardinalidade_com_sem_aspas_simples',1,'p_cardinalidade_com_sem_aspas_simples','lexer.py',295),
  ('cardinalidade_com_sem_aspas_simples -> SIMBOLO_ESPECIAL CARDINALIDADE SIMBOLO_ESPECIAL','cardinalidade_com_sem_aspas_simples',3,'p_cardinalidade_com_sem_aspas_simples','lexer.py',296),
  ('identificadores_classe_sequencia -> IDENTIFICADOR_CLASSE','identificadores_classe_sequencia',1,'p_identificadores_classe_sequencia','lexer.py',303),
  ('identificadores_classe_sequencia -> identificadores_classe_sequencia SIMBOLO_ESPECIAL IDENTIFICADOR_CLASSE','identificadores_classe_sequencia',3,'p_identificadores_classe_sequencia','lexer.py',304),
  ('identificadores_classe_or -> IDENTIFICADOR_CLASSE','identificadores_classe_or',1,'p_identificadores_classe_or','lexer.py',311),
  ('identificadores_classe_or -> identificadores_classe_or OR IDENTIFICADOR_CLASSE','identificadores_classe_or',3,'p_identificadores_classe_or','lexer.py',312),
  ('identificadores_individuo_sequencia -> IDENTIFICADOR_INDIVIDUO','identificadores_individuo_sequencia',1,'p_identificadores_individuo_sequencia','lexer.py',320),
  ('identificadores_individuo_sequencia -> identificadores_individuo_sequencia SIMBOLO_ESPECIAL IDENTIFICADOR_INDIVIDUO','identificadores_individuo_sequencia',3,'p_identificadores_individuo_sequencia','lexer.py',321),
  ('restricao_propriedade -> ONLY','restricao_propriedade',1,'p_restricao_propriedade','lexer.py',328),
  ('restricao_propriedade -> SOME','restricao_propriedade',1,'p_restricao_propriedade','lexer.py',329),
  ('restricao_propriedade -> VALUE','restricao_propriedade',1,'p_restricao_propriedade','lexer.py',330),
]
