(ns csc521.core
	(:gen-class)
  	(:require [instaparse.core :as insta]))


(def whitespace
  (insta/parser "whitespace = #'\\s+'"))

(def parser
  (insta/parser 
    (slurp  "resources/Quirk-EBNF.txt") :auto-whitespace whitespace))


(defn CallByLabel [funLabel & args]
  (apply(resolve (symbol (name funLabel)))args))

(defn third [aList] (nth aList 2))
(defn fourth [aList] (nth aList 3))


(defn CallByLabel [funLabel & args]
  (apply(resolve (symbol (name funLabel)))args))


(defn third [aList] (nth aList 2))
(defn fourth [aList] (nth aList 3))
(defn fifth [aList] (nth aList 4))
(defn sixth [aList] (nth aList 5))
(defn seventh [aList] (nth aList 6))


(defn Program [subtree scope]

  (if 
    ( < 2 (count subtree))
      ((def jpScope (merge scope (CallByLabel (first (second subtree))(second subtree) scope)))	
        (CallByLabel (first (third subtree))(third subtree) jpScope)))
  (if 
    (>= 2 (count subtree))
      (def endscope (CallByLabel(first(second subtree)) (second subtree) scope)))
  (merge scope endscope)); end Program
	
(defn Statement [subtree scope]
  (cond 
    ( = :FunctionDeclaration (first (second subtree)))
      (merge scope (CallByLabel (first (second subtree))(second subtree) scope))
    (= :Assignment (first (second subtree)))
      (merge scope (CallByLabel (first (second subtree))(second subtree) scope))
    (= :Print (first (second subtree)))
      (CallByLabel (first(second subtree))(second subtree) scope)));end Statement

(defn FunctionDeclaration [subtree scope]
  (cond
    (= :RPAREN  (first (second(fifth subtree))))
      (assoc scope (CallByLabel(first (third subtree))(third subtree) scope)
        (CallByLabel (first (second (seventh subtree))) (second (seventh subtree))scope))

    (< 2 (count (fifth subtree)))
      (let [functionName (CallByLabel (first (third subtree))(third subtree)scope)
        paramNames (CallByLabel(first (fifth subtree))(fifth subtree)scope)]
      (assoc scope functionName (vector paramNames (seventh subtree))))));end function declaration

(defn FunctionCallParams [subtree scope]	
  (CallByLabel (first (second subtree))(second subtree) scope)); end function call params


(defn FunctionParams [subtree scope]
  (cond	
    (= 2 (count subtree))
      (println "")
    (< 2 (count subtree))
      (CallByLabel (first (second subtree))(second subtree) scope))); end FunctionParams


(defn FunctionCall [subtree scope]
  (cond 
    (=  :RPAREN (first (second (fourth subtree))))
      (get scope (second (second (second subtree))))
  :else
  ( do
    (def funcName (second (second (second subtree))))
    (def paramvals (CallByLabel (first (fourth subtree))(fourth subtree) scope))
    (def paramname (first (get scope "baz_func")))
    (def funcscope (zipmap paramname paramvals))
    (def funcbody (second (get scope funcName)))
    (first (CallByLabel (first funcbody)funcbody funcscope))))); end function Call



(defn ParameterList [subtree scope]
  (cond
    (= 2 (count subtree))
      (CallByLabel (first (second subtree))(second subtree)scope)
    (< 2 (count subtree))
      (vector (CallByLabel (first (second subtree))(second subtree) scope)
      (CallByLabel ( first (fourth subtree))(fourth subtree) scope))));end parameter list

(defn FunctionBody [subtree scope]
  (if
    ( < 2 (count subtree))
      ((def jpScope (merge scope (CallByLabel (first (second subtree))(second subtree) scope)))	
      (def myvec (CallByLabel (first (third subtree))(third subtree) jpScope))))
  (if
    (>= 2 (count subtree))
      (def endscope (CallByLabel(first(second subtree)) (second subtree) scope)))	
  (vector myvec)); end FunctionBody


(defn Return [subtree scope]
  (CallByLabel (first (third subtree))(third subtree) scope)); end return	

(defn Assignment [subtree scope]
  (cond 
    ( = :SingleAssignment (first (second subtree)))
      (merge scope (CallByLabel (first (second subtree))(second subtree) scope))
    ( = :MultipleAssignment (first (second subtree)))
      (merge scope (CallByLabel (first (second subtree))(second subtree) scope)))); end Assignment


(defn SingleAssignment [subtree scope]	
  (merge scope (assoc {}(CallByLabel (first (third subtree))(third subtree) scope)
    (CallByLabel (first (fifth subtree))(fifth subtree) scope)))); End Single Assignment


(defn MultipleAssignment [subtree scope]	
  (def names (CallByLabel (first (third subtree))(third subtree) scope))
  (def values (CallByLabel (first (fifth subtree))(fifth subtree) scope))
  (zipmap names values)); end Multiple Assignment
		
(defn Print [subtree scope]
  (println (CallByLabel (first (third subtree)) (third subtree) scope)));end print

(defn NameList [subtree scope]
  (cond 
    ( = 2 (count subtree)
      (str (CallByLabel (first (second subtree))(second subtree) scope))
    (< 2 (count subtree))
      (vector (CallByLabel (first (second subtree))(second subtree)scope)(CallByLabel (first (fourth subtree))(fourth subtree)scope)))); end NameList

(defn Parameter [subtree scope]	
  (cond 
    (= nil (get scope (CallByLabel (first (second subtree ))(second subtree)scope)))
    (cond 
      (= :Expression (first (second subtree)))
        (CallByLabel (first (second subtree ))(second subtree)scope)
    :else
      (CallByLabel (first (second subtree))(second subtree) scope))	
  :else	
    (cond (= :Expression (first (second subtree)))
      (get scope (CallByLabel (first (second subtree ))(second subtree)scope))
    :else
      (get scope (CallByLabel (first (second subtree))(second subtree) scope))))); end Parameter

(defn Expression [subtree scope]	
  (cond 
    (= 2 (count subtree))
      (CallByLabel (first (second subtree))(second subtree) scope)
    (= :ADD (first (third subtree)))
      (+ (CallByLabel (first (second subtree))(second subtree) scope)
      (CallByLabel (first (fourth subtree))(fourth subtree) scope))
    (= :SUB (first (third subtree)))
      (- (CallByLabel (first (second subtree))(second subtree) scope)
      (CallByLabel (first (fourth subtree))(fourth subtree) scope)))); end Expression

(defn Term [subtree scope]
  (cond 
    (= 2 (count subtree))
      (CallByLabel (first (second subtree))(second subtree) scope)
    (= :MULT (first (third subtree)))
      (* (CallByLabel (first (second subtree))(second subtree) scope)
      (CallByLabel (first (fourth subtree))(fourth subtree) scope))
    (= :DIV (first (third subtree)))
      (quot (CallByLabel (first (second subtree))(second subtree) scope)
      (CallByLabel (first (fourth subtree))(fourth subtree) scope)))); end Term

(defn Factor [subtree scope]	
  (cond  
    (= 2 (count subtree))
      (CallByLabel (first (second subtree))(second subtree) scope)
    (= :EXP (first (third subtree)))
      (Math/pow (CallByLabel (first (second subtree))(second subtree) scope)
      (CallByLabel (first (fourth subtree))(fourth subtree) scope)))); end Factor

(defn SubExpression [subtree scope]
  (CallByLabel (first (third subtree))(third subtree)scope)); end SubExpression


(defn Value [subtree scope]
  (cond 
    (= :Name (first (second subtree)))
      (CallByLabel (first (second subtree)) subtree scope)
    (= :MyNumber (first (second subtree)))
      (CallByLabel (first (second subtree))(second subtree) scope))); end Value

(defn Name [subtree scope]
  (cond 
    (= 2 (count (second subtree)))
      (cond 
        (= nil (get scope (second (second (second subtree)))))
        (str (second(second subtree)))
      :else
        (get scope (second (second (second subtree)))))
    (= 3 (count (second subtree)))
      (cond 
        (= nil (get scope (second (third (second subtree)))))
        (second (third (second subtree)))
      :else
        (cond
          (= :SUB (first (second (second subtree))))
            (-(get scope (second (third (second subtree)))))
          (= :ADD (first (second (second subtree))))
            (get scope (second (third (second subtree)))))))); end Name

(defn MyNumber [subtree scope]	
  (cond 
    (= 2 (count subtree))
      (Double/parseDouble (second (second subtree)))
    (= :SUB (first (second subtree)))
      (- (Double/parseDouble (second (third subtree))))
    (= :ADD  (first (second subtree)))
      (Double/parseDouble (second (third subtree))))); end Number
	

(defn -main [& args]
  (def stdin (slurp *in*))
  ;(println  *command-line-args*)
  (if (.equals "-pt" (first *command-line-args*))
    (def SHOW_PARSE_TREE true) (def SHOW_PARSE_TREE false))
    (def parse-tree (parser stdin))
  (if (= SHOW_PARSE_TREE true)
    ((println parse-tree) (System/exit 0)))

  (defn interpret [subtree scope] (CallByLabel(first subtree) subtree scope))
  (if (= SHOW_PARSE_TREE false)
    (interpret parse-tree {}))

  (System/exit 0)); end main

(-main)
