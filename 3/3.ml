(* Util - strings *)
let explode s = List.init (String.length s) (String.get s);;
let implode cl = String.init (List.length cl) (List.nth cl);;

(* Read lines from file *)
let read_lines name: string list =
  let ic = open_in name in
  let try_read () =
    try Some (input_line ic) with End_of_file -> None in
  let rec loop acc = match try_read () with
    | Some s -> loop (s :: acc)
    | None -> close_in ic; List.rev acc in
  loop [];;

(* Check if it's a symbol *)
let is_symbol (a: char) (symbols: char list): bool =
  match a with
  | x when (List.mem x symbols) -> true 
  | _ -> false;;

(* Check if it's a digit *)
let is_digit (a: char): bool =
  match a with
  | x when (List.mem x ['0';'1';'2';'3';'4';'5';'6';'7';'8';'9']) -> true 
  | _ -> false;;

(* Get a int[][] of where the symbols are *)
let rec get_symbols_pos_h (lines: char list list) (id: int) (symbols: char list): int list list =
  let rec f (line: char list) (id: int) (acc: int list): int list =
    match line with
    | x :: rest when is_symbol x symbols -> f rest (id+1) (acc @ [id])
    | x :: rest -> f rest id (acc @ [0])
    | [] -> acc
  in
  match lines with
  | line :: rest -> let to_append = (f line id []) in to_append :: (get_symbols_pos_h rest (id + (List.length (List.filter (fun x -> x != 0) to_append))) symbols)
  | [] -> [];;

let get_symbols_pos (lines: char list list) (symbols: char list): int list list =
  get_symbols_pos_h lines 1 symbols;;

(* Print int[][] in a readable format *)
let rec print_ill (lines: int list list): unit =
  let rec print_il (line: int list): unit =
    match line with
    | a :: rest -> print_int a; print_char ' '; print_il rest;
    | _ -> print_newline ()
  in match lines with
  | line :: rest -> print_il line; print_ill rest
  | [] -> ();;

(* Get an OR of two int[][] *)
let rec or_ill_h (ill1: int list list) (ill2: int list list) (acc: int list list): int list list =
  let rec f il1 il2 =
    match il1, il2 with
    | a :: r1, b :: r2 -> (
      match a, b with
      | a, 0 -> a :: (f r1 r2)
      | 0, b -> b :: (f r1 r2)
      | a, b -> a :: (f r1 r2) (* if we OR two ints, we prefer the first one -- somewhat arbitrary *)
    )
    | a :: r1, [] -> a :: (f r1 [])
    | [], b :: r2 -> b :: (f [] r2)
    | [], [] -> []
  in
  match ill1, ill2 with
  | il1 :: r1, il2 :: r2 -> or_ill_h r1 r2 (acc @ [f il1 il2])
  | [], il2 :: r2 -> or_ill_h [] r2 (acc @ [f [] il2])
  | il1 :: r1, [] -> or_ill_h r1 [] (acc @ [f il1 []])
  | [], [] -> acc;;

let rec or_ill (ill1: 'a list list) (ill2: 'a list list): 'a list list =
  or_ill_h ill1 ill2 [];;

let rec shift (ill: int list list) (dir_x: int) (dir_y: int): (int list list) =
  let rec remove_last xs = 
    match xs with
    | a :: [] -> []
    | a :: rest -> a :: (remove_last rest)
    | [] -> []
  in
  match dir_x, dir_y with
  | 0, 0 -> ill
  | 1, 1 -> shift (shift ill 1 0) 0 1
  | -1, -1 -> shift (shift ill (-1) 0) 0 (-1)
  | -1, 1 -> shift (shift ill (-1) 0) 0 1
  | 1, -1 -> shift (shift ill 1 0) 0 (-1)
  | -1, 0 -> (
    List.map (fun il ->
      match il with
      | x :: rest -> rest @ [0]
      | [] -> raise (invalid_arg "shift: invalid bll")
      ) ill
  )
  | 1, 0 -> (
    List.map (fun il -> 0 :: (remove_last il)) ill
  )
  | 0, -1 -> (
    match ill with
    | x :: rest -> rest @ []
    | [] -> raise (invalid_arg "shift: invalid bll")
  )
  | 0, 1 -> (
      [] :: (remove_last ill)
  )
  | _, _ -> raise (invalid_arg "shift: invalid direction");;

(* Get a int[][] of symbols' reach *)
let rec get_reach (lines: char list list) (symbols: char list): int list list = 
  let pos = get_symbols_pos lines symbols in
    let pos_1 = shift pos 0 (-1) in
    let pos_2 = shift pos 0 1 in
    let pos_3 = shift pos 1 0 in
    let pos_4 = shift pos (-1) 0 in
    let pos_5 = shift pos 1 1 in
    let pos_6 = shift pos 1 (-1) in
    let pos_7 = shift pos (-1) 1 in 
    let pos_8 = shift pos (-1) (-1) in
    let combined_1 = or_ill pos_1 pos_2 in
    let combined_2 = or_ill pos_3 pos_4 in
    let combined_3 = or_ill pos_5 pos_6 in
    let combined_4 = or_ill pos_7 pos_8 in
    let combined_5 = or_ill combined_1 combined_2 in
    let combined_6 = or_ill combined_3 combined_4 in
  or_ill combined_5 combined_6;;

type element = El of int * int;;

let rec extract_nums (lines: char list list) (symbols: char list): element list =
  let rec extract_from_line (line: char list) (adj_list: int list) (curr_acc: string) (symbol_id: int): element list =
    match line with
    | c :: rest when is_digit(c) -> (
      match adj_list, line with
      | x :: adj_rest, c :: line_rest when symbol_id == 0 -> extract_from_line line_rest adj_rest (curr_acc ^ (String.make 1 c)) x
      | x :: adj_rest, c :: line_rest -> extract_from_line line_rest adj_rest (curr_acc ^ (String.make 1 c)) symbol_id
      | [], [] -> []
      | _, _ -> raise (invalid_arg "Critical error")
    )
    | c :: rest -> (
      match adj_list, curr_acc with
      | _ :: adj_list, str when symbol_id != 0 -> El(symbol_id, int_of_string str) :: (extract_from_line rest adj_list "" 0)
      | [], str when symbol_id != 0 -> [El(symbol_id, int_of_string str)]
      | _ :: adj_list, _ -> extract_from_line rest adj_list "" 0
      | [], _ -> []
    )
    | [] -> if (curr_acc != "") && symbol_id != 0 then [El(symbol_id, int_of_string curr_acc)] else []
  in let rec extract_from_all (lines_left: char list list) (reach_left: int list list): element list =
    match lines_left, reach_left with
    | ld :: lines_left, rd :: reach_left -> (extract_from_line ld rd "" 0) @ (extract_from_all lines_left reach_left)
    | [], [] -> []
    | _, _ -> raise (invalid_arg "Critical error")
  in let reach_bll = get_reach lines symbols
  in extract_from_all lines reach_bll;;

(* Count elements with some id *)
let rec count_elements_with_id (el: element list) (id: int): int =
  match el with
  | El(eid, num) :: rest when eid == id -> 1 + (count_elements_with_id rest id)
  | El(_, _) :: rest -> count_elements_with_id rest id
  | [] -> 0 

(* Get only elements when n of them have the same id *)
let rec filter_elements_h (el: element list) (rest: element list) (n: int): element list =
  match rest with
  | El(eid, num) :: rest when (count_elements_with_id el eid) == n -> El(eid, num) :: (filter_elements_h el rest n)
  | El(_, _) :: rest -> filter_elements_h el rest n
  | [] -> []

let filter_elements (el: element list) (n: int): element list =
  filter_elements_h el el n;;

(* Sort elements by ID so the same are near each other *)
let sort_element_by_id (el: element list): element list = 
  List.sort (fun e1 e2 -> match e1, e2 with El(id1, _), El(id2, _) -> compare id1 id2) el

(* Print elements *)
let print_elements (el: element list): unit =
  List.iter (function El(a, b) -> print_int a; print_char ' '; print_int b; print_newline ()) el;;

(* Calculate sum of gear ratios *)
(* Gear ratio = numbers of elements with the same id multiplied together *)
let rec sum_of_gear_ratios (sorted_el: element list): int =
  match sorted_el with
  | El(_, num1) :: El(_, num2) :: rest -> (num1 * num2) + (sum_of_gear_ratios rest)
  | [] -> 0
  | _ -> raise (invalid_arg "Wrong input: length not even")

(*      *)
(* Main *)
(*      *)

let lines: string list = (read_lines "input.txt");;
let char_lists: char list list = List.filter (fun line -> List.length line > 1) (List.map explode lines);;

open Printf;;

(* print back input *)
(* List.iter (fun xs -> List.iter (printf "%c") xs; print_newline ()) (char_lists);; *)

let reach = get_reach char_lists;; (* reach test *)
(* print_ill reach;; *)

(* Ex. 1 *)
print_endline "Ex. 1: ";;
let symbols = ['!';'@';'#';'$';'%';'^';'&';'*';'(';')';'+';'-';'_';'/';'=';'>';'<';'~';'`';'\\';',';'?';'[';']';'{';'}';':';';';'|';'"';'\''];;
let nums = extract_nums char_lists symbols in
let sum = List.fold_left (fun acc x -> match x with El(_, num) -> acc + num) 0 nums in
print_int sum;;
print_newline ();;

(* Ex. 2 *)
print_endline "Ex. 2: ";;
let elements = extract_nums char_lists ['*'];;
(* print_elements elements;; *)

let filtered = (filter_elements elements 2);;
(* print_elements filtered;; *)

let sorted = (sort_element_by_id filtered);;
(* print_elements sorted;; *)

let s = sum_of_gear_ratios sorted;;
print_int s;;
print_newline ();;
